#!/bin/bash


#create ASCB feature pickle files
python scripts/generate_ASCB_features.py

#create RandTag content db pickle files
python scripts/make_content_db_pickles.py 40x .16125
python scripts/make_content_db_pickles.py 10x .645
python scripts/make_content_db_pickles.py 10x-40x 0