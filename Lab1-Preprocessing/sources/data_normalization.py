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
        "-m",
        "--method",
    )
    CLI.add_argument(
        "-c",
        "--columns",
        nargs="*"
    )
    CLI.add_argument(
        "-o",
        "--output",
    )
    args = CLI.parse_args()
    return args.input, args.method, args.columns, args.output

newMin = 0.0
newMax = 0.0
def compute_min_max(data, col):             #Compute min and max value for min-max Normalization
    print(f"--Enter new min and new max for {col}--")
    global newMax
    global newMin
    newMin = float(input("Enter new min value: "))
    newMax = float(input("Enter new max value: "))
    curMin = None
    curMax = None
    for cell in data[col]:
        if(pd.isna(cell)):
            continue
        if(curMin == None or curMin > cell):
            curMin = cell
        if(curMax == None or curMax < cell):
            curMax = cell
    return float(curMin), float(curMax), normalize_min_max

def compute_mean_stdDev(data, col):         #Compute mean and standard Deviation for z-score Normalization
    count_instances = 0                     #Count number of instances
    sum_instances = 0                       #Sum of instances in this column
    for cell in data[col]:
        if(pd.isna(cell)):                  #NaN value doesn't count
            continue
        count_instances += 1
        sum_instances += cell
    
    mean = sum_instances / count_instances          #Compute mean 
    stdDev = 0
    for cel in data[col]:
        if(pd.isna(cell)):
            continue
        stdDev += (cell - mean) * (cell - mean)
    stdDev = math.sqrt(stdDev / count_instances)    #Compute standard Deviation
    return mean, stdDev, normalize_z_score

def normalize_min_max(value, curMin, curMax):             #Normalize with min-max Normalization
    return ((value - curMin) / (curMax - curMin)) * (newMax - newMin) + newMin

def normalize_z_score(value, mean, stdDev):         #Normalize with z-score Normalization
    return (value - mean) / stdDev

if __name__ == '__main__':
    """
        Argument from command line. To run: 'python data_normalization.py --input input_file_name.csv --method=method_name --columes col1 col2 ... --output output_file_name.csv'
        Where input_file_name is the name of input data file
              method_name must in ['min-max', 'z-score']
              col1 col2 ... is the label of the column in data file
              output_file_name is the name of output data file
    """

    inputfile, method, columns, outputfile = arg_parser()
    data = pd.read_csv(inputfile)
    attributes = list(data)
    md = None
    if method == 'min-max':
        md = compute_min_max
    elif method == 'z-score':
        md = compute_mean_stdDev

    normalizable_cols = dict()                      #List of value of valid columns
    for col in columns:
        if(is_string_dtype(data[col])):             #We can't normalize non-numeric column
            print(f"Invalid column: {col}")
            continue
        else:
            normalizable_cols[col] = []
        x, y, normalize = md(data, col)             #x,y may be min, max(min-max normalization)
                                                    #           mean, standard deciation(in z-score normalization)
        for index, row in data.iterrows():
            if(pd.isna(row[col]) == False):         #We don't calculate in missing value
                normalizable_cols[col].append(normalize(row[col], x, y))
            else:
                normalizable_cols[col].append("")
    
    f = open(outputfile, 'w')
    f.write(','.join(attr for attr in attributes) + '\n')   #Write columns label to output file

    for index, row in data.iterrows():
        new_line = []
        for attr in attributes:                             #cast row to list for write into output file
            if(attr in normalizable_cols):                  #New value for normalizabel columns
                new_line.append(normalizable_cols[attr][index])
            else:
                new_line.append(row[attr])
        f.write(','.join(str(cell) for cell in new_line) + '\n')    #Write to file
    f.close()