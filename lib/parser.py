import numpy as np
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
    char_set = set("!@#%&()[]{}/?<>'")
    output_string = ""
    for i in range(0, len(current_date_line)):
        if not current_date_line[i] in char_set:
            output_string += current_date_line[i]
    parse_data = " ".join(output_string.split())
    return parse_data

def parse_keyword_COMPDAT_line(well_comp_line: str):
    char_set = set("!@#%&()[]{}/?<>'")
    output_string = ""
    well_comp_line = well_comp_line[:well_comp_line.find('-')]
    for i in range(0, len(well_comp_line)):
        if not well_comp_line[i] in char_set:
            output_string +=  well_comp_line[i]
    output_string = default_params_unpacking_in_line(output_string)
    parse_data = output_string.split()
    parse_data.insert(1,np.nan)
    return parse_data

def parse_keyword_COMPDATL_line(well_comp_line: str):
    char_set = set("!@#%&()[]{}/?<>'")
    output_string = ""
    well_comp_line = well_comp_line[:well_comp_line.find('-')]
    for i in range(0, len(well_comp_line)):
        if not well_comp_line[i] in char_set:
            output_string +=  well_comp_line[i]
    output_string = default_params_unpacking_in_line(output_string)
    parse_data = output_string.split()
    return parse_data


def decode(match):
    ch_st = set("*")
    res=""
    for i in range(0, len(str(match.group(0)))):
        if not match.group(0)[i] in ch_st:
            res +=  match.group(0)[i]
    string = ""
    for i in range(0,int(res[0])):
        string += " DEFAULT"
    return str(string)


def default_params_unpacking_in_line(well_comp_line: str):
    output_string = re.sub('([1-9]\*)', decode, well_comp_line)
    output_string = " ".join([el for el in output_string.split(' ') if el.strip()])
    return output_string

def inspect_schedule():
    return 1
def clean_schedule():
    return 1
def parse_schedule():
    return 1
def extract_keywords_blocks():
    return 1
def extract_lines_from_keyword_block():
    return 1
def parse_keyword_block():
    return 1

