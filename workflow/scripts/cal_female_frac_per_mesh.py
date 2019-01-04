# -*- coding: utf-8 -*-

""" this script calculate the average fraction of female first and last authors
for each disease mesh term.

uses:
    - disease mesh term set
    - multi-author data
    - paper-mesh data

output:
    - female frac per mesh file that contains female first author fraction and
    female last author fraction for each mesh term.

    MeSH term (string) | avg f_first | avg f_last

"""
import sys
import logging
from itertools import islice
from collections import defaultdict

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def load_disease_mesh(disease_mesh_f):
    """ load the disease mesh terms. they are strings; one per line """
    return set(open(disease_mesh_f).read().strip().split('\n'))


def get_pid_to_gender(multi_author_data_f):
    """ generate two dictionaries (first author & last author) for paper id
    to female first or last author """
    author_data_df = pd.read_csv(multi_author_data_f,
                                 usecols=['PID', 'YEAR', 'GENDER_FIRST',
                                          'GENDER_LAST'])
    gender_replace_dic = {'M': 0, 'F': 1}
    author_data_df.replace({'GENDER_FIRST': gender_replace_dic,
                            'GENDER_LAST': gender_replace_dic},
                           inplace=True)
    author_data_dict = author_data_df.set_index('PID').to_dict()
    return author_data_dict['GENDER_FIRST'], author_data_dict['GENDER_LAST']


def get_mesh_to_paperid(raw_paper_mesh_data_f, disease_mesh_terms):
    """ returns a dictionary: mesh term -> [paper id, paper id, ...] """
    mesh2pid = defaultdict(set)
    for line in islice(open(raw_paper_mesh_data_f), 1, None):
        pid, mesh = line.strip().split('\t')
        if mesh in disease_mesh_terms:
            mesh2pid[mesh].add(int(pid))
    return mesh2pid


def main(disease_mesh_f, multi_author_data_f, raw_paper_mesh_data_f, out_path):
    """ calculate the female fraction at the first and last author position
    given a mesh term. """
    disease_mesh_terms = load_disease_mesh(disease_mesh_f)
    logging.info('disease mesh terms loaded.')

    f_first_dict, f_last_dict = get_pid_to_gender(multi_author_data_f)
    logging.info('paper id -> author gender dictionary loaded.')

    mesh2pid = get_mesh_to_paperid(raw_paper_mesh_data_f, disease_mesh_terms)
    logging.info('mesh -> paper id loaded.')

    mesh2ffirst = {}
    mesh2flast = {}
    for mesh, pids in mesh2pid.items():
        ff_list = [f_first_dict[pid] for pid in pids if pid in f_first_dict]
        fl_list = [f_last_dict[pid] for pid in pids if pid in f_last_dict]
        if ff_list and fl_list:
            mesh2ffirst[mesh] = np.mean(ff_list)
            mesh2flast[mesh] = np.mean(fl_list)

    with open(out_path, 'w') as fout:
        fout.write('{}\t{}\t{}\n'.format('MESH', 'F_FIRST_MESH',
                                         'F_LAST_MESH'))
        for mesh in mesh2ffirst:
            fout.write('{}\t{}\t{}\n'.format(mesh, mesh2ffirst[mesh],
                                             mesh2flast[mesh]))


if __name__ == "__main__":
    DISEASE_MESH = sys.argv[1]
    MULTI_AUTHOR_DATA = sys.argv[2]
    RAW_PAPER_MESH_DATA = sys.argv[3]
    OUT_PATH = sys.argv[4]
    main(DISEASE_MESH, MULTI_AUTHOR_DATA, RAW_PAPER_MESH_DATA, OUT_PATH)
