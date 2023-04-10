
import cv2
import numpy as np

# w = 1.5, th = 10, blur_size = 5x5, blur_sigma = 2.0
tb_w = 15
tb_th = 10
tb_blur_size = 1
tb_blur_sigma = 20


def do_sharpen():
    global tb_w, tb_th, tb_blur_size, tb_blur_sigma
    global imL, ima, imb

    if tb_initialized:
        w = tb_w / 10.0
        th = tb_th
        blur_size = tb_blur_size * 2 + 3
        blur_sigma = tb_blur_sigma / 10.0

        print(w, th, blur_size, blur_sigma)

        im_blur = cv2.GaussianBlur(imL, (blur_size, blur_size), blur_sigma)
        im_diff = cv2.subtract(imL, im_blur, dtype=cv2.CV_16S)
        im_abs_diff = cv2.absdiff(imL, im_blur)

        cv2.imshow('im', im)
        cv2.imshow('im_blur', im_blur)
        cv2.imshow('im_abs_diff', im_abs_diff)

        im_diff_masked = im_diff.copy()
        im_diff_masked[im_abs_diff < th] = 0
        imL_sharpen = cv2.add(imL, w * im_diff_masked, dtype=cv2.CV_8UC1)

        res_Lab = cv2.merge([imL_sharpen, ima, imb])
        res_bgr = cv2.cvtColor(res_Lab, cv2.COLOR_Lab2BGR)
        cv2.imshow('sharpen', res_bgr)


def on_tb_changed_th(val):
    global tb_th
    tb_th = val
    do_sharpen()


def on_tb_changed_w(pos):
    global tb_w
    tb_w = pos
    do_sharpen()


def on_tb_changed_blur_size(val):
    global tb_blur_size
    tb_blur_size = val
    do_sharpen()


def on_tb_changed_blur_sigma(val):
    global tb_blur_sigma
    tb_blur_sigma = val
    do_sharpen()


# im = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_COLOR)
im = cv2.imread('Hermes_h.jpg', cv2.IMREAD_COLOR)
# im = cv2.imread('webcam_selfie.jpg', cv2.IMREAD_COLOR)
imLab = cv2.cvtColor(im, cv2.COLOR_BGR2Lab)
imL, ima, imb = cv2.split(imLab)

unsharp_masking_kernel = np.array([0, -1, 0, -1, 5, -1, 0, -1, 0]).reshape((3, 3, 1))
sharpened = cv2.filter2D(im, -1, unsharp_masking_kernel)
cv2.imshow('unsharp masking', sharpened)

tb_initialized = False
cv2.imshow('sharpen', im)
cv2.createTrackbar('W', 'sharpen', tb_w, 50, on_tb_changed_w)
cv2.createTrackbar('threshold', 'sharpen', tb_th, 100, on_tb_changed_th)
cv2.createTrackbar('blur size', 'sharpen', tb_blur_size, 10, on_tb_changed_blur_size)
cv2.createTrackbar('blur sigma', 'sharpen', tb_blur_sigma, 50, on_tb_changed_blur_sigma)
tb_initialized = True
do_sharpen()

cv2.waitKey(0)
cv2.destroyAllWindows()
