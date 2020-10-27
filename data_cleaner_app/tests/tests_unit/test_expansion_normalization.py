from data_cleaner_app.normalization.expansion_normalization import (
    get_coefficient_of_expansion,
)


def test_extract_linear_coefficient_of_expansion_with_kelvin():
    # Arrange
    thermal_expansion = "11 x 10-6/K"
    expected_coefficient = "0.000011"

    # Act
    coefficient = get_coefficient_of_expansion(thermal_expansion, [])

    # Assert
    assert coefficient == expected_coefficient


def test_extract_linear_coefficient_of_expansion_with_µm():
    # Arrange
    thermal_expansion = "7.00 µm/m-°C"
    expected_coefficient = "0.000007"

    # Act
    coefficient = get_coefficient_of_expansion(thermal_expansion, [])

    # Assert
    assert coefficient == expected_coefficient


def test_extract_linear_coefficient_of_expansion_with_range():
    # Arrange
    thermal_expansion = "7.9 - 11 x10 -6 / ° C"
    expected_coefficient = "0.0000079,0.000011"

    # Act
    coefficient = get_coefficient_of_expansion(thermal_expansion, [])

    # Assert
    assert coefficient == expected_coefficient


def test_extract_linear_coefficient_of_expansion_for_given_temperature():
    # Arrange
    thermal_expansion = "10x10 -6 / ° C for 20C"
    expected_coefficient = "0.00001;20"

    # Act
    coefficient = get_coefficient_of_expansion(thermal_expansion, [])

    # Assert
    assert coefficient == expected_coefficient


def test_extract_linear_coefficient_of_expansion_with_decimal_base_value():
    # Arrange
    thermal_expansion = "10.5 x 10-6/°C"
    expected_coefficient = "0.0000105"

    # Act
    coefficient = get_coefficient_of_expansion(thermal_expansion, [])

    # Assert
    assert coefficient == expected_coefficient
