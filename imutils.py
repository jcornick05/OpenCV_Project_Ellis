import numpy as np
import cv2

def translate(image, x, y):
    M = np.float32([[1,0,x],[0,1,y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return shifted

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is not None and height is not None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)

    return resized

def grab_contours(cnts):
	# if the length the contours tuple returned by cv2.findContours
	# is '2' then we are using either OpenCV v2.4, v4-beta, or
	# v4-official
	if len(cnts) == 2:
		cnts = cnts[0]

	# if the length of the contours tuple is '3' then we are using
	# either OpenCV v3, v4-pre, or v4-alpha
	elif len(cnts) == 3:
		cnts = cnts[1]

	# otherwise OpenCV has changed their cv2.findContours return
	# signature yet again and I have no idea WTH is going on
	else:
		raise Exception(("Contours tuple must have length 2 or 3, "
			"otherwise OpenCV changed their cv2.findContours return "
			"signature yet again. Refer to OpenCV's documentation "
			"in that case"))

	# return the actual contours array
	return cnts