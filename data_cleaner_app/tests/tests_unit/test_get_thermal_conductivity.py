from data_cleaner_app.normalizers.thermal_conductivity_normalizer import (
    get_thermal_conductivity,
)


def test_extract_thermal_conductivity_with_negative_kelvin():
    # Arrange
    given_thermal_conductivity = "1.675 W/m-K"
    expected_thermal_conductity = "1.675"

    # Act
    returned_thermal_conductivity = get_thermal_conductivity(given_thermal_conductivity)

    # Assert
    assert returned_thermal_conductivity == expected_thermal_conductity


def test_extract_thermal_conductivity_with_to_range():
    # Arrange
    given_thermal_conductivity = "2.5 to 3 W/mK"
    expected_thermal_conductity = "2.5,3"

    # Act
    returned_thermal_conductivity = get_thermal_conductivity(given_thermal_conductivity)

    # Assert
    assert returned_thermal_conductivity == expected_thermal_conductity


def test_extract_thermal_conductivity_with_range_and_with_hyphenated_range_and_no_units():
    # Arrange
    given_thermal_conductivity = "2.7 - 3.0"
    expected_thermal_conductity = "2.7,3.0"

    # Act
    returned_thermal_conductivity = get_thermal_conductivity(given_thermal_conductivity)

    # Assert
    assert returned_thermal_conductivity == expected_thermal_conductity
