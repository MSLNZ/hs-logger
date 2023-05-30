import cv2
import pytesseract
import time
import take_image as ti


def readImage(filename, init, nr_par):

    global boxes
    ocr_text = ""

    im, t, boxes = ti.take_image(init)
    im_data = im.copy()
    # directory for tesseract installation
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\b.sherson.CI\AppData\Local\Tesseract-OCR\tesseract.exe'
    # restricting the character set helps a lot here
    custom_config = r'-c tessedit_char_whitelist=-1234567890. --oem 3 --psm 8 outputbase digits'

    for i in range(int(len(boxes)/2)):

        image = im[boxes[2 * i][1]:boxes[2 * i + 1][1], boxes[2 * i][0]:boxes[2 * i + 1][0]]
        cv2.imshow(f"Humiditylog{i}", image)
        cv2.imwrite(f"Humiditylog{i}{t}.jpg", image)
        cv2.waitKey(1)
        ocr_text_1 = pytesseract.image_to_string(image, config=custom_config)
        print(f'ocr_text_1 = {ocr_text_1}')
        ocr_text = ocr_text + ocr_text_1.replace("\n", "\t")

    return ocr_text


if __name__ == '__main__':
    i = 0
    read_freq = 3  # in seconds
    parameter_list = ["RH", "T"]
    nr_par = len(parameter_list)

    filename = "test"
    textfile = open(f'{filename}_data.tsv', 'a')
    textfile.write(f'frame number\t{parameter_list[0]}\t{parameter_list[1]}\tTimestamp String\tData_OCR\n')
    textfile.close()

    while i < 10:
        time.sleep(3)
        ocr_text = readImage(filename, not bool(i), nr_par)
        i = i + 1
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        textfile = open(f'{filename}_data.tsv', 'a')
        textfile.write(f'{i}\t{current_time}\t{ocr_text}\n')
        textfile.close()

    textfile.close()
