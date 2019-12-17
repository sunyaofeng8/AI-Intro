# -*- coding: utf-8 -*-

import cv2


def change_into_640_480(img): # change size of the raw image into 640 * 480
    por = min(img.shape[1] / img.shape[0], 640 / 480)
    len = int(por * img.shape[0]) // 2
    mid = img.shape[1] // 2
    img = img[:,mid - len : mid + len]

    img = cv2.resize(img, (640, 480))
    return img


def capture_camera():
    capture = cv2.VideoCapture(0) # Capture Video

    # a window used to display video
    window_name = 'Press "s" to save this photo!'
    cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(window_name, 300, 100)

    while (True):
        ret, img = capture.read()
        img = change_into_640_480(img)

        cv2.imshow(window_name, img) # show images
        res = cv2.waitKey(1)

        # if user press 's' in the keyborad, the images would be saved.
        if res == ord('s'):
            cv2.imwrite('camera/raw.png', img)
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    capture_camera()