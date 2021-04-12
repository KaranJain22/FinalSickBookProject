from tensorflow.keras.models import load_model

model = load_model('modelss-020.model')  # This the trained AI

import numpy as np

import cv2
import urllib
import urllib.request


# The MaskDetector class is the class where the trained AI is applied
class MaskDetector:
    labels_dict = {0: False, 1: True}  # False means that the the mask was not on. True means mask on
    img_size = 150  # The model was trained on 150x150px sized images so the image size must be scaled to that
    color_dict = {0: (0, 0, 255), 1: (0, 255, 0)}

    def __init__(self, imglinks):
        self.links = imglinks

    # This methods converts links into usable, real, images
    def url_to_image(self, url):
        # the url is opened then the image is read but NOT downloaded
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image

    # This goes through all the links to see which contain images with masks an which do not
    def areMasksOn(self):
        maskOn = []  # This is where the booleans if the mast is on or off is stored
        for i in self.links:
            # First, the URL gets converted to an image then the predication is made
            img = self.url_to_image(i)

            maskOn.append(self.predictMask(img))

        return maskOn

    # This uses to AI to predict if the image had a fac wearing a mask
    def predictMask(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_img = gray  # a grayscale image is used at the model was trained on one channel (grayscale) images

        # The image is then processed to mimic the images the model was trained on
        resized = cv2.resize(face_img, (self.img_size, self.img_size))
        normalized = resized / 255.0  # This is the normalized image to prevent any overflow errors from occuring

        # the image is now reshaped to an image that has the exact same shape as the trainign data images
        reshaped = np.reshape(normalized, (1, self.img_size, self.img_size, 1))

        # The model then predicts the if the mask was on or off and
        # it gives a confidence score that corresponds to 0 if the mask was off and to a 1 if the mask was on
        result = model.predict(reshaped)

        # This returns a boolean by using the labels_dict dictionary and finding
        # what the AI thought that was the most probable and therefore finding either a 0 or a 1
        return self.labels_dict[np.argmax(result, axis=1)[0]]

    def quit(self):
        quit()
