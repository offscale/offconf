offconf
=======

Replace variables like `${foo}` within files. Also works with environment variables `${env.bar}`.

See "CLI options" for how to provide additional normal+environment variables.

## Install dependencies

    pip install -r requirements.txt

## Install package

    pip install .

## CLI options

    $ python -m offconf -h
    usage: __main__.py [-h] -f FILENAME -o OUTPUT_FILE [-v VARIABLES]
                       [-e ENV_VARIABLES]

    Interpolate variables from file

    optional arguments:
      -h, --help            show this help message and exit
      -f FILENAME, --filename FILENAME
                            Input file
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Output file
      -v VARIABLES, --variables VARIABLES
                            Any variables to be interpolated (as JSON string)
      -e ENV_VARIABLES, --env-variables ENV_VARIABLES
                            Any environment variables to be interpolated (as JSON string)
