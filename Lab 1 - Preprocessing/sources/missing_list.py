import math
import sys
import numpy as np
import pandas as pd

if __name__ == '__main__':
    """
        Argument from command line. To run: 'python missing_list.py data_file_name.csv'
        Where data_file_name is the name of .csv file
    """
    if len(sys.argv) < 2:
        print('To run: "python missing_list.py data_file_name.csv"')
    else:
        input_file_name = str(sys.argv[1])
        data = pd.read_csv(input_file_name)
        attributes = list(data)
        missing_attr =[]
        for index, row in data.iterrows():
            for attr in attributes:
                if pd.isna(row[attr]) and attr not in missing_attr:
                    missing_attr.append(attr)
        
        print(f'There a {len(missing_attr)} missing attributes!')
        print(', '.join(missing_attr))