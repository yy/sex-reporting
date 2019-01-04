# Raw data

All raw data is provided by Vincent Larivière.

- `genderXgender_v20180710.txt`: the main dataset (received on 20180710).
- `Country_Region_2.xlsx`: a dataset for regional (continental) classification of each country (received on 20180621).
- `MESH_v20180726.txt`: a dataset about paper id and MESH terms (received on 20180726).

# Curated data

- `country_continent_added.csv`: a list of manually added country-continent associations for creating the final country-continent file.

# Downloaded data

- `mesh/mtreesxxxx.bin`: MeSH hierarchy files downloaded from NIH ftp. Downloaded by executing the workflow. 

# Derived data

All generated from the above datasets. 

- `country_continent.csv`: a cleaned version. see the notebook `01 - Continent ...` or the workflow.
- `disease_mesh.txt`: the list of disease MeSH terms.
- `female_frac_per_mesh.csv`: female (first/last) author fraction for each MeSH term.
- `multi_author.csv`: the paper information processed from `genderXgender` file, only the papers with multiple authors.
- `multi_author_mesh.csv`: the paper information + MeSH covariate.
- `multi_author_final.csv`: the paper information + all covariates.
- `paper_mesh_feature.csv`: mesh covariate for each paper.
- `reg_table.csv`: the final regression table that contains all information.
- `single_author.csv`: the paper information processed from `genderXgender` file, only the single authors.
