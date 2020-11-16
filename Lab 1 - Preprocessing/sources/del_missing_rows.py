import sys, getopt
import numpy as np
import pandas as pd
import argparse

def arg_parser():
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "-i",
        "--input"
    )
    CLI.add_argument(
        "-m",
        "--missingrate",
    )
    CLI.add_argument(
        "-o",
        "--output",
    )
    args = CLI.parse_args()
    return args.input, args.missingrate, args.output


if __name__ == '__main__':
    """
        Argument from command line. To run: 'python del_missing_rows.py --input input_file_name.csv -missing-rate 0.x -output output_file_name.csv'
        Where input_file_name is the name of input data file
              0.x is a number 0 <= 0.x <= 1 that we will remove all row have missing-rate >= 0.x
              output_file_name is the name of output data file
    """
    
    inputfile, missing_rate, outputfile = arg_parser()
    missing_rate = float(missing_rate)
    data = pd.read_csv(inputfile)
    c=0
    attributes = list(data)
    for index, row in data.iterrows():                              #count rows
        c += 1
    print(f'There are {c} rows before deleting')
    f = open(outputfile, 'w')
    f.write(','.join(str(attr) for attr in attributes) + '\n')
    for index, row in data.iterrows():
        count = 0
        new_line =[]
        for attr in attributes:
            if pd.isna(row[attr]):
                count += 1
                new_line.append('')
            else:
                new_line.append(str(row[attr]))
        if count/len(attributes) < missing_rate:
            f.write(','.join(str(x) for x in new_line) + '\n')
    
    f.close()

    data = pd.read_csv(outputfile)                                   #Count rows after delete
    c=0
    attributes = list(data)
    for index, row in data.iterrows():
        c += 1
    print(f'There are {c} rows after deleting')