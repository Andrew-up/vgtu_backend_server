import base64
import io
import json
import os.path
import shutil
from ast import literal_eval
from pathlib import Path

from PIL import Image

from definitions import ROOT_DIR
from model.model import HistoryNeuralNetwork, ResultPredict
from repository.ModelUnetRepository import ModelUnetRepository
from service.HealingHistoryService import HealingHistoryService
from service.ResultPredictService import ResultPredictService
from utils.read_xml_file import ReadXmlProject

info = {
    "description": "my-project-name"
}


class Categories(object):
    def __init__(self):
        self.id = 0
        self.name = ''


class Annotations(object):
    def __init__(self):
        self.id: int = 0
        self.iscrowd: int = 0
        self.image_id: int = 0
        self.category_id: int = 0
        self.segmentation = []
        self.bbox = []
        self.area = 0


class ImageObj(object):

    def __init__(self):
        self.id: int = 0
        self.width: int = 512
        self.height: int = 512
        self.file_name: str = ''

    def save_image_from_base64(self, base64_image_string, image_path, ann=None):
        im_bytes = base64.b64decode(base64_image_string)  # im_bytes is a binary image
        im_file = io.BytesIO(im_bytes)  # convert image to file-like object
        img = Image.open(im_file)  # img is now PIL Image object
        # img = Image.open(BytesIO(base64.b64decode(base64_image_string.decode('utf-8'))))
        # img, mask = self.randomflip(img, ann)
        print('=======================')

        # print(ann.annotations)
        self.width = img.width
        self.height = img.height
        img.save(f'{image_path}/{self.file_name}', format='png')
        return img, ann


class CocoJsonFormatClass(object):

    def __init__(self, save_image=False):
        # self.img = None
        self.SAVE_IMAGE_BOOL = save_image
        self.info = info
        self.images: list[ImageObj] = []
        self.annotations: list[Annotations] = []
        self.categories: list[Categories] = []
        self.image_folder_path = os.path.join(ROOT_DIR, 'dataset/temp_dataset')

    def isBase64(self, s):
        try:
            return base64.b64encode(base64.b64decode(s)) == s
        except Exception:
            return False

    def addImage(self, string_base64=None, image_path=None, ann=None):
        image = ImageObj()
        if self.images:
            image.id = self.images[-1].id + 1
        else:
            image.id = 1
        image.file_name = f'{image.id}.png'
        img, mask = image.save_image_from_base64(string_base64, image_path, ann)
        self.images.append(image)
        return image, mask

    def addAnnotation(self, img: ImageObj, history_nn: HistoryNeuralNetwork):
        for i in history_nn.annotations:
            annotation = Annotations()
            annotation.bbox = literal_eval(i.bbox)
            annotation.segmentation = [literal_eval(i.segmentation)]
            annotation.iscrowd = 0
            annotation.image_id = img.id
            annotation.area = i.area
            annotation.category_id = i.category_id
            if self.annotations:
                annotation.id = self.annotations[-1].id + 1
            else:
                annotation.id = 0
            self.annotations.append(annotation)

    def start_qwe(self):
        self.printImageId()

    def addCategories(self, catss: ResultPredict):
        cat = Categories()
        cat.id = catss.id_category
        cat.name = catss.name_category_eng
        self.categories.append(cat)

    def getJsonImages(self):
        return json.dumps(self.images, default=lambda x: x.__dict__)

    def getJsonAnnotations(self):
        return json.dumps(self.annotations, default=lambda x: x.__dict__)

    def getJsonCategories(self):
        return json.dumps(self.categories, default=lambda x: x.__dict__)

    def getJsonFull(self):
        c = CocoJsonFormatClass()
        c.images = json.loads(self.getJsonImages())
        c.annotations = json.loads(self.getJsonAnnotations())
        c.categories = json.loads(self.getJsonCategories())
        c = c.__dict__
        c.pop('SAVE_IMAGE_BOOL', None)
        c.pop('image_folder_path', None)
        return c

    def set_image_folder_path(self, path):
        self.image_folder_path = path

    def printImageId(self):
        data = HealingHistoryService(1).getImageForDataset()
        all_cat = ResultPredictService(1).getAll()
        # print(data)
        for j in all_cat:
            self.addCategories(catss=j)

        for i in data:
            if not (self.isBase64(i.photo_predict_edit_doctor) and self.isBase64(i.photo_original)):
                continue

            if not self.SAVE_IMAGE_BOOL:
                img = ImageObj()
                img.id = i.id_history_neural_network
                img.file_name = str(i.id_history_neural_network) + '.png'
                self.images.append(img)
                self.addAnnotation(img=img, history_nn=i)
                continue

            new_image, mask = self.addImage(string_base64=i.photo_original,
                                            image_path=self.image_folder_path, ann=i)
            if new_image and mask:
                print(i.id_history_neural_network)
                self.addAnnotation(img=new_image, history_nn=mask)


class GenerateJsonFileFromDB(object):

    def __init__(self):
        # self.service = HealingHistoryService(1)

        self.coco_class = CocoJsonFormatClass(save_image=True)
        self.dataset_folder_path = None
        self.annotation_folder_path = None
        self.image_folder_path = None
        self.createFolder()
        self.coco_class.start_qwe()
        # self.printImageId()
        self.generateJsonFile()
        self.copy_datasetToModelTraining()

    def generateJsonFile(self):
        with open(os.path.join(self.annotation_folder_path, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(self.coco_class.getJsonFull(), f, ensure_ascii=False, indent=4)
        return self.coco_class.getJsonFull()

    def createFolder(self):
        r = ModelUnetRepository(doctor_id=1)

        if r.get_last_history_train().path_dataset:
            folder_name = str(r.get_last_history_train().path_dataset)
        else:
            folder_name = 'default1111'
        print(folder_name)
        print(r.get_last_history_train())
        self.annotation_folder_path = Path(ROOT_DIR + '/dataset/' + str(folder_name) + '/annotations/')
        self.image_folder_path = Path(ROOT_DIR + '/dataset/' + str(folder_name) + '/image/')
        os.makedirs(self.annotation_folder_path, exist_ok=True)
        os.makedirs(self.image_folder_path, exist_ok=True)
        self.coco_class.set_image_folder_path(self.image_folder_path)

    def copy_datasetToModelTraining(self):
        dataset_folder = os.path.join(ROOT_DIR, 'dataset')

        if os.path.exists(dataset_folder):
            to = os.path.join(ReadXmlProject().path_train_model, 'dataset')
            print(to)
            if os.path.exists(to):
                shutil.rmtree(to)
                shutil.copytree(dataset_folder, to)
            else:
                print('Проверьте xml file, path_train_model')


if __name__ == '__main__':
    p = GenerateJsonFileFromDB()
    # print(p.getAll())
    pass
