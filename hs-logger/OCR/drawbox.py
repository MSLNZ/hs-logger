import cv2
from time import time


def drawbox(img):
    global crop
    crop = img
    global boxes
    boxes = []

    def on_mouse(event, x, y, flags, params):
        # global img
        t = time()
        crop = img
        if event == cv2.EVENT_LBUTTONDOWN:
            print('Start Mouse Position: ' + str(x) + ', ' + str(y))
            sbox = [x, y]
            boxes.append(sbox)
            # print(count)
            # print(sbox)

        elif event == cv2.EVENT_LBUTTONUP:
            print('End Mouse Position: ' + str(x) + ', ' + str(y))
            ebox = [x, y]
            boxes.append(ebox)
            print(boxes)
            crop = img[boxes[-2][1]:boxes[-1][1], boxes[-2][0]:boxes[-1][0]]

            cv2.imshow('crop', crop)
            k = cv2.waitKey(0)

            if ord('r') == k:
                cv2.imwrite('Crop' + str(t) + '.jpg', crop)
                print("Written to file")

    i = 1
    while i == 1:
        # img = cv2.blur(img, (3, 3))
        img = cv2.resize(img, None, fx=1, fy=1)

        cv2.namedWindow('real image')
        cv2.setMouseCallback('real image', on_mouse, 0)
        cv2.imshow('real image', img)
        if cv2.waitKey(33) == 27:
            cv2.destroyAllWindows()
            i = 0

        if cv2.waitKey(0) == 27:
            cv2.destroyAllWindows()
            i = 0

    return crop, boxes


# if __name__ == '__main__':
#    img = cv2.imread('lena.jpg',0)
