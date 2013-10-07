import sys
import os
import pyslic
import numpy as np
import pickle
from pyslic.image.io import auto_detect_load

#INT_DIR='intermediate_results/RandTag_pickle_files/'
INT_DIR='new_pickle_files/'
if not os.path.isdir(INT_DIR):
    os.makedirs(INT_DIR)

def compute_field_features(img, scale, F):
    try:
        img.scale=scale
        print img.scale
        with pyslic.image.loadedimage(img):
            return pyslic.computefeatures(img, 'field-dna+')
    except:
        return None

def make_content_db(basedir,scale):
    dataset=[]
    pattern_iid_dict={}
    for x in os.listdir(basedir):
        pattern_iid_dict[x]=[]
        for y in os.listdir(basedir+x):
            directory=basedir+x+'/'+y
            print directory
            imgs=auto_detect_load(directory)
            for img in imgs:
                img.scale=scale
                img.load()
                field_features=pyslic.computefeatures(img,'field-dna+')
                img_id=os.path.basename(img.channels['protein']).replace('.bmp','_10x')
                dataset.append([img_id,1,list(field_features)])
                pattern_iid_dict[x].append(img_id)

    pickle.dump(dataset,open(INT_DIR+'dataset_'+resolution+'.pkl','wb'))
    pickle.dump(pattern_iid_dict,open(INT_DIR+'pattern_iid_dict_'+resolution+'.pkl','wb'))
    

resolution=sys.argv[1]
scale=float(sys.argv[2])
res_dir_dict={'10x':'image_files/test_simulated_10x/','40x':'test_image_files/original_40x/'}

if resolution=='10x-40x':
    if not os.path.isfile(INT_DIR+'dataset_10x.pkl'):
        make_content_db(res_dir_dict['10x'],.645)
    if not os.path.isfile(INT_DIR+'dataset_40x.pkl'):
        make_content_db(res_dir_dict['40x'],.16125)
    pattern_iid_40x_dict=pickle.load(open(INT_DIR+'pattern_iid_dict_40x.pkl','rb'))
    dataset_40x=pickle.load(open(INT_DIR+'dataset_40x.pkl','rb'))
    pattern_iid_10x_dict=pickle.load(open(INT_DIR+'pattern_iid_dict_40x.pkl','rb'))
    dataset_10x=pickle.load(open(INT_DIR+'dataset_40x.pkl','rb'))
        
    pattern_iid_dict={}
    for pattern in pattern_iid_10x_dict:
        new_list=[]
        for iid in pattern_iid_10x_dict[pattern]:
            new_list.append(str(iid)+'_10x')
        for iid in pattern_iid_40x_dict[pattern]:
            new_list.append(str(iid)+'_40x')
        pattern_iid_dict[pattern]=new_list
    
    dataset_10x_new = [[x[0]+'_10x',x[1],x[2]] for x in dataset_10x]
    dataset_40x_new = [[x[0]+'_40x',x[1],x[2]] for x in dataset_40x]
    dataset=dataset_10x_new+dataset_40x_new

    pickle.dump(dataset,open(INT_DIR+'dataset_10x-40x.pkl','wb'))
    pickle.dump(pattern_iid_dict,open(INT_DIR+'pattern_iid_dict_10x-40x.pkl','wb'))
    
else:
    make_content_db(res_dir_dict[resolution])
