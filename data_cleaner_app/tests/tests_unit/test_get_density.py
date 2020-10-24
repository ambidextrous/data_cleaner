from pytest import raises

from data_cleaner_app.normalizers.density_normalizer import get_density


def test_normalize_density_with_correct_units():
    # Arrange
    given_density = "5.68 g/cc"
    expected_density = "5.68"

    # Act
    returned_density = get_density(given_density)

    # Assert
    assert returned_density == expected_density


def test_normalize_density_with_incorrect_units():
    # Arrange
    given_density = "5.68 not a unit"
    expected_density = "5.68"

    # Act & Assert
    with raises(ValueError):
        get_density(given_density)


def test_normalize_density_with_alternate_units():
    # Arrange
    given_density = "5.0008 KG/m3"
    expected_density = "0.0050008"

    # Act
    returned_density = get_density(given_density)

    # Assert
    assert returned_density == expected_density


def test_normalize_density_with_temperature_range():
    # Arrange
    given_density = "5.68 g/cc @100°F"
    expected_density = "5.68;37.77777777777778"

    # Act
    returned_density = get_density(given_density)

    # Assert
    assert returned_density == expected_density
