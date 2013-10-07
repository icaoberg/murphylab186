import sys
from ricerca import content
import numpy
import pickle
import csv
import os
import copy

from random import seed, shuffle
from numpy import isnan

INT_DIR='./intermediate_results/RandTag_pickle_files/'

def writeToCSV(file,data):
    f1=open(file,'a')
    csvwriter=csv.writer(f1,delimiter=',')
    csvwriter.writerow(data)
    f1.close()

def printToFile(printfile, str):
    f3=open(printfile,'a')
    print >>f3,str
    f3.close()

def auc(sorted_binary):
    pos=sum(sorted_binary)
    neg=len(sorted_binary)-pos
    #calculate ROC
    xy_arr = []
    tp = 0.0
    fp = 0.0                    #assure float division
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


def combinePosandNeg(pos_sorted,neg_sorted):
    #reverse negative list before averaging
    neg_sorted.reverse()
    img_avg=[]
    rank=range(len(pos_sorted))
    pos_sort_rank=zip(pos_sorted,rank)
    neg_sort_rank=zip(neg_sorted,rank)
    pos_sort_rank.sort(key=lambda img:img[0])
    neg_sort_rank.sort(key=lambda img:img[0])
    for j in range(len(pos_sort_rank)):
        if pos_sort_rank[j][0]==neg_sort_rank[j][0]:
            img_rank=(pos_sort_rank[j][0],float(pos_sort_rank[j][1]+neg_sort_rank[j][1])/2)
            img_avg.append(img_rank)
    #sort by rank
    img_avg.sort(key=lambda img:img[1])
    avg_sorted=[]
    for img in img_avg:
        avg_sorted.append(img[0])
    return avg_sorted

def run_pos_tests(test_pattern_iid_dict, dataset, dataset_dict, max_sample, num_trials, outfile):
  ii=1
  AUC_pos_var_neg_0 = {}
  for i in range(2,max_sample+1,2):
    AUC_pos_var_neg_0[str(i)]=[]
  for pattern, iids in test_pattern_iid_dict.items():
    iids = [str(iid) for iid in iids]
    sum_auc = 0.0
    test_patterns_copy=copy.deepcopy(test_patterns)
    test_patterns_copy.remove(pattern)
    other_pattern=test_patterns_copy[0]
    for i in range(2, max_sample+1,2):
        for z in range(num_trials):
            #get ids of positive samples
            pos_samples = []
            t_iids = test_pattern_iid_dict[pattern]
            shuffle(t_iids)
            pos_iids = t_iids[:i]
            for pos_iid in pos_iids:
                pos_samples.append(str(pos_iid))
            goodSet_pos=[]
            for iid in pos_samples:
                goodSet_pos.append(dataset_dict[str(iid)])
            [sorted_iids_pos,sorted_scores_pos]=content.ranking(alpha,dataset,goodSet_pos)
            final_result=sorted_iids_pos[:min(Num_total_img,len(sorted_iids_pos))]
            sorted_binary=[]
            for rank_iid in final_result:
                if rank_iid in iids:
                    sorted_binary.append(True)
                else:
                    sorted_binary.append(False)
            auc_ = auc(sorted_binary)
            printstr=str(auc_)+'\t'+str(ii)+' / ' + str(max_sample*num_trials*len(test_pattern_iid_dict))
            print printstr
            ii += 1
            AUC_pos_var_neg_0[str(i)].append(auc_)
  return AUC_pos_var_neg_0


def run_neg_tests(test_pattern_iid_dict, dataset, dataset_dict, max_sample, num_trials, outfile):
  ii=1
  AUC_pos_var_neg_0 = {}
  for i in range(1,max_sample+1):
    AUC_pos_var_neg_0[str(i*2)]=[]
  for pattern, iids in test_pattern_iid_dict.items():
      sum_auc = 0.0
      test_patterns_copy=copy.deepcopy(test_patterns)
      test_patterns_copy.remove(pattern)
      other_pattern=test_patterns_copy[0]
      for i in range(1, max_sample+1):
          for z in range(num_trials):
              #get ids of positive samples
              pos_samples = []
              t_iids = test_pattern_iid_dict[pattern]
              shuffle(t_iids)
              pos_iids = t_iids[:i]
              for pos_iid in pos_iids:
                  pos_samples.append(str(pos_iid))
              #and of negative samples
              neg_samples = []
              t_iids = test_pattern_iid_dict[other_pattern]
              shuffle(t_iids)
              neg_iids = t_iids[:i]
              for neg_iid in neg_iids:
                  neg_samples.append(str(neg_iid))
              goodSet_pos=[]
              for iid in pos_samples:
                goodSet_pos.append(dataset_dict[str(iid)])
              [sorted_iids_pos,sorted_scores_pos]=content.ranking(alpha,dataset,goodSet_pos)
              goodSet_neg=[]
              for iid in neg_samples:
                goodSet_neg.append(dataset_dict[str(iid)])
              [sorted_iids_neg,sorted_scores_neg]=content.ranking(alpha,dataset,goodSet_neg)
              avg_sorted=combinePosandNeg(sorted_iids_pos,sorted_iids_neg)
              final_result=avg_sorted[:min(Num_total_img,len(avg_sorted))]
              sorted_binary=[]
              for rank_iid in final_result:
                if rank_iid in iids:
                    sorted_binary.append(True)
                else:
                    sorted_binary.append(False)
              auc_ = auc(sorted_binary)
              printstr=str(auc_)+'\t'+str(ii)+' / ' + str(max_sample*num_trials*len(test_pattern_iid_dict))
              print printstr
              ii += 1
              AUC_pos_var_neg_0[str(i*2)].append(auc_)
  return AUC_pos_var_neg_0


def run_pos_tests_10x_40x(test_pattern_iid_dict, test_patterns, dataset_dict, max_sample, num_trials, outfile):
  ii=1
  AUC_pos_var_neg_0 = {}
  for i in range(2,max_sample+1,2):
    AUC_pos_var_neg_0[str(i)]=[]
  copy_test_pattern_iid_dict=copy.deepcopy(test_pattern_iid_dict)
  for pattern, iids in test_pattern_iid_dict.items():
    sum_auc = 0.0
    test_patterns_copy=copy.deepcopy(test_patterns)
    test_patterns_copy.remove(pattern)
    other_pattern=test_patterns_copy[0]
    for i in range(2, max_sample+1,2):
        for z in range(num_trials):
            #get ids of positive samples
            pos_samples = []
            t_iids = test_pattern_iid_dict[pattern]
            shuffle(t_iids)
            pos_iids = t_iids[:i]
            for pos_iid in pos_iids:
                pos_samples.append(str(pos_iid))
#
            if all(samp.endswith('40x') for samp in pos_samples):
                res='40x'
            else:
                res='10x'

            test_dataset=[]
            for test_pattern, p_iids in copy_test_pattern_iid_dict.items():
                for p_iid in p_iids:
                    v=dataset_dict[p_iid]
                    if v.has_key(res):
                        test_dataset.append(v[res])

            Num_total_img=len(test_dataset)
            
            goodSet_pos=[]
            for iid in pos_samples:
                goodSet_pos.append(dataset_dict[str(iid)][res])
            [sorted_iids_pos,sorted_scores_pos]=content.ranking(alpha,test_dataset,goodSet_pos)

            final_result=sorted_iids_pos[:min(Num_total_img,len(sorted_iids_pos))]
            sorted_binary=[]
            for rank_iid in final_result:
                if rank_iid in iids:
                    sorted_binary.append(True)
                else:
                    sorted_binary.append(False)
            auc_ = auc(sorted_binary)
            printstr=str(auc_)+'\t'+str(ii)+' / ' + str(max_sample*num_trials*len(test_pattern_iid_dict))
            print printstr
            ii += 1
            AUC_pos_var_neg_0[str(i)].append(auc_)
  return AUC_pos_var_neg_0


def run_neg_tests_10x_40x(test_pattern_iid_dict, test_patterns, dataset_dict, max_sample, num_trials, outfile):
  ii=1
  AUC_pos_var_neg_0 = {}
  for i in range(1,max_sample+1):
      AUC_pos_var_neg_0[str(i*2)]=[]
  copy_test_pattern_iid_dict=copy.deepcopy(test_pattern_iid_dict)
  for pattern, iids in test_pattern_iid_dict.items():
      sum_auc = 0.0
      test_patterns_copy=copy.deepcopy(test_patterns)
      test_patterns_copy.remove(pattern)
      other_pattern=test_patterns_copy[0]
      for i in range(1, max_sample+1):
          for z in range(num_trials):
              #get ids of positive samples
              pos_samples = []
              t_iids = test_pattern_iid_dict[pattern]
              shuffle(t_iids)
              pos_iids = t_iids[:i]
              for pos_iid in pos_iids:
                  pos_samples.append(str(pos_iid))
              #and of negative samples
              neg_samples = []
              t_iids = test_pattern_iid_dict[other_pattern]
              shuffle(t_iids)
              neg_iids = t_iids[:i]
              for neg_iid in neg_iids:
                  neg_samples.append(str(neg_iid))
#                  
              #decide resolution
              all_samples=pos_samples+neg_samples
              if all(samp.endswith('40x') for samp in all_samples):
                  res='40x'
              else:
                  res='10x'

              test_dataset=[]
              for test_pattern, p_iids in copy_test_pattern_iid_dict.items():
                for p_iid in p_iids:
                    v=dataset_dict[p_iid]
                    if v.has_key(res):
                        test_dataset.append(v[res])

              Num_total_img=len(test_dataset)
            
              goodSet_pos=[]
              for iid in pos_samples:
                  goodSet_pos.append(dataset_dict[str(iid)][res])
              [sorted_iids_pos,sorted_scores_pos]=content.ranking(alpha,test_dataset,goodSet_pos)
              goodSet_neg=[]
              for iid in neg_samples:
                  goodSet_neg.append(dataset_dict[str(iid)][res])
              [sorted_iids_neg,sorted_scores_neg]=content.ranking(alpha,test_dataset,goodSet_neg)
              avg_sorted=combinePosandNeg(sorted_iids_pos,sorted_iids_neg)
              final_result=avg_sorted[:min(Num_total_img,len(avg_sorted))]
              sorted_binary=[]
              for rank_iid in final_result:
                  if rank_iid in iids:
                      sorted_binary.append(True)
                  else:
                      sorted_binary.append(False)
              auc_ = auc(sorted_binary)
              printstr=str(auc_)+'\t'+str(ii)+' / ' + str(max_sample*num_trials*len(test_pattern_iid_dict))
              print printstr
              ii += 1
              AUC_pos_var_neg_0[str(i*2)].append(auc_)
  return AUC_pos_var_neg_0


def load_10x():
    pat_id_pkl=open(INT_DIR+'pattern_iid_dict_10x.pkl','rb')
    pattern_iid_dict_10x=pickle.load(pat_id_pkl)
    pat_id_pkl.close()

    dataset_pkl=open(INT_DIR+'dataset_10x.pkl','rb')
    dataset_10x=pickle.load(dataset_pkl)
    dataset_pkl.close()

    dataset_dict_10x=dict((line[0],line) for line in dataset_10x)
    return pattern_iid_dict_10x, dataset_10x, dataset_dict_10x


def load_40x():
    pat_id_pkl=open(INT_DIR+'pattern_iid_dict_40x.pkl','rb')
    pattern_iid_dict_40x=pickle.load(pat_id_pkl)
    pat_id_pkl.close()

    dataset_pkl=open(INT_DIR+'dataset_40x.pkl','rb')
    dataset_40x=pickle.load(dataset_pkl)
    dataset_pkl.close()

    dataset_dict_40x=dict((line[0],line) for line in dataset_40x)
    return pattern_iid_dict_40x, dataset_40x, dataset_dict_40x


def load_10x_40x():
    [pattern_iid_10x_dict, dataset_10x, dataset_10x_dict]=load_10x()
    [pattern_iid_40x_dict, dataset_40x, dataset_40x_dict]=load_40x()
#    pattern_iid_dict={}
#    for pattern in pattern_iid_10x_dict:
#        new_list=[]
#        for iid in pattern_iid_10x_dict[pattern]:
#            new_list.append(str(iid)+'_10x')
#        for iid in pattern_iid_40x_dict[pattern]:
#            new_list.append(str(iid)+'_40x')
#        pattern_iid_dict[pattern]=new_list
#
#    dataset_10x_new = [[x[0]+'_10x',x[1],x[2]] for x in dataset_10x]
#    dataset_40x_new = [[x[0]+'_40x',x[1],x[2]] for x in dataset_40x]
#    dataset=dataset_10x_new+dataset_40x_new

    pat_id_pkl=open(INT_DIR+'pattern_iid_dict_10x-40x.pkl','rb')
    pattern_iid_dict=pickle.load(pat_id_pkl)
    pat_id_pkl.close()

    dataset_pkl=open(INT_DIR+'dataset_10x-40x.pkl','rb')
    dataset=pickle.load(dataset_pkl)
    dataset_pkl.close()

    int_dict=dict((line[0],line) for line in dataset)

    dataset_dict={}
    for key in int_dict:
        dataset_dict[key]={}
        if key.endswith('10x'):
            dataset_dict[key]['10x']=int_dict[key]
        if key.endswith('40x'):
            dataset_dict[key]['40x']=int_dict[key]
            new_key=key.replace('40x','10x')
            if int_dict.has_key(new_key):
                new_vals=int_dict[new_key]
                dataset_dict[key]['10x']=[key,new_vals[1],new_vals[2]]
                
    
#    dataset_dict={}
#    for a in dataset:
#        dataset_dict[a[0]]={}

#    for a in dataset_10x_new:
#        dataset_dict[a[0]]['10x']=a

#    for a in dataset_40x_new:
#            dataset_dict[a[0]]['40x']=a
#            new_key=a[0].replace('40x','10x')
#            if dataset_dict.has_key(new_key):
#                if len(dataset_dict[new_key]['10x'])==3:
#                    dataset_dict[a[0]]['10x']=[a[0],dataset_dict[new_key]['10x'][1],dataset_dict[new_key]['10x'][2]]

    return pattern_iid_dict, dataset, dataset_dict


#####PARAMETERS######
alpha = -5
##################### 

pattern1=sys.argv[1]
pattern2=sys.argv[2]
resolutions=sys.argv[3]
sample_type=sys.argv[4]

test_patterns=[pattern1,pattern2]

if resolutions == '10x-40x':
    [pattern_iid_dict,dataset,dataset_dict]=load_10x_40x()
elif resolutions == '10x':
    [pattern_iid_dict,dataset,dataset_dict]=load_10x()
elif resolutions == '40x':
    [pattern_iid_dict,dataset,dataset_dict]=load_40x()
else:
    print 'must specify valid resolution: 10x, 40x, 10x-40x'

Num_total_img = len(dataset)

test_pattern_iid_dict=dict((pattern,pattern_iid_dict[pattern]) for pattern in test_patterns)
filename_prefix=resolutions+'_'
for pattern in test_pattern_iid_dict.keys():
    filename_prefix+=pattern+'_'
    
outfile='scripts/out/'+filename_prefix+sample_type+'.out'

########samples from all clones, normalization###################

max_sample = int(sys.argv[5])
num_trials = int(sys.argv[6])

if resolutions == '10x-40x':
  if sample_type=='pos':
    print 'processing positive ROC test'
    seed(42)
    AUC_pos_var_neg_0=run_pos_tests_10x_40x(test_pattern_iid_dict,test_patterns,dataset_dict,max_sample,num_trials,outfile)
  elif sample_type=='neg':
    seed(43)
    print 'processing positive/negative ROC test'
    AUC_pos_var_neg_0=run_neg_tests_10x_40x(test_pattern_iid_dict,test_patterns,dataset_dict,max_sample,num_trials,outfile)
  else:
    print 'please choose to run either pos (positive samples only) or neg (positive and negative samples)'
else:
    test_dataset=[]
    for pattern in test_patterns:
        for iid in pattern_iid_dict[pattern]:
            test_dataset.append(dataset_dict[iid])
    if sample_type=='pos':
        print 'processing positive ROC test'
        seed(666)
        AUC_pos_var_neg_0=run_pos_tests(test_pattern_iid_dict,test_dataset,dataset_dict,max_sample,num_trials,outfile)
    elif sample_type=='neg':
        print 'processing positive/negative ROC test'
        seed(667)
        AUC_pos_var_neg_0=run_neg_tests(test_pattern_iid_dict,test_dataset,dataset_dict,max_sample,num_trials,outfile)
    else:
        print 'please choose to run either pos (positive samples only) or neg (positive and negative samples)'
                                    


filename = filename_prefix+'-allclones_'+sample_type+'.pkl'
output = open('out/'+filename, 'wb')
pickle.dump(AUC_pos_var_neg_0, output)
output.close()

