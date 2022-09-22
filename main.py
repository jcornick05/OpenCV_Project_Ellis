# Imports
from matplotlib import pyplot as plt
import argparse
import cv2
import imutils
import numpy as np

def displayHistogram(image):
    chans = cv2.split(image)
    color = "b", "g", "r"
    plt.figure()
    plt.title("Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    for (chan, color) in zip(chans, color):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color = color)
        plt.xlim([0, 256])

    fig = plt.figure
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    plt.show()

#-----------------------------------------------------------------#

def on_change(val):
    #print(val)
    imageCopy = image.copy()

    cv2.putText(imageCopy, str(val), (0, imageCopy.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4)
    cv2.imshow(winName, imageCopy)

#-----------------------------------------------------------------#

def on_change_move(val):
    #print(val)
    x_val = int(cv2.getTrackbarPos("x", winName))
    y_val = int(cv2.getTrackbarPos("y", winName))
    r_val = int(cv2.getTrackbarPos("rotation", winName))
    #imageCopy = image.copy()
    
    global updated

    rotated = imutils.rotate(image, r_val)
    updated = imutils.translate(rotated, x_val, y_val)

    cv2.imshow(winName, updated)

#-----------------------------------------------------------------#

def on_change_arithmetic(val):
    type = int(cv2.getTrackbarPos("type", winName))
    change_val = int(cv2.getTrackbarPos("change", winName))

    global updated

    if type == 0:
        M = np.ones(image.shape, dtype = "uint8") * change_val
        updated = cv2.add(image, M)
    else:
        M = np.ones(image.shape, dtype = "uint8") * change_val
        updated = cv2.subtract(image, M)

    cv2.imshow(winName, updated)

#-----------------------------------------------------------------#

# Gets the image from the user
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # The image the user would like to use
winName = "Default" # Name of the window

editPhrase = ["tester", "move", "arithmetic"]
EDITED = False
CONTINUE = True
DISPLAY_HIST = False
while CONTINUE:
    cv2.imshow(winName, image)
    print("What would you like to do?")
    option = str(input(" --> ")).lower()

    if option in editPhrase:
        if option == "tester":
            cv2.createTrackbar('slider', winName, 0, 255, on_change) # Creates the trackbar
        elif option == "move":
            cv2.createTrackbar('rotation', winName, 0, 360, on_change_move) # Creates the trackbar
            cv2.createTrackbar('x', winName, 0, 100, on_change_move) # Creates the trackbar
            cv2.setTrackbarMin('x', winName, -100) # Redefines trackbar bounds
            cv2.createTrackbar('y', winName, 0, 100, on_change_move) # Creates the trackbar
            cv2.setTrackbarMin('y', winName, -100) # Redefines trackbar bounds
        elif option == "arithmetic":
            cv2.createTrackbar('type', winName, 0, 1, on_change_arithmetic) # Creates the trackbar
            cv2.createTrackbar('change', winName, 0, 255, on_change_arithmetic) # Creates the trackbar
            
        cv2.waitKey(0)
        image = updated
        # Redefines the updated image
        cv2.destroyAllWindows() 
        EDITED = True # Allows the user to save edits

    elif option == "show histogram":
        displayHistogram(image)
        DISPLAY_HIST = True

    elif option == "save":
        if EDITED:
            print("What would you like to name your image?")
            fname = str(input(" --> "))
            cv2.imwrite("C:/Users/George/OneDrive/Desktop/ADVHCS/projects/OpenCV_Project/edited/" + fname, image) # Saves the edited image
        else:
            print("You haven't changed the image!")

    elif option == "close":
        CONTINUE = False

    else:
        print("Not a valid response!")
        

    
cv2.destroyAllWindows()