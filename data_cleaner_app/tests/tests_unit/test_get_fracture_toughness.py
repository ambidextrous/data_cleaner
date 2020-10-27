from data_cleaner_app.normalization.toughness_normalization import (
    get_fracture_toughness,
)


def test_extract_fracture_toughness_with_range_and_alternate_symbol():
    # Arrange
    given_fracture_toughness = "6.5 to 8 MPam1/2"
    expected_fracture_toughness = "6.5,8"

    # Act
    returned_fracture_toughness = get_fracture_toughness(given_fracture_toughness, [])

    # Assert
    assert returned_fracture_toughness == expected_fracture_toughness


def test_extract_fracture_toughness_with_temperature_association():
    # Arrange
    given_fracture_toughness = ">6.04@23C"
    expected_fracture_toughness = "6.04;23"

    # Act
    returned_fracture_toughness = get_fracture_toughness(given_fracture_toughness, [])

    # Assert
    assert returned_fracture_toughness == expected_fracture_toughness
