# -*- coding: utf-8 -*-

""" this script merge the paper mesh features to multi author data. 

input:
    - multi-author data
    - paper mesh feature data

output:
    multi author data with mesh, country, and subdiscipline covariates

"""
import sys
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def cal_f_cov(df, cov_col):
    tempdf = df.copy()
    for pos in ['FIRST', 'LAST']:
        logging.info(f'{cov_col} w GENDER_{pos}')
        tempdf[f'GENDER_{pos}'].replace(dict(M=0, F=1), inplace=True)
        f_dict = tempdf.groupby(cov_col)[f'GENDER_{pos}'].mean().to_dict()
        df[f'F_{pos}_{cov_col}'] = tempdf[cov_col].replace(f_dict)
    return df


def attach_f_country(df):
    ''' calculate f_first_country and f_last_country '''
    return cal_f_cov(df, 'MAIN_COUNTRY')


def main(multi_author_f, paper_mesh_feature_f, out_f):
    """ merge multi author df with paper mesh feature df w left join on PID """

    multi_df = pd.read_csv(multi_author_f)
    logging.info('multi author data loaded.')

    mesh_df = pd.read_csv(paper_mesh_feature_f, sep='\t')
    logging.info('paper mesh feature loaded.')

    df = pd.merge(multi_df, mesh_df, on='PID', how='left')
    df = attach_f_country(df)

    df.to_csv(out_f, index=False)


if __name__ == "__main__":
    MULTI_AUTHOR_DATA = sys.argv[1]
    PAPER_MESH_FEATURE_DATA = sys.argv[2]
    OUT_PATH = sys.argv[3]
    main(MULTI_AUTHOR_DATA, PAPER_MESH_FEATURE_DATA, OUT_PATH)
