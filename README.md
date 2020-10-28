# Data Cleaner App Programming Task
A simple command line application that transforms "unclean" sample data into a "clean"
format. 

## Project Requirements
* Use of python
  * Done
* Give the possibility to choose from multiple clean output formats: `csv`, `json`, `xlsx`
  * Done
* Unit tests
  * Done

## Testing

To run unit tests, set up a Python 3.8 virtual env and install dependencies
```bash
pip install requirments.txt
```
The run tests with:
```bash
pytest data_cleaner_app
```

## Running
To generate CSV file from dirty data sample, run:
```bash
python data_cleaner_app/main.py data_cleaner_app/matmatch_data/Ceramic_Raw_Data.csv my_test_output.csv
```

To generate JSON file from dirty data sample, run:
```bash
python data_cleaner_app/main.py data_cleaner_app/matmatch_data/Ceramic_Raw_Data.csv my_test_output.json
```

To generate XLSX file from dirty data sample, run:
```bash
python data_cleaner_app/main.py data_cleaner_app/matmatch_data/Ceramic_Raw_Data.csv my_test_output.xlsx
```

## Description

### Approach taken
* A simple Command Line Interface is used to operate the tool.
* Unit testing focuses on ensuring that the correct outputs are produced for given inputs, including all sample data, plus a few additions
* Each input field is processed via a configurable normalization function which attempts to extract the following attributes from the field:
  * A single numeric value, e.g. `2.1`
  * A range of numeric values, e.g. `2.0-2.2`
  * A value conversion function, e.g. `lambda x: 2 * x`
  * A temperature value, e.g. `20.4`
  * A temperature conversion function, e.g. `lambda x: x - 273.15`

Any of the values that can be extracted from the field data are then stored in a NumericalMaterial object.
* The NumericalMaterial object uses a `.format` method to ensure that outputs are correctly formatted to the `<single_value/lower_bound,upper_bound(OPTIONAL;temperature>)` format. E.g. `2;20` or `3.0-3.3;0` or `18.2`.
* The file extension of the provided output file name is then used to decide whether to output the normalized data as a `.cvs`, `.json` or `.xlsx` file.

### Design decision
* I decided to follow the principle of composition over inheritence when designing 
the normalization process, to ensure that the normalization process for each field 
could be individually adjusted without causeing conflicts within a complex 
inheritance hierarchy.
* I also decided to cut down on code repetition by pooling the normalization functions'
common elements in a file of common functions.
* I decided to use the `pandas` library for `csv`/`json`/`xlsx` processing, as it provides
a concise interface for doing so.
* I decided to use the `click` library for building the command line interface tool for
the same reason.
* I decided to write the unit tests using the `Arrange`, `Act`, `Assert` idiom because
I think it provides a readable, standardized format for testing.
* I decided to include all of the parameters for adjusting the normalization for each
field in the associated normalization function for that field so as to ensure that 
all of the elements of normalization configuration could be adjusted in a single place,
using a single idiom. The normalization procedure for each field is similar, but slightly 
different, so the programme benefits from the possibility for it to be adjusted in this
way.