from lib import parser
if __name__ == '__main__':
    keywords = ("DATES","COMPDAT","COMPDATL")
    parameters = ""
    input_file = 'input data/test_schedule.inc'
    output_file = 'output data/schedule.csv'

    schedule.df=parser.transform_schedule(keywords,parameters,input_file,output_file)