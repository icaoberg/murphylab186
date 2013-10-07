#!/bin/bash

export PYTHONPATH=./:./PySLIC-0.4.5:./ricerca:$PYTHONPATH

wget -n http://murphylab.web.cmu.edu/software/2012_Nature_Methods/Nature_Methods_OMERO.searcher_intermediate.tgz
tar -xvf Nature_Methods_OMERO.searcher_intermediate.tgz

dir1="./intermediate_results"
if [ ! -d $dir1 ]; then
    echo "Please either untar intermediate_results directory into this one or run generate_intermediate_from_images.sh."
    exit
fi

echo "Generating Fig. 1a"
python scripts/ASCB_ROC_curve_generator.py >& scripts/out/ASCB_ROC_curve_generator.out
python scripts/print_ASCB_csv.py out/AUC_ASCB.pkl2
python scripts/print_ASCB_figs.py

echo "Generating Fig. 1b"
python scripts/RandTag_ROC_curve_generator.py ER Mito 40x pos 10 50 >& scripts/out/40x_RT_ROC_ER_Mito_pos.out
python scripts/RandTag_ROC_curve_generator.py Mito Nucleus 40x pos 10 50 >& scripts/out/40x_RT_ROC_Mito_Nucleus_pos.out
python scripts/RandTag_ROC_curve_generator.py Nucleus ER 40x pos 10 50 >& scripts/out/40x_RT_ROC_Nucleus_ER_pos.out
python scripts/RandTag_ROC_curve_generator.py ER Mito 40x neg 5 50 >& scripts/out/40x_RT_ROC_ER_Mito_neg.out
python scripts/RandTag_ROC_curve_generator.py Mito Nucleus 40x neg 5 50 >& scripts/out/40x_RT_ROC_Mito_Nucleus_neg.out
python scripts/RandTag_ROC_curve_generator.py Nucleus ER 40x neg 5 50 >& scripts/out/40x_RT_ROC_Nucleus_ER_neg.out
python scripts/print_RandTag_csv.py 40x Fig1b.csv
python scripts/print_RandTag_figs_matlab.py 40x Fig1b.png


echo "Generating Fig. S1a"
python scripts/RandTag_ROC_curve_generator.py ER Mito 10x pos 10 50 >& scripts/out/10x_RT_ROC_ER_Mito_pos.out
python scripts/RandTag_ROC_curve_generator.py Mito Nucleus 10x pos 10 50 >& scripts/out/10x_RT_ROC_Mito_Nucleus_pos.out
python scripts/RandTag_ROC_curve_generator.py Nucleus ER 10x pos 10 50 >& scripts/out/10x_RT_ROC_Nucleus_ER_pos.out
python scripts/RandTag_ROC_curve_generator.py ER Mito 10x neg 1 2 >& scripts/out/10x_RT_ROC_ER_Mito_neg.out
python scripts/RandTag_ROC_curve_generator.py Mito Nucleus 10x neg 5 50 >& scripts/out/10x_RT_ROC_Mito_Nucleus_neg.out
python scripts/RandTag_ROC_curve_generator.py Nucleus ER 10x neg 5 50 >& scripts/out/10x_RT_ROC_Nucleus_ER_neg.out
python scripts/print_RandTag_csv.py 10x FigS1a.csv
python scripts/print_RandTag_figs_matlab.py 10x FigS1a.png

echo "Generating Fig. S1b"
python scripts/RandTag_ROC_curve_generator.py ER Mito 10x-40x pos 10 50 >& scripts/out/10x-40x_RT_ROC_ER_Mito_pos.out
python scripts/RandTag_ROC_curve_generator.py Mito Nucleus 10x-40x pos 10 50 >& scripts/out/10x-40x_RT_ROC_Mito_Nucleus_pos.out
python scripts/RandTag_ROC_curve_generator.py Nucleus ER 10x-40x pos 10 50 >& scripts/out/10x-40x_RT_ROC_Nucleus_ER_pos.out
python scripts/RandTag_ROC_curve_generator.py ER Mito 10x-40x neg 5 50 >& scripts/out/10x-40x_RT_ROC_ER_Mito_neg.out
python scripts/RandTag_ROC_curve_generator.py Mito Nucleus 10x-40x neg 5 50 >& scripts/out/10x-40x_RT_ROC_Mito_Nucleus_neg.out
python scripts/RandTag_ROC_curve_generator.py Nucleus ER 10x-40x neg 5 50 >& scripts/out/10x-40x_RT_ROC_Nucleus_ER_neg.out
python scripts/print_RandTag_csv.py 10x-40x FigS1b.csv
python scripts/print_RandTag_figs_matlab.py 10x-40x FigS1b.png
