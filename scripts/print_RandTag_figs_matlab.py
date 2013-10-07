import sys
import pickle
import numpy as np
from glob import glob

def colors(fname):
  color=''
  if 'Mito' in fname:
    if 'ER' in fname:
      color='1'
    if 'Nucl' in fname:
      color='2'
  else:
    color='3'
  if 'pos' in fname:
    return "Col{"+color+"});"
  elif 'neg' in fname:
    return "Col{"+color+"},'MarkerFaceColor',col{"+color+"});"

def printToFile(printfile, str):
  f3=open(printfile,'a')
  print >>f3,str
  f3.close()
              
resolutions=sys.argv[1]
figfile=sys.argv[2]
filenames=glob('out/'+resolutions+'_*.pkl')
outfile='display_ROC_result_'+resolutions+'.m'

#print header
printToFile(outfile,"Col={'-k^' '-gs' '-ro'};")
printToFile(outfile,"col={'k','g','r'};")
printToFile(outfile,"%Mito-ER, Mito-Nucleus, Nucleus-ER")
printToFile(outfile,"x=[2,4,6,8,10];")
printToFile(outfile,"")

#print mean and stderror values for each pairing
for fname in filenames:
  printToFile(outfile,"%"+fname)
  filename=pickle.load(open(fname,'rb'))
  meanval=[]
  label=[]
  stderror=[]

  pos=filename.keys()
  printToFile(outfile,"tmp=zeros("+str(len(pos))+",2)");

  for key in pos:
    a=filename[str(key)]
    a_mean=np.mean(a)
    std=np.std(a)
    num_trials=len(a)
    stderr=std/np.sqrt(num_trials)
    if 'pos' in fname:
      ind_str=str(int(key)/2)
    elif 'neg' in fname:
      ind_str=key
    printToFile(outfile,"tmp("+ind_str+",:)=["+str(a_mean)+", "+str(stderr)+"];")

  printToFile(outfile,"tmp=tmp';")
  printToFile(outfile,"y=tmp(1,:);")
  printToFile(outfile,"e=tmp(2,:);")
  errorbar_start="errorbar(x,y,e, "
  errorbar_end=colors(fname)
  printToFile(outfile,errorbar_start+errorbar_end)
  printToFile(outfile,"hold on")
  printToFile(outfile,"")

#print tail
printToFile(outfile,"axis([0 11 0 1]);")
printToFile(outfile,"xlabel('Number of Positive/Negative samples')")
printToFile(outfile,"ylabel('Average area under ROC curve')")
printToFile(outfile,"title('Content-Based Image Retrieval of 40x Images')")
printToFile(outfile,"")
printToFile(outfile,"hleg1 = legend('0 Mito vs ER (pos)','1 Mito vs ER (pos + neg)','2 Mito vs Nuclear (pos)','3 Mito vs Nuclear (pos + neg)','4 Nuclear vs ER (pos)','5 Nuclear vs ER (pos + neg)');")
printToFile(outfile,"")
printToFile(outfile,"set(hleg1,'Location','SouthEast')")
printToFile(outfile,"")
printToFile(outfile,"fz_title = 12;")
printToFile(outfile,"fz_str = 6;")
printToFile(outfile,"fz_num = 5;")
printToFile(outfile,"dpi = 600;")
printToFile(outfile,"")
printToFile(outfile,"figuresize_6 = [11,9];")
printToFile(outfile,"set(gcf,'PaperUnits','centimeters','PaperPosition',[0,0,figuresize_6])")
printToFile(outfile,"print('-dpng',['-r' int2str(dpi)],['"+figfile+"'])")

