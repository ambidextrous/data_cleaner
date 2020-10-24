from pytest import raises

from data_cleaner_app.normalizers.base_material_normalizer import (
    get_base_material_from_name,
)


def test_extract_base_material_from_name_easy_case():
    # Arrange
    name = "Zirconium Oxide"
    expected_base_material = "Zirconium Oxide"

    # Act
    base_material = get_base_material_from_name(name)

    # Assert
    assert base_material == expected_base_material


def test_extract_base_material_not_found():
    # Arrange
    name = "Not a material"
    expected_base_material = "Zirconium Oxide"

    # Act & Assert
    with raises(ValueError):
        get_base_material_from_name(name)


def test_extract_base_material_not_found():
    # Arrange
    name = "Zirconium (Cu)"
    expected_base_material = "Zirconium Oxide"

    # Act & Assert
    with raises(ValueError):
        get_base_material_from_name(name)


def test_extract_base_material_from_name_null_cases():
    # Arrange
    name = None

    # Act & Assert
    with raises(ValueError):
        get_base_material_from_name(name)


def test_extract_base_material_from_name_with_irregular_capitalization():
    # Arrange
    name = "ZirCONium oxide"
    expected_base_material = "Zirconium Oxide"

    # Act
    base_material = get_base_material_from_name(name)

    # Assert
    assert base_material == expected_base_material


def test_extract_base_material_from_name_with_irregular_formula_spacing():
    # Arrange
    name = "Zirconium Oxide (ZrO 2 )"
    expected_base_material = "Zirconium Oxide"

    # Act
    base_material = get_base_material_from_name(name)

    # Assert
    assert base_material == expected_base_material


def test_extract_base_material_formula_with_non_standard_name():
    # Arrange
    name = "ZrO2 Y-PSZ"
    expected_base_material = "Zirconium Oxide"

    # Act
    base_material = get_base_material_from_name(name)

    # Assert
    assert base_material == expected_base_material


def test_extract_base_material_with_comma_separated_names():
    # Arrange
    name = "Zirconium Oxide, Zirconia, (ZrO2)"
    expected_base_material = "Zirconium Oxide"

    # Act
    base_material = get_base_material_from_name(name)

    # Assert
    assert base_material == expected_base_material
