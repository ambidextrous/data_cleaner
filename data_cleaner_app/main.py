import pandas
from pandas import DataFrame
import os
import numpy as np
from typing import Any
import json
import click
import logging

from config import LOGGING_FILE
from data_cleaner_app.normalization.density_normalization import get_density
from data_cleaner_app.normalization.expansion_normalization import (
    get_coefficient_of_expansion,
)
from data_cleaner_app.normalization.magenetic_normalization import (
    get_magnetic_susceptibility,
)
from data_cleaner_app.normalization.metling_normalization import get_metling_point
from data_cleaner_app.normalization.name_normalization import get_name
from data_cleaner_app.normalization.thermal_normalization import (
    get_thermal_conductivity,
)
from data_cleaner_app.normalization.toughness_normalization import (
    get_fracture_toughness,
)

logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)


def clean_data(input_filename: str, output_filename: str):
    cwd = os.getcwd()
    path_to_input = os.path.join(cwd, input_filename)
    df = pandas.read_csv(path_to_input)
    normalized_df = normalize_dataframe(df)
    output_dataframe(normalized_df, output_filename)


def output_dataframe(df: DataFrame, output_file_name: str) -> None:
    """
    Output dataframe as .json, .csv or .xlsx file based on supplied ending of output file name
    """
    try:
        format = output_file_name.split(".")[1]
    except IndexError:
        format = None
    if format == "csv":
        DataFrame.to_csv(df, output_file_name, index=False)
    elif format == "xlsx":
        DataFrame.to_excel(df, output_file_name, index=False)
    elif format == "json":
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        with open(output_file_name, "w") as outfile:
            outfile.write(json.dumps(parsed, indent=4))
    else:
        raise ValueError(
            f"Unable to output to file format {format}, expected one of csv, xlsx or json"
        )


def normalize_dataframe(df: DataFrame) -> DataFrame:
    """
    Normalize an input dataframe to ensure all fields correctly named and numerical 
    fields formatted according to the required <single_val/value_range>;<temperature> format,
    E.g. 2.3;20 or 2.2,2.3;20
    """
    normalized_rows = []
    df = df.fillna("")
    error_indexes = []

    for index, row in df.iterrows():

        try:

            normalized_row_data = {}
            warnings = []

            source = row["source"]
            normalized_row_data["source"] = source

            base_material = row["baseMaterial"]
            normalized_row_data["baseMaterial"] = base_material

            internalId = row["internalId"]
            normalized_row_data["internalId"] = internalId

            name = get_name(row["name"], base_material, warnings)
            normalized_row_data["name"] = name

            thermal_expansion = get_coefficient_of_expansion(
                row["thermal expansion"], warnings
            )
            normalized_row_data[
                "linearCoefficientOfThermalExpansion"
            ] = thermal_expansion

            thermal_conductivity = get_thermal_conductivity(
                row["thermal conductivity"], warnings
            )
            normalized_row_data["thermalConductivity"] = thermal_conductivity

            fracture_toughness = get_fracture_toughness(
                row["fracture toughness"], warnings
            )
            normalized_row_data["fractureToughness"] = fracture_toughness

            density = get_density(row["Density"], warnings)
            normalized_row_data["density"] = density

            magnetic_susceptibility = get_magnetic_susceptibility(
                row["Magnetic Susceptibility"], warnings
            )
            normalized_row_data[
                "specificVolumetricSusceptibility"
            ] = magnetic_susceptibility

            melting_point = get_metling_point(row["Melting Point"], warnings)
            normalized_row_data["meltingPoint"] = melting_point

            normalized_row_data["warnings"] = str(warnings) if warnings else ""

            normalized_rows.append(normalized_row_data)

        except Exception as ex:
            # Log error in row and print to stdout, then continue with other rows
            message = f"Problem cleaning row number {index} {row} of data:\n {ex}"
            logging.error(message)
            error_indexes.append(index)
            print(message)

    if error_indexes:
        errors_warning = f"ERROR: {len(error_indexes)} error(s) while processing row(s): {error_indexes}"
        logging.error(errors_warning)
        print(errors_warning)

    normalized_df = DataFrame(normalized_rows, dtype=str)

    columnTitles = [
        "source",
        "name",
        "internalId",
        "baseMaterial",
        "linearCoefficientOfThermalExpansion",
        "thermalConductivity",
        "fractureToughness",
        "density",
        "specificVolumetricSusceptibility",
        "meltingPoint",
        "warnings",
    ]
    normalized_df = normalized_df.reindex(columns=columnTitles)

    column_names = normalized_df.head()
    for column_name in column_names:
        normalized_df[column_name] = normalized_df[column_name].astype(str)
    normalized_df = normalized_df.fillna("")
    normalized_df.reset_index(drop=True, inplace=True)

    return normalized_df


@click.command(name="clean", help='Cleans a "dirty" file to meet required forma')
@click.argument("input_filename")
@click.argument("output_filename")
def clean(input_filename: str, output_filename: str):
    """
    Command Line Interface tool to insert product table entries

    Example usage:

    python data_cleaner_app/main.py data_cleaner_app/matmatch_data/Ceramic_Raw_Data.csv my_test_output.csv
    """
    clean_data(input_filename, output_filename)


if __name__ == "__main__":
    clean()
