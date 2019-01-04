#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This script cleans the results.

input: result table

output: cleaned table path

1. fix the bug in the date.
2. add the odds ratios.
3. rename the variables.

"""

import sys
import logging

import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def main(in_f, out_f):
    with open(out_f, 'w') as fout:
        result_flag = False
        for line in open(in_f):
            if line.startswith('Dep.'):
                for a, b in {'SRA': 'SR', 'SRF': 'SR_F', 'SRM': 'SR_M',
                             'SRB': 'SR_B'}.items():
                    line = line.replace(a, b)
            if line.startswith('Date:'):
                line = line.replace(',', '.', 2).replace('.', ',', 1)
            if line.startswith('GENDER'):
                for a, b in {'GENDER_FL[T.AF]': 'Male-Female',
                             'GENDER_FL[T.FA]': 'Female-Male',
                             'GENDER_FL[T.FF]': 'Female-Female'}.items():
                    line = line.replace(a, b)
            if result_flag:
                temp = line.split(',')
                OR, ci_low, ci_high = np.exp([float(temp[1]),
                                              float(temp[5]),
                                              float(temp[6])])
                line = line.strip('\n') +\
                    f', {OR:.2f}, {ci_low:.2f}, {ci_high:.2f}\n'
            if ' coef ' in line:
                result_flag = True
                line = line.strip('\n') + ', Odds Ratio , [0.025 , 0.975]\n'

            fout.write(line)


if __name__ == "__main__":
    RESULT_TABLE = sys.argv[1]
    CLEANED_PATH = sys.argv[2]
    main(RESULT_TABLE, CLEANED_PATH)
