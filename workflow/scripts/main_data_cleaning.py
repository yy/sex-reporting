# -*- coding: utf-8 -*-

""" this script cleans the main dataset and saves into a csv file.

input:
    - the publication dataset (by Vincent Larivière).
    - the continent dataset (by Vincent Larivière).

output:
    - a csv file with country and continent columns.

"""
import sys
import logging

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def load_data(in_file):
    """ returns a pandas dataframe of the raw dataset. """
    dtypes = {'id_Art': 'int',
              'Year': 'int',
              'Main_country': 'category',
              'nb_AUTEUR': 'int',
              'NB_ADRESSE': 'int',
              'nb_REFERENCE': 'int',
              'FI_2': 'float',
              'CIT_ALL_IAC': 'int',
              'GENDER_TOPIC': 'category',
              'gender_First': 'category',
              'gender_Last': 'category',
              'fracF': 'float',
              'FractM': 'float',
              'Ediscipline': 'category',
              'ESpecialite': 'category'}
    return pd.read_csv(in_file, sep='\t', dtype=dtypes)


def load_country_data(main_country_data_file, added_country_data_file):
    """ load the country data (raw and added) and returns a dataframe """
    return pd.concat([pd.read_csv(main_country_data_file),
                      pd.read_csv(added_country_data_file)])


def merge_pubdata_with_country_data(pub_df, cntry_df):
    """ merge the publication table and country table """
    return pd.merge(pub_df, cntry_df, left_on='MAIN_COUNTRY',
                    right_on='COUNTRY', how='left')


def rename_df(pub_df):
    """ renaming columns with uppercase style """
    rename_dic = {'id_Art': 'PID',
                  'Year': 'YEAR',
                  'Main_country': 'MAIN_COUNTRY',
                  'nb_AUTEUR': 'N_AUTHORS',
                  'NB_ADRESSE': 'N_ADDRESSES',
                  'nb_REFERENCE': 'N_REFS',
                  'rEVUE': 'VENUE',
                  'FI_2': 'IF',
                  'CIT_ALL_IAC': 'N_CITATIONS',
                  'gender_First': 'GENDER_FIRST',
                  'gender_Last': 'GENDER_LAST',
                  'fractF': 'FEMALE_FRACTION',
                  'FractM': 'MALE_FRACTION',
                  'Ediscipline': 'DISCIPLINE',
                  'ESpecialite': 'SUBDISCIPLINE'}
    return pub_df.rename(index=str, columns=rename_dic, inplace=False)


def clean_gender_var(pub_df):
    """ cleaning gender variable """
    gender_replace_dic = {'INI': np.nan, 'UNK': np.nan, 'UNI': np.nan,
                          'uni': np.nan, 'unk': np.nan, 'm': 'M', 'f': 'F'}
    return pub_df.replace({
        'GENDER_FIRST': gender_replace_dic,
        'GENDER_LAST': gender_replace_dic})


def drop_unk_gender(pub_df):
    """ drop the rows with unknown gender """
    return pub_df.dropna(subset=['GENDER_FIRST', 'GENDER_LAST', 'GENDER_TOPIC'])


def sanity_checks(cleaned_df):
    """ impact factor may still contain NaN """
    assert len(cleaned_df) == 2106521
    assert all(cleaned_df[cleaned_df.N_AUTHORS == 1].GENDER_FIRST ==
               cleaned_df[cleaned_df.N_AUTHORS == 1].GENDER_LAST)
    assert cleaned_df.DISCIPLINE.isnull().sum() == 0
    assert cleaned_df.SUBDISCIPLINE.isnull().sum() == 0
    assert cleaned_df.N_CITATIONS.isnull().sum() == 0
    assert cleaned_df.N_AUTHORS.isnull().sum() == 0
    assert cleaned_df.N_ADDRESSES.isnull().sum() == 0
    assert cleaned_df.N_REFS.isnull().sum() == 0


def save_single_author_pubs(cleaned_df, out_file):
    """ single author table """
    cleaned_df[cleaned_df.N_AUTHORS == 1].to_csv(out_file, index=False)


def save_multi_author_pubs(cleaned_df, out_file):
    """ multi-author paper table """
    cleaned_df[cleaned_df.N_AUTHORS > 1].to_csv(out_file, index=False)


if __name__ == "__main__":
    PUB_DATA_FILE = sys.argv[1]
    COUNTRY_DATA_FILE = sys.argv[2]
    COUNTRY_ADDED_DATA_FILE = sys.argv[3]
    SINGLE_AUTHOR_OUT_FILE = sys.argv[4]
    MULTI_AUTHOR_OUT_FILE = sys.argv[5]

    COUNTRY_DF = load_country_data(COUNTRY_DATA_FILE, COUNTRY_ADDED_DATA_FILE)
    RAW_PUB_DF = load_data(PUB_DATA_FILE)
    RENAMED_PUB_DF = rename_df(RAW_PUB_DF)
    MERGED_DF = merge_pubdata_with_country_data(RENAMED_PUB_DF, COUNTRY_DF)
    DF = drop_unk_gender(clean_gender_var(MERGED_DF))
    sanity_checks(DF)

    save_single_author_pubs(DF, SINGLE_AUTHOR_OUT_FILE)
    save_multi_author_pubs(DF, MULTI_AUTHOR_OUT_FILE)
