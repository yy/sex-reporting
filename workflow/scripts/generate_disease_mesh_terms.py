# -*- coding: utf-8 -*-

""" this script create a list of MeSH terms that belong to the "C" (disease)
category.

input:
    - ../data/mesh/mtrees{year}.bin files
        (note that there are no files for 1999 and 2000).

output:
    - ../data/disease_mesh.txt

"""
import os
import sys
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def disease_mesh_term_generator(mesh_files):
    """ a generator that yield disease mesh terms """
    for mesh_f in mesh_files:
        for line in open(mesh_f):
            try:
                term, code = line.strip().split(';')
            except ValueError:
                continue
            if code.startswith('C'):
                yield term


def main(mesh_path, out_path):
    """ main function """
    meshtree_files = glob.glob(os.path.join(mesh_path, '*'))
    disease_mesh_terms = set(disease_mesh_term_generator(meshtree_files))
    with open(out_path, 'w') as fout:
        fout.write('\n'.join(disease_mesh_terms))


if __name__ == "__main__":
    IN_FILES = sys.argv[1:-1]
    OUT_PATH = sys.argv[-1]
    MESH_PATH = os.path.commonpath(IN_FILES)
    main(MESH_PATH, OUT_PATH)
