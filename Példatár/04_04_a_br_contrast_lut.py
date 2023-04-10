
# https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/

import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

global img, new_image
global brightness, contrast


def get_diagram_as_image(in_fig):
    in_fig.canvas.draw()
    data = np.frombuffer(in_fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(in_fig.canvas.get_width_height()[::-1] + (3,))
    data_bgr = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

    return data_bgr


def do_brightness_contrast():
    global brightness, contrast, new_image

    print('======================')
    print('Brightness:', brightness)
    print('Contrast:', contrast)

    factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
    print('Factor:', factor)

    start_time = time.perf_counter()
    # Iteratív képpont bejárással
    # for y in range(img.shape[0]):
    #     for x in range(img.shape[1]):
    #         for c in range(img.shape[2]):
    #            new_image[y, x, c] = np.clip(brightness + factor * (img[y, x, c] - 128) + 128, 0, 255)
    # end_time = time.perf_counter()

    # Numpy tömb aritmetikával
    # new_image = np.uint8(np.clip(brightness + factor * (np.float32(img) - 128.0) + 128, 0, 255))
    # end_time = time.perf_counter()

    # OpenCV keresőtáblával
    x = np.arange(0, 256, 1)
    lut = np.uint8(np.clip(brightness + factor * (np.float32(x) - 128.0) + 128, 0, 255))
    new_image = cv2.LUT(img, lut)
    end_time = time.perf_counter()

    print((end_time - start_time) * 1000.0, 'ezredmásodperc')

    ax.clear()
    x = np.arange(0, 256, 1)
    ax.plot(x, x, 'g--', label='Eredeti', linewidth=2)
    ax.plot(x, lut, 'r-', label='Fényesség/kontraszt leképezés', linewidth=2)
    plt.legend()

    lut_im = get_diagram_as_image(fig)
    cv2.imshow('LUT', lut_im)

    cv2.imshow("before", img)
    cv2.imshow("after", new_image)


def on_trackbar_brightness(br):
    global brightness
    brightness = br - 255
    do_brightness_contrast()


def on_trackbar_contrast(cntr):
    global contrast
    contrast = cntr - 255
    do_brightness_contrast()


if __name__ == '__main__':
    # fname = 'SeaCliffBridge_1_800.jpg'
    fname = 'hk_flower_h.jpg'
    img = cv2.imread(fname)
    new_image = img.copy()

    print(img.shape)

    # Grafikon beállítások
    fig = plt.figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    plt.xlabel('Eredeti intenzitásérték')
    plt.ylabel('Pont operáció eredménye')
    plt.xlim([0, 255])
    # plt.ylim([0, 255])

    brightness = 0
    contrast = 0
    cv2.imshow("before", img)
    cv2.imshow("after", img)
    cv2.createTrackbar('Brightness', 'after', 255, 511, on_trackbar_brightness)
    cv2.createTrackbar('Contrast', 'after', 255, 511, on_trackbar_contrast)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
