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

def read_schedule(file):
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
            data = []
            res = []
            i = 0
            for line in lines:
                data.append(clear_file_string(line))
            prs = [r for r in data if r not in ['',"  "]]
            while i < len(prs):
                if prs[i] == "WEFAC":
                    while not prs[i] in ["DATES", "COMPDAT", "COMPDATL", "END"]:
                        i = i + 1
                res.append(prs[i])
                i = i + 1
    return res

def clear_file_string(line):
    char_set = set("!@#%&()[]{}/?<>")
    output_string = ""
    line = line[:line.find('-')]
    for i in range(0, len(line)):
        if not line[i] in char_set:
            output_string += line[i]
    return output_string


def parse_keyword_DATE_line(current_date_line: str):
    char_set = set("!@#%&()[]{}/?<>'")
    output_string = ""
    current_date_line = current_date_line[:current_date_line.find('-')]
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

def parse_schedule(list: list, keywords):
    output = []
    i = 0
    while i < len(list):

        if list[i] == "END":
            break

        if list[i] == "COMPDAT":
            i = i + 1

            while not list[i] in keywords:
                res = [np.nan]
                res.extend(parse_keyword_COMPDAT_line(list[i]))
                output.append(res)
                i = i + 1

        if list[i] == "COMPDATL":
            i = i + 1

            while not list[i] in keywords:
                res = [np.nan]
                res.extend(parse_keyword_COMPDATL_line(list[i]))
                output.append(res)
                i = i + 1

        if list[i] == "DATES":
            i = i + 1

            while not list[i+1] in ["COMPDAT","COMPDATL"]:
                if list[i+1] == "DATES":
                    res = [parse_keyword_DATE_line(list[i]), np.nan]
                    output.append(res)
                    i = i + 2
                elif list[i+1] == "END":
                    res = [parse_keyword_DATE_line(list[i]), np.nan]
                    output.append(res)
                    break
                else:
                    res = [parse_keyword_DATE_line(list[i]), np.nan]
                    output.append(res)
                    i = i + 1

            date = parse_keyword_DATE_line(list[i])
            i = i + 1

            while list[i] != "DATES":
                if list[i] == "COMPDAT":
                    i = i + 1

                    while not list[i] in keywords:
                        res = [date]
                        res.extend(parse_keyword_COMPDAT_line(list[i]))
                        output.append(res)
                        i = i + 1

                if list[i] == "COMPDATL":
                    i = i + 1

                    while not list[i] in keywords:
                        res = [date]
                        res.extend(parse_keyword_COMPDATL_line(list[i]))
                        output.append(res)
                        i = i + 1

                if list[i] == "END":
                    break

    return output

def extract_keywords_blocks():
    return 1
def extract_lines_from_keyword_block():
    return 1
def parse_keyword_block():
    return 1

