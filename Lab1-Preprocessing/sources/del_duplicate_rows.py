import sys, getopt
import numpy as np
import pandas as pd
import argparse

def arg_parser():                       #Use argparse to simplify command line arguments process
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


if __name__ == '__main__':
    """
        Argument from command line. To run: 'python del_missing_cols.py --input input_file_name.csv -missing-rate 0.x -output output_file_name.csv'
        Where input_file_name is the name of input data file
              0.x is a number 0 <= 0.x <= 1 that we will remove all row have missing-rate >= 0.x
              output_file_name is the name of output data file
    """
    
    inputfile, outputfile = arg_parser()
    data = pd.read_csv(inputfile)
    attributes = list(data)     #List of attibutes label of dataframe
    hashtable = dict()          #this dict if 1 instance've existed yet?
    f = open(outputfile, 'w')
    f.write(','.join(str(attr) for attr in attributes) + '\n')  #Write attributes label to  output file
    for index, row in data.iterrows():
        key = ','.join(str(row[attr]) for attr in attributes)   #Cast a row to a str(use for hashtable)
        if(key not in hashtable):                               #If this row hasn't existed
            hashtable[temp] = 1                                     #Mark it has existed, otherwise just skip
            new_line = []                                       #Cast row to a list for write into csv file
            for attr in attributes:
                if(pd.isna(row[attr])):
                    new_line.append('')
                else:
                    new_line.append(str(row[attr]))
            f.write(','.join(cell for cell in new_line) + '\n') #Write this row to output file
    f.close()