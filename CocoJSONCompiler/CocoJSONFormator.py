'''
{
    "info": info,
    "images": [image],
    "annotations": [annotation],
    "licenses": [license],
}

info{
"year": int, "version": str, "description": str, "contributor": str, "url": str, "date_created": datetime,
}

image{
    "id": int,
    "width": int,
    "height": int,
    "file_name": str,
    "license": int,
    "flickr_url": str,
    "coco_url": str,
    "date_captured": datetime,
}

license{
"id": int, "name": str, "url": str,
}
"annotations": [
        {
            "id": 1,
            "image_id": 1,
            "category_id": 2,
            "bbox": [260, 177, 231, 199],
            "segmentation": [...],
            "keypoints": [224, 226, 2, ...],
            "num_keypoints": 10,
            "score": 0.95,
            "area": 45969,
            "iscrowd": 0
        }
'''
import os, time
from PIL import Image as Img
import json
from datetime import datetime
import sys

class Image:
    def __init__(self, id: int, license: int, file_name: str, height: int, width: int, date: str):
        self.id = id
        self.license = license
        self.file_name = file_name
        self.height = height
        self.width = width
        self.date_captured = date

class Annotation:
    def __init__(self, id: int, image_id: int, category_id: int, bbox: list, segmentation: list, keypoints: list,
                 score: float, area: int, is_crowd: bool ):
        self.id = id
        self.image_id = image_id
        self.category_id = category_id
        self.bbox = bbox
        self.segmentation = segmentation
        self.keypoints = keypoints
        self.num_keypoints = len(keypoints)/3
        self.score = score
        self.area = area
        self.is_crowd = int(is_crowd)

class Info:
    def __init__(self, year: int, version: str, description: str, contributor: str, url: str, date_created: datetime):
        self.year = year
        self.version = version
        self.description = description
        self.contributor = contributor
        self.date_created = date_created

class License:
    def __init__(self, id: int, name: str, url: str):
        self.id = id
        self.name = name
        self.url = url

all_files = os.listdir("./")
txt_files = filter(lambda x: x[-4:] == '.txt', all_files)

Images = []
Annotations = []
image_id = 0
annotation_id = 0

# category_id = need to update according to the ids.
script_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
for t in txt_files:
    jpg = "./" + t[:-4] + ".jpg"
    img = Img.open(jpg)
    wid, hgt = img.size
    image = Image(id=image_id, license=0, file_name=jpg, height=hgt, width=wid, date=time.ctime(os.path.getmtime(jpg)))
    Images.append(json.dumps(image.__dict__))
    with open(t) as f:
        #line = [id, l, t, height, width], l,t,height,width according to dragDropTest.py
        lines = f.readline()

        text_info = lines.split(" ")
        ann = Annotation(image_id=image_id, id=annotation_id, category_id=0,
                         bbox=[int(text_info[1]), int(text_info[2]), int(text_info[3]), int(text_info[4])],
                         segmentation=list(), keypoints=list(), score=0.9, is_crowd=False,
                         area=((int(text_info[2])+int(text_info[4]))*(int(text_info[1]) + int(text_info[3]))))
        Annotations.append(json.dumps(ann.__dict__))
    image_id += 1
    annotation_id += 1

print(Images)
print(Annotations)

Final = {"info": "",
         "licenses": "",
         "categories": "",
         "Images": Images,
         "annotations": Annotations
         }

with open('final_data.json', 'w') as f:
    json.dump(Final, f)