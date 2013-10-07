from PIL import Image
import numpy as np
def tif2array(tif_file,debug = False):
    """
    @param the tiff file(tif_file), path must be included.
    @return an 3D numpy array, if error, return empty list
    """
    try:
        #6/28/2012 Y.Yu fixed a bug here
        im = Image.open(tif_file) # read the image
    except:
        if debug:
            print 'invalid tiff file'
        return []

    tmplist = [] # store each slice
    firstframe = np.asarray(im.getdata()).reshape(im.size[::-1])

    if firstframe.shape == (): # check if the image can be read 
        if debug:
            print "unsupported image format"
        return []

    tmplist.append(firstframe)
    (row,col) = tmplist[0].shape#image size
    
    try:
        while 1:
            im.seek(im.tell()+1)
            tmp_frame = np.asarray(im.getdata()).reshape(im.size[::-1])   
            if tmp_frame.shape == ():# check if the image can be read 
                if debug:
                    print "The "+str(im.tell())+'th frame is an invalid image'
                return []
            tmplist.append(tmp_frame)
    except EOFError:
        pass # read each frame

    hight = len(tmplist) # the hight of image
    result = np.empty((row,col,hight)) # store the data as a 3D numpy array
    for i in xrange(hight):
        try:
            result[:,:,i] = tmplist[i]
        except:
            if debug:
                print "the size of each frame must be same"
            return []
    #6/28/2012 Y.Yu Changed the output data type as unsigned int
    if im.mode == 'L': # it's 8bit image
        result = result.astype('uint8')
    elif 'I' in im.mode: # it's 16bit image
        result = result.astype('uint16')
    else:
        print 'unsupported image format'
        return None
    return result
        