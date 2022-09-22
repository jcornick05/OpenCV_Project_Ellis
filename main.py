# Imports
import argparse
import cv2
import imutils
import os

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


# Gets the image from the user
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # The image the user would like to use
winName = "Default" # Name of the window

editPhrase = ["tester", "move"]
EDITED = False
CONTINUE = True
while CONTINUE:
    cv2.imshow(winName, image)
    print("What would you like to do?")
    option = str(input(" --> "))

    if option in editPhrase:
        if option == "tester":
            cv2.createTrackbar('slider', winName, 0, 255, on_change) # Creates the trackbar
        elif option == "move":
            cv2.createTrackbar('rotation', winName, 0, 360, on_change_move) # Creates the trackbar
            cv2.createTrackbar('x', winName, 0, 100, on_change_move) # Creates the trackbar
            cv2.setTrackbarMin('x', winName, -100) # Redefines trackbar bounds
            cv2.createTrackbar('y', winName, 0, 100, on_change_move) # Creates the trackbar
            cv2.setTrackbarMin('y', winName, -100) # Redefines trackbar bounds
            
        cv2.waitKey(0)
        image = updated # Redefines the updated image
        cv2.destroyAllWindows() 
        EDITED = True # Allows the user to save edits

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