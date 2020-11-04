import sys
import numpy as np
import pandas as pd

if __name__ == '__main__':
    """
        Argument from command line. To run: 'python count_missing_row.py data_file_name.csv'
        Where data_file_name is the name of .csv file
    """

    if(len(sys.argv) < 2):
        print('To run: "python count_missing_row.py data_file_name.csv"')
    else:
        input_file_name = sys.argv[1]
        data = pd.read_csv(input_file_name)
        attributes = list(data)
        count = 0
        for index, row in data.iterrows():
            for attr in attributes:
                if(pd.isna(row[attr])):
                    count += 1
                    break
        
        print(f'There are {count} row which missing value')