import sys
import pickle
import numpy

def printToFile(printfile, str):
    f3=open(printfile,'a')
    print >>f3,str
    f3.close()

filename=sys.argv[1]
outfile='Fig1a.csv'
printToFile(outfile,"##pattern,number of images,mean AUC,standard error")
pkl_file=open(filename,'rb')
data=pickle.load(pkl_file)
for i in data.keys():
    a=data[str(i)]
    mean = numpy.mean(a)
    std = numpy.std(a)
    num_imgs = len(a)
    stderr = std/numpy.sqrt(num_imgs)
    printstr = str(i)+','+str(num_imgs)+','+str(mean)+','+str(stderr)
    printToFile(outfile,printstr)

pkl_file.close()
