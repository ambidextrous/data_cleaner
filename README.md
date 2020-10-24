Overview:
You’ll find below is a small and simple assignment to help us understand how you work.
There are two core parts: completing the programming task and then presenting / reviewing
your approach.
The Programming Task:
Please implement a simple software that transitions the "unclean" data sample to a "clean"
format. Project Requirements:
● Use of python
● Give the possibility to choose from multiple clean output formats: csv, json, xlsx
● Unit tests
Data Sample:
Provided in the link are the following sets of data
(https://docs.google.com/spreadsheets/d/18zvhJFtWxIKuX15-Hbq24yP9k1UeYPKL7h6YV1hn5
ak/edit?usp=sharing):
● Sheet “Ceramic_Raw_Data”: contains some “unclean” data.
● Sheet “material_property_map”: some information that should be mapped to the clean
data.
● Sheet “material_data_result”: Some ideal end result.
Data cleaning:
● Strip the values of any additional characters. Multiple values / ranged values should be
joined with a comma (“,”) separator. Temperature association with values should be
joined with semicolon (“;”).
○ 2.5 to 3 W/mK - > 2.5,3
○ >6.04@20C -> 6.04;23
● Map material property names.
● Unit conversion where needed.
Submission:
Feel free to send a link to a github repository or email the python files you put together.