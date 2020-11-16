import sys, getopt
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
import argparse
import math

def arg_parser():
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "-i",
        "--input"
    )
    CLI.add_argument(
        "-hi",
        "--hiearchies",
        nargs="*"
    )
    CLI.add_argument(
        "-o",
        "--output"
    )
    args = CLI.parse_args()
    return args.input, args.hiearchies, args.output

def to_nominal(value, group):   #Set label for value
    for value_range in group:
        if (value_range[0] == group[-1][0]) or (value_range[1] < value and value <= value_range[2]):
            return value_range[0]

def init(hiearchies_file, columns, group):
    f = open(hiearchies_file, 'r')
    col = f.readline()[:-1]
    if col in columns:
        return
    columns.append(col)
    group[col] = []
    while True:
        label = f.readline()[:-1]
        if(label == '.'):
            break
        lower_bound = float(f.readline()[:-1])
        upper_bound = float(f.readline()[:-1])
        group[col].append((label, lower_bound, upper_bound))
    f.close()

if __name__ == '__main__':
    """
        Argument from command line. To run: 'python data_normalization.py --input input_file_name.csv --method=method_name --columes col1 col2 ... --output output_file_name.csv'
        Where input_file_name is the name of input data file
              col1 col2 ... is the label of the column in data file
              output_file_name is the name of output data file
    """

    inputfile, hiearchies, outputfile = arg_parser()
    data = pd.read_csv(inputfile)
    columns = []
    group = dict()
    for hiearchies_file in hiearchies:
        init(hiearchies_file, columns, group)
    attributes = list(data)

    nominal_cols = dict()                      #List of value of valid columns
    for col in columns:
        if(is_string_dtype(data[col])):             #We can't normalize non-numeric column
            print(f"Invalid column: {col}")
            continue
        else:
            nominal_cols[col] = []
        for index, row in data.iterrows():
            if(pd.isna(row[col]) == False):         #We don't calculate in missing value
                nominal_cols[col].append(to_nominal(row[col], group[col]))
            else:
                nominal_cols[col].append("")
    
    f = open(outputfile, 'w')
    f.write(','.join(attr for attr in attributes) + '\n')   #Write columns label to output file
 
    for index, row in data.iterrows():
        new_line = []
        for attr in attributes:                             #cast row to list for write into output file
            if(attr in nominal_cols):                  #New value for normalizabel columns
                new_line.append(nominal_cols[attr][index])
            else:
                new_line.append(row[attr])
        f.write(','.join(str(cell) for cell in new_line) + '\n')    #Write to file
    f.close()