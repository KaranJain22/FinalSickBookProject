'''
This code is meant to run on a server so that large amount of data can be effectively
processed as our group's computers are relatively weak and will not be able
to keep up with a large amount of users like 400+ users that a server will easily be able to handle
A Personal Computer can be a server for this code
'''


from time import sleep

import firebase_admin
from firebase_admin import credentials
from FaceAI import MaskDetector
from firebase_admin import db

# This gives is establishes the server as a trusted device for firebase by using the credentials firebase json file
cred = \
    credentials.Certificate('sickbook-56291-firebase-adminsdk-6ckct-8091676728.json')

'''
This initiates where the firebase is stored and connect the credibility json file to the firebase which allows for
the reading and writing of firebase data
'''
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://sickbook-56291-default-rtdb.firebaseio.com/'
                               })
# This code has to constantly run in order to mimic a server and checks for any updates to the firebase
while True:
    sleep(1)  # This one second sleep is to make sure
    # the firebase had enough time to update and makes sure that the server is not being over worked

    root = db.reference()
    (data, a) = root.get(
        'people')  # This gets all the data from the people key in the firebase dictionary data structure

    links = []  # This is where the links to the images will be stored
    paths = []  # This is where the firebase fire path to a specific person lies

    # This for loop is to get the face image links and the firebase paths for every person in firebase
    # A nested for loop is used as the data is stored as a python dictionary in a python dictionary
    for first in data:

        for second in data[first]:

            # This it to make sure that there is a new face image to apply the AI to and that server resources are
            # not wasted on applying the AI to images that already have had the AI applied to them

            try:
                if data[first][second]['new'] is None or data[first][second]['new'] \
                        == 'true':
                    links.append(data[first][second]['faceimg'])  # This is the specific link string to the the temporary face image link that is in firebase
                    paths.append('people/' + second)  # The path in the firebase is stored which will allow for changing of the infomation of in the path
            except:
                if data[first][second]['faceimg'] is not None: # if there is no image then no detection can happen
                    links.append(data[first][second]['faceimg'])
                    paths.append('people/' + second)

    detector = MaskDetector(links)  # the AI Mask Detector system is used for all the links obtained by the parsing of firebase

    bools = detector.areMasksOn()  # boolean array that store is a mask was on or not and is parallel to paths

    index = 0
    # This updates all the information that needs to be updated from the path
    # This write new information in firebase
    for first in paths:
        db.reference(first).update({'MaskOn': str(bools[index])})
        db.reference(first).update({'new': 'false'})
        index += 1
