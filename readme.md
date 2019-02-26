# Data Viz Workshop

Setup instructions at [stefann.eu/viz-workshop](http://stefann.eu/viz-workshop)





### Dataset Details

| Variable                  | Description                                                  | Format                                 |
| ------------------------- | ------------------------------------------------------------ | -------------------------------------- |
| movie_title               | Original movie title                                         | unicode string                         |
| title_year                | Original release year                                        | 1916 through 2016                      |
| genres                    | Movie categorization                                         | pipe separated categories              |
| plot_keywords             | Keywords describing the movie plot                           | pipe separated keywords(s)             |
| country                   | Production country                                           | categorical string                     |
| language                  | Original release language                                    | categorical string                     |
| duration                  | Movie duration                                               | minutes, integer                       |
| content_rating            | Parent advisory content rating                               | categorical string                     |
| color                     | Original colorization                                        | Color or Black and White               |
| aspect_ratio              | Movie aspect ratio                                           | float (width/height)                   |
| director_name             | Director of the movie                                        | first and last name(s)                 |
| actor_1_name              | Primary actor starring in the movie                          | first and last name(s)                 |
| actor_2_name              | Another starring actor                                       | first and last name(s)                 |
| actor_3_name              | Another starring actor                                       | first and last name(s)                 |
| director_facebook_likes   | Likes on the director's Facebook page                        | rounded to the nearest thousand        |
| actor_1_facebook_likes    | Likes on actor_1's Facebook page                             | rounded to the nearest thousand        |
| actor_2_facebook_likes    | Likes onactor_2's Facebook page                              | rounded to the nearest thousand        |
| actor_3_facebook_likes    | Likes onactor_3's Facebook page                              | likes, rounded to the nearest thousand |
| cast_total_facebook_likes | Total amount of Facebook likes of the entire cast of the movie | count                                  |
| movie_facebook_likes      | Likes on the movie's Facebook page                           | count                                  |
| facenumber_in_poster      | Order of the actor who featured in the movie poster          | zero-indexed                           |
| imdb_score                | IMDB Score                                                   | float, out of ten                      |
| num_voted_users           | Votes on IMDB                                                | count                                  |
| num_user_for_reviews      | User reviews on IMDB                                         | count                                  |
| num_critic_for_reviews    | Critic reviews on IMDB                                       | count                                  |
| movie_imdb_link           | IMDB link of the movie                                       | URL                                    |
| gross                     | Gross earnings of the movie                                  | USD, integer                           |
| budget                    | Budget of the movie                                          | USD, integer                           |