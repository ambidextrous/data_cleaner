from data_cleaner_app.normalizers.density_normalizer import get_density


def test_normalize_density_with_correct_units():
    # Arrange
    given_thermal_conductivity = "5.68 g/cc"
    expected_thermal_conductity = "5.68"

    # Act
    returned_thermal_conductivity = get_thermal_conductivity(given_thermal_conductivity)

    # Assert
    assert returned_thermal_conductivity == expected_thermal_conductity
