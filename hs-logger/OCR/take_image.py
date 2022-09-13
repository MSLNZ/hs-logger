import cv2
import drawbox as db
from time import time

def take_image(init):
    global boxes
    # initialize the camera
    # If you have multiple camera connected with
    # current device, assign a value in cam_port
    # variable according to that
    cam_port = 0
    cam = cv2.VideoCapture(cam_port, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1800)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1600)
    if init:
        print("Frame default resolution: (" + str(cam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "; " + str(
            cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) + ")")
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1800)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1600)
        print("Frame resolution set to: (" + str(cam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "; " + str(
            cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) + ")")

    # reading the input using the camera
    result, image = cam.read()

    # If image will detected without any error,
    # show result

    if result:
        # saving image in local storage
        t = time()

        if init:
            image, boxes = db.drawbox(image)
            cv2.imwrite(f"Humiditylog{t}.jpg", image)

        # showing result, it take frame name and image
        # output
        #
        # If keyboard interrupt occurs, destroy image
        # window
        #

    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")

    return image, t, boxes


if __name__ == '__main__':
    take_image()
