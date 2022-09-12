import argparse
import cv2

def on_change(val):
    print(val)
    
    imageCopy = image.copy()

    cv2.putText(imageCopy, str(val), (0, imageCopy.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4)
    cv2.imshow(winName, imageCopy)

# Gets the image from the user
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # The image the user would like to use

winName = "Default"

cv2.imshow(winName, image)
cv2.createTrackbar('slider', winName, 0, 255, on_change) # Creates the trackbar

cv2.waitKey(0)
cv2.destroyAllWindows()