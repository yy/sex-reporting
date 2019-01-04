# -*- coding: utf-8 -*-

""" this script download the MeSH tree files from NIH ftp and saves them in 
the data folder under 'mesh/'. 

output:
    - data/mesh/'mtrees{year}.bin' files 
        (note that there are no files for 1999 and 2000).  

"""
import sys
import os
import logging

from itertools import chain
from ftplib import FTP

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def mk_outdir(out_path):
    if not os.path.exists(out_path):
        try:
            os.makedirs(out_path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    logging.info('output directory is created.')

def fpath_generator():
    mesh_dir = 'online/mesh'
    mtree_fname = 'meshtrees/mtrees{year}.bin'
    for year in chain(range(1997, 1999), range(2001, 2019)):
        year_folder = '1999-2010' if year < 2011 else f'{year}'
        yield os.path.join(mesh_dir, 
                           year_folder, 
                           mtree_fname.format(year=year))


if __name__ == "__main__":
    FTP_URL = 'nlmpubs.nlm.nih.gov'
    OUT_PATH = '../data/mesh'

    mk_outdir(OUT_PATH)
    ftp = FTP(FTP_URL)
    ftp.login()

    for fname in fpath_generator():
        out_fname = os.path.join(OUT_PATH, os.path.basename(fname))
        ftp.retrbinary(f'RETR {fname}', open(out_fname, 'wb').write)
        logging.info(f'{fname} downloaded.') 


