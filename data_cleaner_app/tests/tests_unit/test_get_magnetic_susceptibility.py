from data_cleaner_app.normalizers.magenetic_susceptibility_normalizer import (
    get_magnetic_susceptibility,
)


def test_normalize_magnetic_susceptibility():
    # Arrange
    given_magnetic_susceptibility = "-0.0000138"
    expected_magnetic_susceptibility = "-0.0000138"

    # Act
    returned_magnetic_susceptibility = get_magnetic_susceptibility(
        given_magnetic_susceptibility
    )

    # Assert
    assert returned_magnetic_susceptibility == expected_magnetic_susceptibility
