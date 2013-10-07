import pickle
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from pylab import *
import matplotlib.pyplot as plt

def process_label(label):
    new_label=''
    for x in label.split(' '):
        if x=='AND':
            new_label+=','
        elif x in ['axon','nucleus','cell']:
            new_label+=x
        else:
            new_label+=x[0].upper()
    return new_label


filename=pickle.load(open('./out/AUC_ASCB.pkl2','rb'))
meanval=[]
num_imgs_val=[]
label=[]
stderror=[]

for i in filename.keys():
    a=filename[str(i)]
    mean=np.mean(a)
    std=np.std(a)
    num_imgs=len(a)
    stderr=std/np.sqrt(num_imgs)
    label.append(str(i))
    meanval.append(mean)
    num_imgs_val.append(num_imgs)
    stderror.append(stderr)
                                    
num_imgs_ind=[]
for ind, val in enumerate(num_imgs_val):
    num_imgs_ind.append((ind,val))

num_imgs_ind.sort(key=lambda img:img[1])

y1val=[]
y2val=[]
x1val=[]
steval=[]

for x in num_imgs_ind:
    ind=x[0]
    y1val.append(meanval[ind])
    y2val.append(num_imgs_val[ind])
    x1val.append(process_label(label[ind]))
    steval.append(stderror[ind])

fig=plt.figure(figsize=(9,7))
ax1=fig.add_subplot(111)
num_classes=11
pos=np.arange(num_classes)+0.5
plt.yticks(np.arange(0,420,50))
ax1.set_ylabel('# images')
rects=ax1.bar(pos, y2val, align='center',width=0.5,color='b')
plt.ylim(0,350)
plt.axis('tight')
ax2=ax1.twinx()
plt.yticks(np.arange(0,1.2,.2))
plt.ylim(0,1.0)
ax2.set_ylabel('AUC')
lines=errorbar(pos,y1val, color='r', linewidth=4, ecolor='k', yerr=steval)
plt.savefig('Fig1a.pdf')
