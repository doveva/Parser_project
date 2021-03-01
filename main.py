from lib import parser
import re
if __name__ == '__main__':
    keywords = ("DATES","COMPDAT","COMPDATL")
    parameters = ""
    input_file = 'input data/test_schedule.inc'
    output_file = 'output data/schedule.csv'


print(parser.parse_keyword_COMPDATL_line("'W4' 40 30  1   3 	OPEN 	1* 	1 	2 	1 	3* 			4.0 /"))
