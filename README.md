offconf
=======

Replace variables like `${foo}` within files. Also works with environment variables `${env.bar}`.
Now handles piping to given functions and, custom arrow functions also.

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

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
