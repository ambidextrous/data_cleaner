from data_cleaner_app.normalization.metling_normalization import get_metling_point


class TestTemperature:
    def test_get_melting_point_range_celcius(self):
        # Arrange
        string_with_melting_point = "2681 - 2847 °C"
        expected_melting_point = "2681,2847"

        # Act
        returned_melting_point = get_metling_point(string_with_melting_point, [])

        # Assert
        assert returned_melting_point == expected_melting_point

    def test_get_metling_point_fahrenheit(self):
        # Arrange
        string_with_melting_point = "4,919° F"
        expected_melting_point = "2715"

        # Act
        returned_melting_point = get_metling_point(string_with_melting_point, [])

        # Assert
        assert returned_melting_point == expected_melting_point
