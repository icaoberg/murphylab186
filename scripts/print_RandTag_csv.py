import sys
import pickle
import numpy
from glob import glob

def printToFile(printfile, str):
    f3=open(printfile,'a')
    print >>f3,str
    f3.close()

resolutions=sys.argv[1]
outfile=sys.argv[2]
printToFile(outfile,"##pattern mix, total number positive and negative images,mean AUC,standard error")
filenames=glob('out/'+resolutions+'_*.pkl')
for filename in filenames:
  pkl_file=open(filename,'rb')
  data=pickle.load(pkl_file)
  for i in data.keys():
    a=data[str(i)]
    mean = numpy.mean(a)
    std = numpy.std(a)
    num_imgs = len(a)
    stderr = std/numpy.sqrt(num_imgs)
    printstr = filename+','+str(i)+','+str(mean)+','+str(stderr)
    printToFile(outfile,printstr)

  pkl_file.close()
