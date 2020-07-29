from hashlib import md5
import os
from PIL import Image
from catdog import app, r


def save_picture(picture_data, req_ip): #todo 2MB limit  #todo chack magic bytes?/try except on open
    picture_name = md5(req_ip.encode()).hexdigest()
    picture_path = os.path.join(app.root_path, 'static', 'user_pictures', picture_name)
    img = Image.open(picture_data)
    img.convert('RGB').save(picture_path+'.jpg', quality=95)
    return picture_name+'.jpg'


def detect_wraper(picture_name):
    detection = detect_animal(picture_name)
    r.hset('picture_detaction', picture_name, detection)
    return


def detect_animal(picture_name):
    from imageai.Detection import ObjectDetection

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(app.root_path, "models", "yolo.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(app.root_path, 'static', 'user_pictures'
                                                                                , picture_name),
                                                 output_image_path=os.path.join(app.root_path, 'static', 'user_pictures'
                                                                                , "imagenew.jpg"),
                                                 minimum_percentage_probability=30)
    predictlist = [i['name'] for i in detections]
    for predict in predictlist:
        if predict.lower() == 'cat':
            return 'cat'
        if predict.lower() == 'dog':
            return 'dog'
    else:
        return "Not a cat or a dog!"