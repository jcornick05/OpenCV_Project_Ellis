# Imports
from matplotlib import pyplot as plt
import argparse
import cv2
import imutils
import numpy as np

#-----------------------------------------------------------------#

def getInput(choices):
    helpTracker = 0
    while True:
        choice = str(input(" --> ")).lower()
        if choice in ["options", "see options", "help", "h"]:
            print("Your possible choices are the following:")
            for i in range(len(choices)):
                print(str(i+1) + ") " + choices[i])
        elif choice in choices:
            return choice
        else:
            print("Please enter a valid option!")
            helpTracker += 1
            if helpTracker >= 3:
                print("You can see all your options by entering 'Options'")

#-----------------------------------------------------------------#

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

def on_change_blur(val):
    type = int(cv2.getTrackbarPos("type", winName))
    intensity = int(cv2.getTrackbarPos("intensity", winName))

    global updated

    if intensity == 0:
        updated = image
    else:
        if type == 0:
            updated = cv2.blur(image, (intensity, intensity))
        elif type == 1:
            if (intensity % 2) == 0:
                intensity -= 1
                cv2.setTrackbarPos("intensity", winName, intensity)

            updated = cv2.GaussianBlur(image, (intensity, intensity), 0)
        else:
            if (intensity % 2) == 0:
                intensity -= 1
                cv2.setTrackbarPos("intensity", winName, intensity)

            updated = cv2.medianBlur(image, intensity)
            

    cv2.imshow(winName, updated)


#-----------------------------------------------------------------#

def on_change_sharpen(val):
    range = int(cv2.getTrackbarPos("range", winName))
    intensity = int(cv2.getTrackbarPos("intensity", winName))

    global updated

    if intensity == 0:
        updated = image
    else:
        if (intensity % 2) == 0:
                intensity -= 1
                cv2.setTrackbarPos("intensity", winName, intensity)

        updated = cv2.bilateralFilter(image, range, intensity, intensity)

    cv2.imshow(winName, updated)

#-----------------------------------------------------------------#

def on_change_threshold(val):
    type = int(cv2.getTrackbarPos("type", winName))
    blur = int(cv2.getTrackbarPos("blur", winName))

    global updated

    converted = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if blur == 0:
        blurred = image
    else:
        if (blur % 2) == 0:
            blur -= 1
            cv2.setTrackbarPos("blur", winName, blur)
        blurred = cv2.GaussianBlur(converted, (blur, blur), 0)

    if type == 0:
        (T, updated) = cv2.threshold(blurred, 155, 255, cv2.THRESH_BINARY_INV)
    elif type == 1:
        (T, updated) = cv2.threshold(blurred, 155, 255, cv2.THRESH_BINARY)
    else:
        (T, threshInv) = cv2.threshold(blurred, 155, 255, cv2.THRESH_BINARY_INV)
        updated = cv2.bitwise_and(image, image, mask = threshInv)

    cv2.imshow(winName, updated)

#-----------------------------------------------------------------#

# Gets the image from the user
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])           # The image the user would like to use
winName = "Default"                         # Name of the window

# Lists of options
editOptions = ["tester", "move", "arithmetic", "blur", "sharpen", "threshold", "back"]
intialOptions = ["edit", "data", "save", "quit"]
dataOptions = ["show histogram", "back"]

# State tracking variables
EDITED = False
CONTINUE = True
DISPLAY_HIST = False

# Main loop
while CONTINUE:
    cv2.imshow(winName, image)              # Displays the window
    print("\n  -- MAIN MENU --\n")          # UI Display
    print("What would you like to do?")     # User prompt
    option = getInput(intialOptions)        # Gets the user's input

    # Checks if the user would like to edit their image
    if option == "edit":
        print("\n  -- EDIT MENU --\n")
        option = getInput(editOptions)
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
        elif option == "blur":
            cv2.createTrackbar('type', winName, 0, 2, on_change_blur) # Creates the trackbar
            cv2.createTrackbar('intensity', winName, 0, 15, on_change_blur) # Creates the trackbar
        elif option == "sharpen":
            cv2.createTrackbar('range', winName, 0, 15, on_change_sharpen) # Creates the trackbar
            cv2.createTrackbar('intensity', winName, 0, 51, on_change_sharpen) # Creates the trackbar
        elif option == "threshold":
            cv2.createTrackbar('type', winName, 0, 2, on_change_threshold) # Creates the trackbar
            cv2.createTrackbar('blur', winName, 0, 51, on_change_threshold) # Creates the trackbar
        #elif option == "back":
            #pass
        else:
            print("ERROR: Recieved a 'valid' input with no function")
        
        cv2.waitKey(0)
        try:
            image = updated
        except:
            pass
        # Redefines the updated image
        cv2.destroyAllWindows() 
        EDITED = True # Allows the user to save edits

    # Checks if the user would like to view the images data
    elif option == "data":
        print("\n  -- DATA MENU --\n")
        option = getInput(dataOptions)
        if option == "show histogram":
            displayHistogram(image)
            DISPLAY_HIST = True
        elif option == "back":
            pass
        else:
            print("ERROR: Recieved a 'valid' input with no function")

    # Checks if the user would like save the image
    elif option == "save":
        if EDITED:
            print("What would you like to name your image?")
            fname = str(input(" --> "))
            cv2.imwrite("C:/Users/George/OneDrive/Desktop/ADVHCS/projects/OpenCV_Project/edited/" + fname, image) # Saves the edited image
        else:
            print("You haven't changed the image!")

    # Checks if the user would like to quit
    elif option == "quit":
        CONTINUE = False

    # Displays error message if input is recieved but no action is take
    else:
        print("ERROR: Recieved a 'valid' input with no function")
        

    
cv2.destroyAllWindows()