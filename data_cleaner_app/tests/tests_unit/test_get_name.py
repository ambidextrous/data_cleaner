from data_cleaner_app.normalization.name_normalization import get_name


def test_normalize_correct_name():
    # Arrange
    given_name = "Zirconium Oxide"
    expected_name = "Zirconium Oxide"

    # Act
    returned_name = get_name(given_name, "Zirconium Oxide")

    # Assert
    assert returned_name == expected_name


def test_normalize_name_with_missformatted_formula():
    # Arrange
    given_name = "Zirconium Oxide (ZrO 2 )"
    expected_name = "Zirconium Oxide"

    # Act
    returned_name = get_name(given_name, "Zirconium Oxide")

    # Assert
    assert returned_name == expected_name


def test_normalize_name_with_multiple_names():
    # Arrange
    given_name = "Zirconium Oxide, Zirconia, ZrO2"
    expected_name = "Zirconium Oxide"

    # Act
    returned_name = get_name(given_name, "Zirconium Oxide")

    # Assert
    assert returned_name == expected_name


def test_normalize_name_formula_and_no_known_name():
    # Arrange
    given_name = "ZrO2 Y-PSZ"
    expected_name = "ZrO2 Y-PSZ"

    # Act
    returned_name = get_name(given_name, "Zirconium Oxide")

    # Assert
    assert returned_name == expected_name
