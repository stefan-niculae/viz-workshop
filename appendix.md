# Package manager
Since I couldn't find a good, short pip/venv guide:

Package manager makes it easy to install, manage and share libraries.

A virtual environment makes it easy to keep packages separate between projects. It is useful because you don't want to install everything for every project, and also two projects might require different versions of the same package.

Using the package manager `pip`:
 1. installation: _`pip` comes installed with Python >=3.4_
   - upgrading: `pip install -U pip`
 2. install a package: `pip install <package>`
   - upgrade a package: `pip install -U <package>`
   - install a specific version of a package: `pip install <package>==3.1.40` (add `--force-reinstall` to replace)
 3. view all packages installed: `pip list`
 4. export your installed packages and their versions: `pip freeze > requirements.txt` (the usual file name)
   - the redirect operator (`>`) creates/overwrites the output of the command on the left to the path on the right
 5. install packages from an exported list: `pip install -r requirements.txt`
 6. uninstall a package: `pip uninstall <package>`
 
Using the virtual environment module `venv`:
 1. installation: _`venv` is part of the standard library as of Python 3.5_
 2. create a new virtual environment: `python -m venv path/to/env`
   - `python -m <module>` is the standard way of running a module in Python
   - to create using a different version of Python: `python3.6 -m venv path/to/env`
 3. activate a virtual environment: `source env/bin/activate`
   - `source` is a shell command which executes the file passed as argument
   - your command prompt should now start with `(env) ...$`
 4. deactivate a virtual environment: enter `deactivate` anywhere, or exit your session
 5. Note: you should not commit the `env` folder to version control platforms. The list of packages and their versions (`requirements.txt`) suffices.

Look into OS-specific tools to upgrade your Python version, such as [brew](https://brew.sh) on macOS.
Look into [pyenv](https://github.com/pyenv/pyenv) if you wish to keep multiple versions of Python. 
I also like to the [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) extension, to make managaging virtual environments easier.

> Pip: [guide](https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/) (but use the newer `venv` built-in, [reference](https://docs.python.org/3/library/venv.html))

# Essential style guide:
 - indent with 4 tabs
 - one statement per line (bad: `if x == 1: ...`)
 - don't double-check booleans (bad: `if x is True: ...`)
 
 - leave one blank space between operators (bad: `x+1`, good: `x + 1`)
 - leave one blank space after arguments/collection elements
 - no blank space after default/named arguments
 - leave two blank spaces before inline comments and one after the `#` symbol (bad: `x = 1#comment`, good; `x = 1  # comment`)
 - leave trailing commas (better for version control)
 
 - always give variables descriptive names
 - name variables in `snake_case`
 - constants in `ALL_CAPS`
 - `_` as an ignore variable
 
 - always remember to close files (simpler if using the `with` construct)
 
 >  Style guide: [PEP8's basic](https://www.python.org/dev/peps/pep-0008/), [Google's in depth](http://google.github.io/styleguide/pyguide.html)
 