# -*- coding: utf-8 -*-

""" this script cleans the country-continent data and saves into a csv file.

input: the country-continent excel file (by Vincent Larivière).

output: a csv file with country and continent columns.

"""
import sys

import pandas as pd


def clean_data(in_file, out_file):
    """ this function select two columns (country and continent), remove
    missing values
    """
    geo_df = pd.read_excel(in_file)
    geo_df = geo_df[['ERegroupement', 'Econtinent_2']]
    geo_df.rename(index=str, inplace=True,
                  columns={'ERegroupement': 'COUNTRY',
                           'Econtinent_2': 'CONTINENT'})

    geo_df.dropna(inplace=True)
    geo_df.drop_duplicates(inplace=True)
    geo_df.iloc[0].CONTINENT = 'Asia'
    geo_df.to_csv(out_file, index=False)


if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    OUT_FILE = sys.argv[2]

    clean_data(IN_FILE, OUT_FILE)
