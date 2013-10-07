# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Carnegie Mellon University All Rights Reserved.
# Use is subject to license terms supplied in LICENSE.txt #
# 
# Version: 1.0
#
##"""
##@author Baek Hwan Cho
##"""

## Test script that generates Fig 2a


def auc(sorted_binary):
    pos=sum(sorted_binary)
    neg=len(sorted_binary)-pos
    #calculate ROC 
    xy_arr = []
    tp = 0.0
    fp = 0.0			#assure float division
    for label in sorted_binary:
      if label == True:
      	tp+=1
      else:
	fp+=1
      xy_arr.append([fp/neg,tp/pos])
    #area under curve
    aoc = 0.0
    prev_x = 0
    for x,y in xy_arr:
            if x != prev_x:
                    aoc += (x - prev_x) * y
                    prev_x = x
    return aoc	


def histogram(L):
    d = {}
    for x in L:
        if x in d:
            d[x] += 1
        else:
            d[x] = 1
    return d


def merge(seq):
    merged = []
    for s in seq:
        for x in s:
            merged.append(x)
    return merged 


from ricerca import content
import pickle
import glob
import numpy


GO_TERMS={}

GO_TERMS['GO:0000228']= 'nuclear chromosome'
GO_TERMS['GO:0000776']= 'kinetochore'
GO_TERMS['GO:0000922']= 'spindle pole'
GO_TERMS['GO:0001725']= 'stress fiber'
GO_TERMS['GO:0001726']= 'ruffle'
GO_TERMS['GO:0005623']= 'cell'
GO_TERMS['GO:0005634']= 'nucleus'
GO_TERMS['GO:0005814']= 'centriole'
GO_TERMS['GO:0005815']= 'microtubule organizing center'
GO_TERMS['GO:0005819']= 'spindle'
GO_TERMS['GO:0005856']= 'cytoskeleton'
GO_TERMS['GO:0005874']= 'microtubule'
GO_TERMS['GO:0005881']= 'cytoplasmic microtubule'
GO_TERMS['GO:0005925']= 'focal adhesion'
GO_TERMS['GO:0009289']= 'pilus'
GO_TERMS['GO:0014069']= 'postsynaptic density'
GO_TERMS['GO:0015629']= 'actin cytoskeleton'
GO_TERMS['GO:0015630']= 'microtubule cytoskeleton'
GO_TERMS['GO:0020010']= 'conoid'
GO_TERMS['GO:0030027']= 'lamellipodium'
GO_TERMS['GO:0030175']= 'filopodium'
GO_TERMS['GO:0030424']= 'axon'
GO_TERMS['GO:0030425']= 'dendrite'
GO_TERMS['GO:0030426']= 'growth cone'
GO_TERMS['GO:0043668']= 'exine'
GO_TERMS['GO:0044294']= 'dendritic growth cone'
GO_TERMS['GO:0044295']= 'axonal growth cone'
GO_TERMS['GO:0044309']= 'neuron spine'
GO_TERMS['GO:0044420']= 'extracellular matrix part'
GO_TERMS['GO:0044456']= 'synapse part'
GO_TERMS['GO:0045111']= 'intermediate filament cytoskeleton'
GO_TERMS['GO:0045202']= 'synapse'
GO_TERMS['GO:0055028']= 'cortical microtubule'
GO_TERMS['GO:0055120']= 'striated muscle dense body'
GO_TERMS['GO:0060076']= 'excitatory synapse'
GO_TERMS['GO:0070258']= 'inner membrane complex'
GO_TERMS['GO:0072372']= 'primary cilium'

flag_bad_iids = False
#try:
#    f1=open('img_ids_low_auc.pkl2','rb')
#    iids_bad_from_file = pickle.load(f1)
#    f1.close()
#    flag_bad_iids = True
#except:
#    flag_bad_iids = False
    
# read image ids and their GO terms
f1=open('scripts/image_ids_ASCB.goterms','r')
image_lines=f1.readlines()
f1.close()

image_dict={}
goterms = []
IIDs_selected_imgs = []
for line in image_lines:
     [id,goterm]=line.split('###')
     iid=long(id.strip())
     flag_good = True
     if flag_bad_iids:
         if iid in iids_bad_from_file:
             flag_good = False
     if flag_good:
         goterm_=goterm.strip()
         image_dict[iid]=goterm_
         goterms.append(goterm_)
         IIDs_selected_imgs.append(iid)


got = histogram(goterms)
patterns = got.keys()
pattern_iid_dict={}
for pattern in patterns:
		 pattern_iid_dict[pattern]=[]

AVG_AUC_per_each_pattern = {}


for iid, pattern in image_dict.items():
		 pattern_iid_dict[pattern].append(iid)
    

pattern_term_iid_dict = {}
for pts, iids in pattern_iid_dict.items():
		 tmp = []
		 key = pts.split(',')
		 for key2 in key:
		 		 key3 = key2.split(' ')
		 		 tmp.append(key3)
		 pattern2 = merge(tmp)
		 
		 name_tmp = []
		 for jj in pattern2:
		 			name_tmp.append(GO_TERMS[jj])
		 name_tmp.sort()
		 name = ''
		 for go_term in name_tmp:
		 		  name = name+go_term+' AND '
		 name = name[:-5]
		 if pattern_term_iid_dict.has_key(name):
		 			pattern_term_iid_dict[name] += iids
		 else:
		 			pattern_term_iid_dict[name]=iids
		 

number_of_image_per_pattern = {}
number_of_image_total = 0
for pts, iids in pattern_term_iid_dict.items():
		 number_of_image_per_pattern[pts]=len(iids)
		 number_of_image_total = number_of_image_total + len(iids)



pattern_term_iid_dict_refine = {}
number_of_image_per_pattern_refine = {}
number_of_image_total_refine = 0
for pts, iids in pattern_term_iid_dict.items():
		 if len(iids) >= 5: # only for those pattern that include more than 4 images
                     pattern_term_iid_dict_refine[pts]=iids
                     number_of_image_per_pattern_refine[pts]=len(iids)
                     number_of_image_total_refine = number_of_image_total_refine + len(iids)
                     

		 


# generate the contentDB dataset
files = glob.glob("./intermediate_results/ASCB_features/*.pkl")

dataset=[]    
for fl in files:
    ID = fl.replace("./intermediate_results/ASCB_features/","")[:-4] # assuming the file name ends with '.pkl' such as '1123.pkl'
    if long(ID) in IIDs_selected_imgs:
        pkl_file = open(fl, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
        feat_vec = list(data[:])  # not sure if this is correct
        dataset.append([ID,1,feat_vec])


# initialization
AUC_per_each_pattern = {}
for key, iids in pattern_term_iid_dict_refine.items():
    AUC_per_each_pattern[key]=[]
		
ii=1
aucs = []
low_auc = []
for key, iids in pattern_term_iid_dict_refine.items():
    for iid in iids:
        # pickle file read
        filename = './intermediate_results/ASCB_features/'+str(iid)+'.pkl'
        pkl_file = open(filename, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()

        ID=iid
        feat_vec = list(data[:])  # not sure if this is correct
        goodset = [[ID, 1, feat_vec]]

        alpha = -5
        [sorted_iids, sorted_scores] = content.ranking( alpha, dataset, goodset )
        
        sorted_binary = []
        for rank_iid in sorted_iids:
                if long(rank_iid) in iids:
                        sorted_binary.append(True)
                else:
                        sorted_binary.append(False)
        auc_ = auc(sorted_binary)

        if auc_ < 0.5:
            low_auc.append([iid, key])

        print str(ii) + ' / ' + str(number_of_image_total_refine)
        print auc_

        AUC_per_each_pattern[key].append(auc_)
        aucs.append(auc_)
        ii=ii+1





keylist = AUC_per_each_pattern.keys()
keylist.sort()
# display the results
for key in keylist:
    mean = numpy.mean(AUC_per_each_pattern[key])
    std = numpy.std(AUC_per_each_pattern[key])
    std_err = std/numpy.sqrt(len(AUC_per_each_pattern[key])) # standard error is std/sqrt(N)
    print key + ' NUM_IMG: ' + str(len(AUC_per_each_pattern[key])) + ' AVG: '+str(mean)+ '  STDE: ' + str(std_err)

print 'total number of images: ' + str(number_of_image_total_refine)
print 'overall average of AUCs: ' + str(numpy.mean(aucs))


output = open('./out/AUC_ASCB.pkl2', 'wb')
pickle.dump(AUC_per_each_pattern, output)
output.close()





