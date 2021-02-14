import numpy
import re
import pandas
import os

def transform_schedule (keywords,parameters,input_file,output_file):
    """
    reads an input file and return .csv file
    :param keywords
    :param parameters
    :param input_file
    :param output_file
    :return:
    """
    return

def read_schedule():
    file = '../input data/test_schedule.inc'
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            lines = f.readlines()
            print(lines)
            f.close()
    return lines

def parse_keyword_DATE_line(current_date_line: str):
    char_set = set("!@#%&*()[]{}/?<>")
    output_string = ""
    for i in range(0, len(current_date_line)):
        if not current_date_line[i] in char_set:
            output_string += current_date_line[i]
    parse_data = " ".join(output_string.split())
    return parse_data

def parse_keyword_COMPDAT_line(well_comp_line: str):
    char_set = set("!@#%&*()[]{}/?<>")
    output_string = ""
    well_comp_line = well_comp_line[:well_comp_line.find('-')]
    for i in range(0, len(well_comp_line)):
        if not well_comp_line[i] in char_set:
            output_string +=  well_comp_line[i]
    parse_data = output_string.split()
    return parse_data

def inspect_schedule():

def clean_schedule():

def parse_schedule():

def extract_keywords_blocks():

def extract_lines_from_keyword_block():

def parse_keyword_block():


