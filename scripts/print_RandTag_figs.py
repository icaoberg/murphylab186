import sys
import pickle
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from pylab import *
import matplotlib.pyplot as plt
from glob import glob

def colors(fname):
  if 'Mito' in fname:
    if 'ER' in fname:
      return 'r'
    if 'Nucl' in fname:
      return 'b'
  else:
    return 'k'

resolutions=sys.argv[1]
filenames=glob(resolutions+'*.pkl')
for fname in filenames:
  filename=pickle.load(open(fname,'rb'))
  meanval=[]
  label=[]
  stderror=[]

#  pos=['2','4','6','8','10']
  pos=filename.keys()
  for i in pos:
    a=filename[str(i)]
    mean=np.mean(a)
    std=np.std(a)
    num_trials=len(a)
    stderr=std/np.sqrt(num_trials)
    label.append(str(i))
    meanval.append(mean)
    stderror.append(stderr)
                                    
  fig=plt.figure(figsize=(9,7))
  ylabel('AUC')
#  plt.axis('tight')
#  plt.ylim(0,1.0)
#  plt.yticks(np.arange(0,1.2,.2))
  line_color=colors(fname)
  print line_color
  line1, errlines1,extra=errorbar(pos,meanval,yerr=stderror, fmt=line_color, ecolor='k')

plt.savefig('Fig1b.pdf')
