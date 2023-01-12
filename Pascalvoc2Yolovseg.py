import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
from shutil import copyfile
from tqdm import tqdm

# Reference : https://gist.github.com/Amir22010/a99f18ca19112bc7db0872a36a03a1ec

dirs = ['train', 'val', 'test']
classes = ['CLS1', 'CLS2', 'CLS3' ]

def getImagesInDir(dir_path):
    # Get the Image set list from directory
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'): # this script assumes all of your images are .jpg
        image_list.append(filename)

    return image_list

def getImgfromTxt(txt_path):
    # Get the Image set list from pre-defined txt.
    image_list = []
    f = open(txt_path, "r")
    for line in f.readlines():
        img_fileNm = 'images/'+os.path.splitext(line)[0].split("/")[-1]+".jpg" # this script assumes all of your images are .jpg
        image_list.append(img_fileNm)
    return image_list        

def convert_bbox_VOC(size, box):
    # BBOX style converting(for object detection)
    # box = xmin, xmax, ymin, ymax
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h) #bbox format(tl x, tl y, w, h)

def convert_polygon_VOC(size, box):
    # Polygon style converting(for instance segmentation)
    # box = xmin, xmax, ymin, ymax
    xmin, xmax, ymin, ymax = box
    dw = 1./(size[0])
    dh = 1./(size[1])
    
    # Clockwise
    polygon = [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]
    polygon[::2] = [point*dw for point in polygon[::2]]
    polygon[1::2] = [point*dh for point in polygon[1::2]]
    
    return tuple(polygon) # polygon format(x1, y1, x2, y2, x3, y3, x4, y4)

def convert_annotation(dir_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]
    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + '/labels/' + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        
        # Convert as Polygon style(for Instance Segmentation)
        bb = convert_polygon_VOC((w,h), b)
        
        # if you wanna bbox format(x, y, w, h), using below function
        # bb = convert_bbox_VOC((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == "__main__":
    cwd = "./"

    for dir_path in dirs:
        full_dir_path = dir_path # train, val, test
        output_path = '../yolo-style/'+full_dir_path

        if not os.path.exists(output_path+'/images'):
            os.makedirs(output_path+'/images')
        if not os.path.exists(output_path+'/labels'):
            os.makedirs(output_path+'/labels')
            
        fileListTxt = cwd+dir_path+'_filelist.txt'
        image_paths = getImgfromTxt(fileListTxt)
        
        # If you want get the pathes list as Directory
        # image_paths = getImagesInDir($Each Train/Test/Val Image Directory Path)
        
        list_file = open(output_path + '.txt', 'w')
        for image_path in tqdm(image_paths):
            list_file.write(image_path + '\n')
            # Convert Annotation as Yolo TXT format
            convert_annotation(full_dir_path, output_path, image_path)
            # Copy Image files
            copyfile(image_path, output_path+'/images/'+image_path.split("/")[-1])
        list_file.close()

        print("Finished processing: " + dir_path)