# -*- coding: utf-8 -*-

import cv2
from facepp_API import connect_to_facepp


def Find_faces_and_mark_them(filepath):
    '''
    Given a raw picture with pixel 1280*960 or 640*480,
    this function would find all the faces,
    then save each face as file 'face/face0.png', 'face/face1.png' .....
    then mark the face boxes in the 'face/marked.png'
    '''

    def get_position(img, face):
        '''
        Given a image and the json file (generated by Face++), return the coordinates of the face
        The left-top point locates at (x1, y1), and the width and the height are both s.
        '''

        rectangle = face['face_rectangle']
        x1, y1= rectangle['top'], rectangle['left']
        s = max(rectangle['width'], rectangle['height'])
        s = s // 6 * 5

        x1 = x1 - (s // 3 * 2)
        x2 = x1 + s * 2
        x1, x2 = max(x1, 0), min(x2, img.shape[0])

        y1 = y1 - (s // 2)
        y2 = y1 + s * 2
        y1, y2 = max(y1, 0), min(y2, img.shape[1])
        
        s = min(x2 - x1, y2 - y1)

        return x1, y1, s
    
    def pre_treat_marked_img(img):
        '''
        since marked image is 430 * 320, this function would resize it and save it as 'face/marked.png'
        '''
        marked_img = img.copy()
        H = marked_img.shape[0]
        W = marked_img.shape[1]
        portion = max(1.0, H / 320)

        if H > 320:
            W = int(W / H * 320)
            H = 320
            
        marked_img = cv2.resize(marked_img, (W, H))
        cv2.imwrite('face/marked.png', marked_img)

        return portion

    # Begin
    faces = connect_to_facepp(filepath)
    if len(faces) == 0:
        return 0 # No faces existed
    
    img = cv2.imread(filepath)
    portion = pre_treat_marked_img(img) # resize Marked image
    marked_img = cv2.imread('face/marked.png')
    color = (0, 255, 0) # Green Line

    print("raw image: ", img.shape)

    faces_img = []
    for face in faces:
        x1, y1, s = get_position(img, face)
        faces_img.append(img[x1 : x1+s, y1 : y1+s])
    
        x1, y1, s = int(x1 / portion), int(y1/portion), int(s/portion)
        
        # Mark faces with green border
        marked_img[x1, y1:y1+s] = color
        marked_img[x1+s-1, y1:y1+s] = color
        marked_img[x1:x1+s, y1] = color
        marked_img[x1:x1+s, y1+s-1] = color

    # sort all the faces by their size, and only store the top 4 biggest faces.
    faces_img.sort(key = lambda face: face.shape[0] * face.shape[1], reverse=True)
    faces_img = faces_img[:4]

    for d, face in enumerate(faces_img):
        cv2.imwrite('face/face%d.png' % d, face)

    cv2.imwrite('face/marked.png', marked_img)
    return len(faces_img)


if __name__ == '__main__':
    Find_faces_and_mark_them('raw/raw1.jpeg')