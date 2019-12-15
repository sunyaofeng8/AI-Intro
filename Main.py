# -*- coding: utf-8 -*-

import os
import cv2

from client import DL_GAN
from find_faces import Find_faces_and_mark_them
from get_attributes import Attribute
from graphic_interface import PhotoViewer


def get_fps_attrs(fp, number_of_faces):
    fps = ["face/face%d.png" % d for d in range(number_of_faces)]
    faces = [cv2.imread(fps[d]) for d in range(number_of_faces)]
    
    shape = [face.shape[0] * face.shape[1] for face in faces]
    print("shape of each images: ",shape)

    # calculate occu_rate
    raw_img = cv2.imread(fp)
    raw_img_size = raw_img.shape[0] * raw_img.shape[1]
    shape = [size / raw_img_size for size in shape] 

    attrs = [Attribute(fps[d], occu_rate = shape[d]) for d in range(number_of_faces)]

    # change the size of the faces into 128*128
    for d in range(number_of_faces):
        cv2.imwrite(fps[d], cv2.resize(faces[d], (128, 128)))
    
    return fps, attrs


def get_DLGAN():
    DL_GAN('face/face0.png') # The biggest face

    hair = [('black', '黑发'), ('brown', '棕发'), ('blonde', '金发')]
    sex = [('male', '男'), ('female', '女')]

    DLGAN_fps = ['DLGAN/' + h[0] + '-' + s[0] + '.png' for h in hair for s in sex]
    DLGAN_zw = [h[1] + ' ' + s[1] for h in hair for s in sex]
    DLGAN_attrs = [Attribute(fp) for fp in DLGAN_fps]

    return DLGAN_fps, DLGAN_zw, DLGAN_attrs


def show_face(fp): # show faces
    print("======== Display ========")

    number_of_faces = Find_faces_and_mark_them(fp)
    print("the number of faces = %d" % number_of_faces)

    if number_of_faces == 0: # No faces existed
        return 0

    fps, attrs = get_fps_attrs(fp, number_of_faces)
    DLGAN_fps, DLGAN_zw, DLGAN_attrs = get_DLGAN()

    app = PhotoViewer(fps, attrs, DLGAN_fps, DLGAN_zw, DLGAN_attrs)
    app.MainLoop()
    return 1
    

def capture_camera():
    print('====== Photo Time =======')
    os.system('python camera.py') # call camera
    show_face(r'camera/raw.png')


if __name__ == '__main__':
    '''
    You can choose whether use camera or not.
    If you don't want to camera, please specify the file path of the raw image.
    '''

    show_face(r"raw/raw10.jpeg")
    #capture_camera()