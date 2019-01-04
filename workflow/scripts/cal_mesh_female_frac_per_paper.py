# -*- coding: utf-8 -*-

""" this script calculate the average fraction of female first and last authors
for each paper based on the paper's disease mesh terms.

input:
    - female frac per mesh file
    - multi-author data
    - raw paper mesh data

output:
    paper mesh feature

    paper id | avg_f_first_mesh | avg_f_last_mesh

"""
import sys
import logging
from itertools import islice
from collections import defaultdict

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def get_pid_to_gender(multi_author_data_f):
    """ generate two dictionaries (first author & last author) for paper id
    to female first or last author """
    author_data_df = pd.read_csv(multi_author_data_f,
                                 usecols=['PID', 'YEAR', 'GENDER_FIRST',
                                          'GENDER_LAST'])
    gender_replace_dic = {'M': 0, 'F': 1}
    author_data_df.replace({'GENDER_FIRST': gender_replace_dic,
                            'GENDER_LAST': gender_replace_dic}, inplace=True)
    author_data_dict = author_data_df.set_index('PID').to_dict()
    return author_data_dict['GENDER_FIRST'], author_data_dict['GENDER_LAST']


def get_pid_to_mesh(raw_paper_mesh_data_f, disease_mesh_terms):
    """ returns a dictionary: paper id -> {mesh term, mesh term, ...} """
    pid2meshes = defaultdict(set)
    for line in islice(open(raw_paper_mesh_data_f), 1, None):
        pid, mesh = line.strip().split('\t')
        pid = int(pid)
        if mesh in disease_mesh_terms:
            pid2meshes[pid].add(mesh)
    return pid2meshes


def load_disease_mesh(disease_mesh_f):
    """ load the disease mesh terms. they are strings; one per line """
    return set(open(disease_mesh_f).read().strip().split('\n'))


def load_female_frac_per_mesh(female_frac_per_mesh_f: str):
    """ loads and returns the female fraction per mesh data. """
    df = pd.read_csv(female_frac_per_mesh_f, sep='\t')
    mesh2fracs = df.set_index('MESH').to_dict()
    return mesh2fracs['F_FIRST_MESH'], mesh2fracs['F_LAST_MESH'] 


def main(disease_mesh_f, female_frac_per_mesh_f, raw_paper_mesh_data_f,
         out_path):
    """ for each paper, we look at their disease mesh terms and calculate
    the average f_first_mesh and f_last_mesh """

    disease_mesh_terms = load_disease_mesh(disease_mesh_f)
    logging.info('disease mesh terms loaded.')

    mesh2ffirst, mesh2flast = load_female_frac_per_mesh(female_frac_per_mesh_f)
    logging.info('f frac per mesh data loaded.')

    pid2meshes = get_pid_to_mesh(raw_paper_mesh_data_f, disease_mesh_terms)
    logging.info('pid2mesh data loaded.')

    pid2ffirst = {}
    pid2flast = {}
    null_cnt = 0
    for pid, meshes in pid2meshes.items():
        ff_list = [mesh2ffirst[mesh] for mesh in meshes if mesh in mesh2ffirst]
        fl_list = [mesh2flast[mesh] for mesh in meshes if mesh in mesh2flast]
        if ff_list and fl_list:
            pid2ffirst[pid] = np.mean(ff_list)
            pid2flast[pid] = np.mean(fl_list)

    with open(out_path, 'w') as fout:
        fout.write('{}\t{}\t{}\n'.format('PID', 'F_FIRST_MESH', 'F_LAST_MESH'))
        for pid in pid2ffirst:
            fout.write('{}\t{}\t{}\n'.format(pid, pid2ffirst[pid],
                                             pid2flast[pid]))


if __name__ == "__main__":
    DISEASE_MESH = sys.argv[1]
    FEMALE_FRAC_PER_MESH = sys.argv[2]
    RAW_PAPER_MESH_DATA = sys.argv[3]
    OUT_PATH = sys.argv[4]
    main(DISEASE_MESH, FEMALE_FRAC_PER_MESH, RAW_PAPER_MESH_DATA, OUT_PATH)
