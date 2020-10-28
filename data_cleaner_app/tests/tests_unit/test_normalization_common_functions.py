#from data_cleaner_app.normalization.common import get_temperature
#
#
#class TestTemperature:
#    def test_get_temperature_celcius(self):
#        # Arrange
#        string_with_temp = "1.675 W/m-K @ 25°C"
#        expected_temp = ";25.0"
#
#        # Act
#        returned_temp = get_temperature(string_with_temp)
#
#        # Assert
#        assert returned_temp == expected_temp
#
#    def test_get_temperature_fahrenheit(self):
#        # Arrange
#        string_with_temp = "1.675 W/m-K for 25°F"
#        expected_temp = ";-3.888888888888889"
#
#        # Act
#        returned_temp = get_temperature(string_with_temp)
#
#        # Assert
#        assert returned_temp == expected_temp
#
#    def test_get_negative_temperature_in_celcius(self):
#        # Arrange
#        string_with_temp = "1.675 W/m-K @ -25"
#        expected_temp = ";-25.0"
#
#        # Act
#        returned_temp = get_temperature(string_with_temp)
#
#        # Assert
#        assert returned_temp == expected_temp
#