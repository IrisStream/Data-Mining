import sys
import numpy as np
import pandas as pd 
from pandas.api.types import is_string_dtype
import argparse
import infix

def arg_parser():
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "-i",
        "--input"
    )
    CLI.add_argument(
        "-o",
        "--output",
    )
    args = CLI.parse_args()
    return args.input, args.output

if __name__ == "__main__":
    inputfile, outputfile = arg_parser()
    data = pd.read_csv(inputfile)
    attributes = list(data)
    exp = input("Enter expression: ")               #Expression that we want to calculate

    alter_name = input("Enter new column name: ")   #Name of new column
    if(alter_name == ''):
        attributes.append(' '.join(e for e in expression))
    else:
        attributes.append(alter_name)

    expression = infix.get_expression(exp)          #Raw String to expression for calculate
    use_attributes =[]                              #Label of attributes use in expression
    for x in expression:
        if(len(x) > 1 and x.isnumeric() == False):  #Push all operand that may be an attributes list
            use_attributes.append(x)
    for attr in use_attributes:
        if attr not in attributes or is_string_dtype(data[attr]):   #Check if it's an attribute or not
                                                                    #We also can't calculate of attribute's data type isn't numeric
            print(f"Invalid attributes: {attr}")
            sys.exit()

    f = open(outputfile,'w')
    f.write(','.join(attr for attr in attributes) + '\n')           #Write attributes label
    for index, row in data.iterrows():
        next_line = []
        calculatable = True         
        for i in range(len(attributes) - 1):
            attr = attributes[i]
            next_line.append(str(row[attr]))
            if(attr in use_attributes and pd.isna(row[attr])):
                calculatable = False            #If there're a missing value, we don't calculate that row
        if(calculatable):
            next_line.append(str(infix.calculate(row, expression))) #Calculate expression
        else:
            next_line.append('')                                    #Missing value if we don't calculate
        f.write(','.join(cell for cell in next_line) + '\n')        #Write line to output file
    f.close()