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
        for line in open(in_f):
            if line.startswith('Dep.'):
                line = line.replace('IF', 'Impact Factor')
            if line.startswith('Date:'):
                line = line.replace(',', '.', 2).replace('.', ',', 1)
            if line.startswith('GENDER'):
                for a, b in {'GENDER_TOPIC[T.B]': 'Sex reported (M & F)',
                             'GENDER_TOPIC[T.F]': 'Sex reported (F)',
                             'GENDER_TOPIC[T.M]': 'Sex reported (M)',
                             'GENDER_FIRST[T.F]': 'Female first author',
                             'GENDER_LAST[T.F]': 'Female last author'}.items():
                    line = line.replace(a, b)
            if line.startswith('Warnings'):
                break

            if line.startswith('Omnibus'):
                line = '\n' + line

            fout.write(line)


if __name__ == "__main__":
    RESULT_TABLE = sys.argv[1]
    CLEANED_PATH = sys.argv[2]
    main(RESULT_TABLE, CLEANED_PATH)
