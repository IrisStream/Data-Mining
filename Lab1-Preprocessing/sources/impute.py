import sys, getopt
import numpy as np
import pandas as pd
import argparse
from pandas.api.types import is_string_dtype

def compute_mean(data, col):                    
    print('compute mean')
    count_instances = 0
    sum_instances = 0.0
    if(is_string_dtype(data[col])):             #can not use median for non-numeric column
            print(f"Invalid column: {col}")
            return
    for cell in data[col]:
        if(pd.isna(cell)):
            continue
        count_instances += 1
        sum_instances += cell
    return sum_instances / count_instances

def compute_median(data, col):
    print('compute median')
    pool = []
    if(is_string_dtype(data[col])):              #can not use median for non-numeric column
            print(f"Invalid column: {col}")
            return
    for cell in data[col]:
        if(pd.isna(cell)):
            continue
        pool.append(cell)
    pool_len = len(pool)
    pool.sort()
    if(pool_len % 2 == 0):
        return (pool[(pool_len - 1) // 2] + pool[pool_len // 2]) / 2
    else:
        return pool[pool_len // 2]

def compute_mode(data, col):
    print('compute mode')
    hash_table = dict()
    if(is_string_dtype(data[col]) == False):             #can not use mode for numeric column
            print(f"Invalid column: {col}")
            return
    for cell in data[col]:
        if(pd.isna(cell)):
            continue
        if(cell not in hash_table):
            hash_table[cell] = 1
        else:
            hash_table[cell] += 1
    mode = None
    for key in hash_table:
        if mode == None or hash_table[mode] < hash_table[key]:
            mode = key
    return mode

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


if __name__ == '__main__':
    """
        Argument from command line. To run: 'python impute.py --input input_file_name.csv --method method_name --columns col1 col2 ... --output output_file_name.csv'
        Where input_file_name is the name of input data file
              method_name must in ['mean', 'median', 'mode']
              col1 col2 ... is the label of the column in data file
              output_file_name is the name of output data file
    """

    inputfile, method, columns, outputfile = arg_parser()
#   inputfile = 'house-prices.csv'
#   method = 'mode'
#   columns =['Alley']
#   outputfile = 'hihi-prices.csv'

    data = pd.read_csv(inputfile)
    md = None
    if method == 'mean':
        md = compute_mean
    elif method == 'median':
        md = compute_median
    elif method == 'mode':
        md = compute_mode

    for col in columns:
        value = md(data, col)
        for index, row in data.iterrows():
            if(pd.isna(row[col])):
                data.at[index, col] = value
    data.to_csv(outputfile)