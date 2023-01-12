## PascalVOC2YOLO
[blog](https://yjs-program.tistory.com/333)   

Converting PascalVOC XML to YOLO txt format   

- This Script written on Ubuntu, Yolov7
- This Script written for Segmentation(default), Object Detection(optional)

### Instruction
1. Place the file into your data directory
```
┌── Data Directory
    ├── images : Image set Directory
    ├── train : XML set Directory(for Train)
    ├── val : XML set Directory(for Validation)
    ├── test : XML set Directory(for Test)
    ├── images_filelist.txt : List of Image Pathes
    ├── train_filelist.txt : List of Train XML pathes
    ├── val_filelist.txt : List of Validation XML paths
    ├── test_filelist.txt : List of Test XML paths
    └── {Place the Code in here!}
```
2. Edit "classes", "dirs" array as your data & Check the dir path in "main" folder
3. Choose how to get the Image set list (from Directory or from TXT file)   
💡 If you wanna make the pre-defined txt file, use below simple script   


```python
# Make TXT list
txt_file = open("./filelist.txt", "w")
files = glob.glob("./train/*") # Get the file lists
xml_lst = sorted([file for file in files if file.endswith(".xml")]) # XML file directory
for line in xml_lst:
    txt_file.write(line+"\n")
txt_file.close()
```

4. Choose the data type    
    - Bbox ( `x, y, w, h` ): for Object Detection
    - Polygon( `x1, y1, ..., x4, y4` ): for Segmentation)
5. Running the Script. Converted Data will be on `../yolo-style/`

```
┌── yolo-style
│    └── train : XML set Directory(for Train)
│        ├── images : image directory
│        └── labels : txt directory
│    └── val : XML set Directory(for Validation)
│        ├── images : image directory
│        └── labels : txt directory
│    └── test : XML set Directory(for Test)
│        ├── images : image directory
│        └── labels : txt directory
│    ├── train.txt : List of Train image pathes
│    ├── val.txt : List of Validation image paths
└──  └── test.txt : List of Test image paths
```   
   
   
   
Reference : Upgraded from Amir's [code](https://gist.github.com/Amir22010/a99f18ca19112bc7db0872a36a03a1ec)   
