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

To run unit tests, set up a Python 3.8.5 virtual environment. Add the project folder
to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:path/to/data_cleaner_app"
```
and install dependencies
```bash
pip install requirments.txt
```
Run tests with:
```bash
pytest data_cleaner_app
```

## Running
To generate CSV file from dirty data sample, run:
```bash
python data_cleaner_app/main.py data_cleaner_app/matmatch_data/Ceramic_Raw_Data.csv my_test_output.csv
```

Sample output:
```csv
source,name,internalId,baseMaterial,linearCoefficientOfThermalExpansion,thermalConductivity,fractureToughness,density,specificVolumetricSusceptibility,meltingPoint,warnings
https://www.ceramtec.com/ceramic-materials/zirconium-oxide/,Zirconium Oxide,MAMAC001,Zirconium Oxide,0.000011,"2.5,3","6.5,8",,,,
```
To generate JSON file from dirty data sample, run:
```bash
python data_cleaner_app/main.py data_cleaner_app/matmatch_data/Ceramic_Raw_Data.csv my_test_output.json
```

Sample output:
```json
[
    {
        "source": "https://www.americanelements.com/zirconium-oxide-1314-23-4",
        "name": "Zirconium Oxide",
        "internalId": "MAMAC005",
        "baseMaterial": "Zirconium Oxide",
        "linearCoefficientOfThermalExpansion": "0.0000105",
        "thermalConductivity": "",
        "fractureToughness": "",
        "density": "",
        "specificVolumetricSusceptibility": "",
        "meltingPoint": "2715",
        "warnings": "[{'float_conversion_warning': \"Converted given value 4,919 to float value 4919.0 using ',' thousands marker\"}]"
    }
]
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
* The NumericalMaterial object uses a `.format()` method to ensure that outputs are correctly formatted to the `<single_value/lower_bound,upper_bound(OPTIONAL;temperature>)` format. E.g. `2;20` or `3.0,3.3;0` or `18.2`.
* The file extension of the provided output file name is then used to decide whether to output the normalized data as a `.cvs`, `.json` or `.xlsx` file.

### Design decisiony
* The noramlization system is designed to minimize code repetition (by storing common 
functionality in the `common` directory) while also minimizing coupling (by following
the principle of "composition over inheritance"). The goal of the system design is to
maximize maintainability by designing each normalization function to deal with all given 
test cases, while also ensuring that the function can be easily adapted to futher data 
(including special cases) if and when more test data is made available.
* I decided to include all of the parameters for adjusting the normalization for each
field in the associated normalization function for that field so as to ensure that 
all of the elements of normalization configuration could be adjusted in a single place. 
The normalization procedure for each field is similar, but slightly different, so the 
programme benefits from the possibility for it to be adjusted in this way.
* I added a `warnings` field to the output to inform users when potentially 
problematic normalization decisions have been made:

```json
"warnings": "[{'float_conversion_warning': \"Converted given value 4,919 to float value 4919.0 using ',' thousands marker\"}]
```
* I added error logging and printing of errors to `stdout` in the case of an error (most
likely a value error) being produced while processing any one line of the input CSV:
```
Problem cleaning row number 0 
source                     https://www.ceramtec.com/ceramic-materials/zir...
name                                                  Zirconium Oxide (ZrO2)
internalId                                                          MAMAC001
baseMaterial                                                 Zirconium Oxide
thermal expansion                                      NOT_A_NUMERICAL_VALUE
thermal conductivity                                           2.5 to 3 W/mK
fracture toughness                                          6.5 to 8 MPam1/2
Density                                                                     
Magnetic Susceptibility                                                     
Melting Point                                                               
Name: 0, dtype: object of data: Unable to find unit conversion function for string not_a_numerical_value (cleaned to not_a_numerical_value) in conversion dict {'µmm': <function <lambda> at 0x7fec85fa7700>, 'µm/m': <function <lambda> at 0x7fec85fa7790>, '10-6': <function <lambda> at 0x7fec85fa7820>, '10-6°c': <function <lambda> at 0x7fec85fa7940>} (safe_values=[])

```
In the case of such a failure in the normalization of a single row other rows will not be
affected. To test this functionality, run:
```bash
python data_cleaner_app/main.py data_cleaner_app/matmatch_data/corrupted.csv my_corrupted_output.json
```
* I decided to use the `pandas` library for `csv`/`json`/`xlsx` processing, as it provides
a concise interface for doing so.
* I decided to use the `click` library for building the command line interface tool for
the same reason.
* I decided to write the unit tests using the `Arrange`, `Act`, `Assert` idiom because
I think it provides a readable, standardized format for testing.