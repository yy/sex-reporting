#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This script prepares the regression table.

input: multi-author data

output: regression table with all variables

"""

import sys
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def remove_comma_in_subdiscipline(df):
    """ remove comma because it creates issues with statsmodels export """
    df.SUBDISCIPLINE.replace('Social Sciences, Biomedical',
                             'Biomedical Social Sciences', inplace=True)
    return df


def set_pivot(df):
    """ set the pivot (reference) variables """
    df.GENDER_TOPIC.replace('N', 'A', inplace=True)
    df.GENDER_FIRST.replace('M', 'A', inplace=True)
    df.GENDER_LAST.replace('M', 'A', inplace=True)
    df.CONTINENT.replace('Northern America', 'AA', inplace=True)
    return df


def set_first_last_gender_var(df):
    ''' create a varialbe for first + last author's gender '''
    df['GENDER_FL'] = df.GENDER_FIRST + df.GENDER_LAST
    return df


def add_combined_covariates(df):
    df['F_MESH'] = (df['F_FIRST_MESH'] + df['F_LAST_MESH']) / 2.0
    df['F_COUNTRY'] = (df['F_FIRST_MAIN_COUNTRY'] +
                       df['F_LAST_MAIN_COUNTRY']) / 2.0
    return df


def add_dep_vars(df):
    ''' adding SR, SR_M, SR_F, and SR_B variables '''
    df['SRA'] = df.GENDER_TOPIC.replace(dict(A=0, B=1, M=1, F=1),
                                        inplace=False)
    df['SRM'] = df.GENDER_TOPIC.replace(dict(A=0, B=1, M=1, F=0),
                                        inplace=False)
    df['SRF'] = df.GENDER_TOPIC.replace(dict(A=0, B=1, M=0, F=1),
                                        inplace=False)
    df['SRB'] = df.GENDER_TOPIC.replace(dict(A=0, B=1, M=0, F=0),
                                        inplace=False)
    return df


def pre_process(df):
    ''' pre-processing the data '''
    df = remove_comma_in_subdiscipline(df)
    logging.info('a comma from the subdiscipline variable removed.')

    df = set_pivot(df)
    logging.info('pivot variables are set up.')

    df = set_first_last_gender_var(df)
    logging.info('first + last author gender variable generated.')

    df = add_combined_covariates(df)
    logging.info('combined covariates generated.')

    df = add_dep_vars(df)
    logging.info('dependent variables are added.')

    logging.info('# of rows without mesh var: {}'.format(
        df.F_FIRST_MESH.isna().sum()))
    logging.info('# of rows with mesh var: {}'.format(
        len(df) - df.F_FIRST_MESH.isna().sum()))

    return df


def main(data_f, reg_table_f):
    """ run regressions and write the results """
    df = pd.read_csv(data_f)
    logging.info('data loaded (N = {}).'.format(len(df)))

    df = pre_process(df)
    logging.info('data processed')

    df.to_csv(reg_table_f, index=False)


if __name__ == "__main__":
    MULTI_AUTHOR_DATA = sys.argv[1]
    REG_TABLE = sys.argv[2]
    main(MULTI_AUTHOR_DATA, REG_TABLE)
