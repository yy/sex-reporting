#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This script runs the main models.

input: multi-author data

output: tables and figures.

"""

import sys
import logging

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BR = 'Biomedical Research'
CM = 'Clinical Medicine'
HE = 'Health'


def run_model(model):
    """ run a model based on the specification """
    iv_str = ' + '.join(model['ivs'])
    dep_var = model['dv']
    model_formula = f'{dep_var} ~ {iv_str}'
    logger.info('model: %s', model_formula)

    result = smf.logit(model_formula, data=model['data']).fit()
    logger.info('model fitted.')
    return result


def run_sr_models(all_df):
    """ run sex reporting models """
    br_df = all_df[all_df.DISCIPLINE == BR]
    cm_df = all_df[all_df.DISCIPLINE == CM]
    he_df = all_df[all_df.DISCIPLINE == HE]

    ivs = ['GENDER_FL', 'YEAR', 'np.log2(N_AUTHORS)', 'CONTINENT', 'F_MESH',
           'F_COUNTRY', 'SUBDISCIPLINE']
    models = [{'name': 'sra_all', 'dv': 'SRA', 'ivs': ivs, 'data': all_df},
              {'name': 'sra_br', 'dv': 'SRA', 'ivs': ivs, 'data': br_df},
              {'name': 'sra_cm', 'dv': 'SRA', 'ivs': ivs, 'data': cm_df},
              {'name': 'sra_he', 'dv': 'SRA', 'ivs': ivs, 'data': he_df},
              {'name': 'srm_all', 'dv': 'SRM', 'ivs': ivs, 'data': all_df},
              {'name': 'srf_all', 'dv': 'SRF', 'ivs': ivs, 'data': all_df},
              {'name': 'srb_all', 'dv': 'SRB', 'ivs': ivs, 'data': all_df}]

    for model in models:
        with open('../results/SR_{}.csv'.format(model['name']), 'w') as fout:
            result = run_model(model)
            fout.write(result.summary().as_csv())


def run_jif_models(all_df):
    """ journal impact factor models """
    br_df = all_df[all_df.DISCIPLINE == BR]
    cm_df = all_df[all_df.DISCIPLINE == CM]
    he_df = all_df[all_df.DISCIPLINE == HE]
    years = [2008, 2010, 2012, 2014, 2016]
    jif_model = ('IF ~ GENDER_TOPIC + GENDER_FIRST + GENDER_LAST '
                 '+ np.log2(N_AUTHORS) + CONTINENT + SUBDISCIPLINE')

    def run_and_save(df, model_name='IF_all'):
        for year in years:
            result = smf.ols(jif_model, data=df[df.YEAR == year]).fit()
            with open(f'../results/{model_name}_{year}.csv', 'w') as fout:
                fout.write(result.summary().as_csv())

    run_and_save(df=all_df, model_name='IF_all')
    run_and_save(df=br_df, model_name='IF_br')
    run_and_save(df=cm_df, model_name='IF_cm')
    run_and_save(df=he_df, model_name='IF_he')


def main(reg_table_f, result_files):
    """ run regressions and write the results """
    all_df = pd.read_csv(reg_table_f)
    logger.info('data loaded (N = {}).'.format(len(all_df)))

    run_sr_models(all_df)
    run_jif_models(all_df)


if __name__ == "__main__":
    REG_TABLE = sys.argv[1]
    RESULT = sys.argv[2:]
    main(REG_TABLE, RESULT)
