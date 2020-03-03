import pickle
import re
from datetime import datetime

import numpy as np
import pandas as pd
from tabula import read_pdf

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent='usc-viz-workshop-5-wip')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)  # it can give "Time out" error if too many are requested in quick succession


class cache_locally:
    def __init__(self, expensive_function):
        self.expensive_function = expensive_function
        self.pickle_path = f'[cache]{expensive_function.__name__}.pickle'

        # Read past cache data or start empty
        try:
            with open(self.pickle_path, 'rb') as f:
                self.memory_cache = pickle.load(f)
        except FileNotFoundError:
            self.memory_cache = {}

    def __call__(self, *args, **kwargs):
        if kwargs:
            raise NotImplementedError(f'For simplicity, the {self.__class__.__name__} decorator does not support keyword args.')
        key = args

        # Result is not cached
        if key not in self.memory_cache:
            # Call the expensive function
            self.memory_cache[key] = self.expensive_function(*args)

            # Update the file cache
            with open(self.pickle_path, 'wb') as f:
                pickle.dump(self.memory_cache, f)

        return self.memory_cache[key]


@cache_locally
def find_coordinates(region):
    loc = geocode(region)
    return loc.latitude, loc.longitude


def replace_column_values(df, column, orig2changed):
    """ inplace """
    for orig_val, changed_val in orig2changed.items():
        row_mask = df[column] == orig_val
        df.loc[row_mask, column] = changed_val


def clean_numeric_values(series, dtype=int):
    """ of asterisks and other pollutions """
    def maybe_parse_int(s):
        try:
            return re.findall(r'(\d+)', s)[0]
        except:
            return np.nan
    converted = series.astype(str).map(maybe_parse_int).dropna()
    return converted.astype(dtype)


def parse_china(report_pdf_url: str, pages=3) -> pd.DataFrame:
    df = read_pdf(report_pdf_url, pages=pages)[0]

    # Last row contains totals
    df = df.iloc[:-1]

    if len(df.columns) == 2:
        # The first 6 rows are artifacts due to multi-columns
        df = df.iloc[6:]
        # First column is extracted as "Hong Kong 5917 318 332" (region, population, daily confirmed, daily suspect)
        df.iloc[:, 0] = df.iloc[:, 0].str.split().str[:-3].str.join(' ')

    else:
        df = df.iloc[5:]
    df = pd.DataFrame({
        'region': df.iloc[:, 0],
        # Last column is extracted as "41 65914 2682" (daily deaths, cumulative cases, cumulative deaths)
        # or "1347 7" (cumulative cases, cumulative deaths)
        'cases' : clean_numeric_values(df.iloc[:, -1].str.split().str[-2]),
        'deaths': clean_numeric_values(df.iloc[:, -1].str.split().str[-1]),
    }).reset_index(drop=True)

    # Normalize values for better downstream localization
    replace_column_values(df, 'region', {
        'Taipei and environs': 'Taipei',
    })
    df.region = df.region.map(lambda val: re.sub(r'(.+) sar', r'\1', val, flags=re.IGNORECASE))

    df['further_granularity'] = np.nan
    df.loc[df.region == 'Hubei', 'further_granularity'] = 'Wuhan, Hubei'

    return df


def parse_world(report_pdf_url: str, pages=(4, 5)) -> pd.DataFrame:
    # The table spreads over two pages, but the second one does not have the headers repeated
    dfs = read_pdf(report_pdf_url, pages=pages, pandas_options={'header': None})
    df = pd.concat(dfs)

    country_col = 0
    for column in df:
        all_column_values = ' '.join(df.loc[:, column].values.astype(str).tolist()).lower()
        if 'confirmed' in all_column_values:
            cases_col = column
        if 'deaths' in all_column_values:
            deaths_col = column

    # Remove inline region dividers
    df.dropna(subset=[country_col, cases_col, deaths_col], inplace=True)

    df = pd.DataFrame({
        'region': df.iloc[:, country_col],
        'cases':  clean_numeric_values(df.iloc[:, cases_col] .str.split().str[0]),
        'deaths': clean_numeric_values(df.iloc[:, deaths_col].str.split().str[0]),
    }).dropna().reset_index(drop=True)
    df.cases  = df.cases .astype(int)
    df.deaths = df.deaths.astype(int)

    # Remove row totals and international/cruise ship cases
    bad_mask = df.region.map(lambda r: any(w in r.lower() for w in ['total', 'international', 'diamond', 'princess']))
    df = df[~bad_mask]

    # WHO is diplomatically using the official name of the country, but the geojson is using the colloquial name
    replace_column_values(df, 'region', {
        'Republic of Korea': 'South Korea',
        'America': 'United States of America',
        'United States of': 'United States of America',
        'Russian Federation': 'Russia',
        'North Macedonia': 'Macedonia',
        'Iran (Islamic Republic of)': 'Iran',
        'The United Kingdom': 'The United Kingdom',
        'Viet Nam': 'Vietnam',
    })

    df['further_granularity'] = np.nan
    df.loc[df.region == 'Italy', 'further_granularity'] = 'Milan, Italy'

    return df


@cache_locally
def parse_report(report_pdf_url, china_pages, world_pages):
    china_provinces = parse_china(report_pdf_url, china_pages)
    world_countries = parse_world(report_pdf_url, world_pages)

    all_china = china_provinces.sum()
    all_china.region = 'China'
    world_countries.loc[len(world_countries)] = all_china  # append

    china_provinces['region_kind'] = 'Chinese province'
    world_countries['region_kind'] = 'Country'

    date_str = re.findall(r'(\d{8})', report_pdf_url)[0]
    date = datetime.strptime(date_str, '%Y%m%d')
    china_provinces['date'] = date
    world_countries['date'] = date

    return pd.concat([china_provinces, world_countries])
