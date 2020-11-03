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
        "--missing_rate",
    )
    CLI.add_argument(
        "-o",
        "--output",
    )
    args = CLI.parse_args()
    return args.input, float(args.missing_rate), args.output

def get_valid_attributes(data, missing_rate):
    attributes = list(data)                         #List of attributes of relation
    count_missing = dict.fromkeys(attributes, 0)    #Store number of missing value of each attributes
    count_instances = 0                             #Count number of instances
    for index, row in data.iterrows():              
        for attr in attributes:
            if pd.isna(row[attr]):
                count_missing[attr] += 1            #Count if missing
        count_instances += 1                        #Count instances
    valid_attributes = []                           #List of attributes that've missing rate valid
    for attr in attributes:
        if(count_missing[attr]/count_instances <= missing_rate):
            valid_attributes.append(attr)
    return valid_attributes

if __name__ == '__main__':
    """
        Argument from command line. To run: 'python del_missing_cols.py --input input_file_name.csv -missing-rate 0.x --output output_file_name.csv'
        Where input_file_name is the name of input data file
              0.x is a number 0 <= 0.x <= 1 that we will remove all row have missing-rate >= 0.x
              output_file_name is the name of output data file
    """
    
    inputfile, missing_rate, outputfile = arg_parser()
    data = pd.read_csv(inputfile)                       #read data from inputfile
    
    valid_attributes = get_valid_attributes(data, missing_rate)

    f = open(outputfile, 'w')
    f.write(','.join(str(attr) for attr in valid_attributes) + '\n')    #Write attributes label
    for index, row in data.iterrows():
        f.write(','.join(str(row[attr]) for attr in valid_attributes) + '\n')   #Write row
    f.close()