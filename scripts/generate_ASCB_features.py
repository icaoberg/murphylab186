try:
      import cPickle as pickle
except:
      import pickle
      
import os
print os.getcwd()
import sys
sys.path.append(os.getcwd()+'/scripts')
import tif2array
import pyslic

for key, val in sys.modules.items():
      if 'pyslic' in key:
            print key,val

INPUT_DIR='./images/ASCB_images/'
OUTPUT_DIR='./intermediate_results/ASCB_features/'

if not os.path.isdir(OUTPUT_DIR):
      os.makedirs(OUTPUT_DIR)

image_res_dict=pickle.load(open('scripts/image_res_dict.pkl','rb'))
for imageid, res in image_res_dict.items():
      filename=INPUT_DIR+str(imageid)+'.tiff'
      if os.path.isfile(filename):
          img_read=tif2array.tif2array(filename,True)
          img=pyslic.Image()
          img.channeldata['protein']=img_read[:,:,0]
          img.channels['protein']=filename
          img.scale=res
          feats=pyslic.computefeatures(img,'slf33')
          if feats is not None:
              pickle.dump(feats,open(OUTPUT_DIR+str(imageid)+'.pkl','wb'))

                                            
