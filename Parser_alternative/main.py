from lib import parser
import re
if __name__ == '__main__':
    keywords = ("DATES","COMPDAT","COMPDATL", "END")
    parameters = ""
    input_file = 'input data/test_schedule.inc'
    output_file = 'output data/schedule.csv'

data = parser.read_schedule(input_file)
print(parser.parse_schedule(data,keywords))

i=1
