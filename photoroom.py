# Imports
from matplotlib import pyplot as plt
import argparse
import cv2
import imutils
import numpy as np

#-----------------------------------------------------------------------------#

def getNumVersion(list):
    """
    Purpose: Returns numeric version of a given list
    Parameters: A list to evaluate (list)
    Return VAL: A list of numbers (list)
    """
    listNums = []
    for i in range(len(list)):
        listNums.append(str(i + 1))
    return listNums

def getInput(choices, choiceNums):
    """
    Purpose: Get user input for a given list of options
    Parameters: The two lists defining input options, one of the strings (list) 
    and one of the numeric values that represent those strings (list)
    Return VAL: The user's desired choice
    """
    helpTracker = 0
    while True:
        choice = str(input(" --> ")).lower()
        if choice in ["options", "see options", "help", "h"]:
            print("Your possible choices are the following:")
            for i in range(len(choices)):
                print(str(i+1) + ") " + choices[i])
        elif choice in choices:
            return choice
        elif choice in choiceNums:
            return choices[int(choice)-1]
        else:
            print("Please enter a valid option!")
            helpTracker += 1
            if helpTracker >= 3:
                print("You can see all your options by entering 'Options'")

#-----------------------------------------------------------------------------#

def displayHistogram(image):
    """
    Purpose: Display a histogram for a given image using opencv
    Parameters: The image to display a histogram of
    Return VAL: None
    """
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

#-----------------------------------------------------------------------------#

def getDrawingData(winName):
    """
    Purpose: Get the slider values for color and radius in a certain window
    Parameters: The window in which the sliders reside
    Return VAL: The selected color and selected radius
    """
    r = int(cv2.getTrackbarPos("r", winName))
    g = int(cv2.getTrackbarPos("g", winName))
    b = int(cv2.getTrackbarPos("b", winName))
    radius = int(cv2.getTrackbarPos("radius", winName))
    return (b, g, r), radius

#-----------------------------------------------------------------------------#

def draw_dot(event, x, y, flags, param):
    """
    Purpose: Draws a dot on the screen for a give point if the players clicks
    and then shows the new image
    Parameters: The mouse click event, the x and y value of the mouse, any flags
    or other paramters
    Return VAL: None
    """
    global DRAWING, updated
    updated = image
    color, radius = getDrawingData(winName)
    try:
        if event == cv2.EVENT_LBUTTONUP:
            DRAWING = False
        elif event == cv2.EVENT_LBUTTONDOWN or DRAWING:
            cv2.circle(updated, (x,y), radius, color, -1)
            DRAWING = True
    except:
        DRAWING = False

    cv2.imshow(winName, updated)

#-----------------------------------------------------------------------------#

def on_change_nothing(val):
    """
    Purpose: Has no action but exists for sliders that don't need a normal 
    on_change function
    Parameters: The slider val
    Return VAL: None
    """
    pass

#-----------------------------------------------------------------------------#

def on_change_move(val):
    """
    Purpose: Moves image position based on slider values
    Parameters: The slider val
    Return VAL: None
    """
    x_val = int(cv2.getTrackbarPos("x", winName))
    y_val = int(cv2.getTrackbarPos("y", winName))
    r_val = int(cv2.getTrackbarPos("rotation", winName))
    
    global updated

    rotated = imutils.rotate(image, r_val)
    updated = imutils.translate(rotated, x_val, y_val)

    cv2.imshow(winName, updated)

#-----------------------------------------------------------------------------#

def on_change_arithmetic(val):
    """
    Purpose: Changes arithmetic values of the image based on slider values
    Parameters: The slider val
    Return VAL: None
    """
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

#-----------------------------------------------------------------------------#

def on_change_blur(val):
    """
    Purpose: Blurs the image based on slider values
    Parameters: The slider val
    Return VAL: None
    """
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

#-----------------------------------------------------------------------------#

def on_change_sharpen(val):
    """
    Purpose: Sharpens image based on slider values 
    Parameters: The slider val
    Return VAL: None
    """
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

#-----------------------------------------------------------------------------#

def on_change_threshold(val):
    """
    Purpose: Thresholds the image based on slider values
    Parameters: The slider val
    Return VAL: None
    """
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

#-----------------------------------------------------------------------------#

def on_change_edge(val):
    """
    Purpose: Applies various forms of edging based on slider values
    Parameters: The slider val
    Return VAL: None
    """
    blur = int(cv2.getTrackbarPos("blur", winName))
    low = int(cv2.getTrackbarPos("low thresh", winName))
    high = int(cv2.getTrackbarPos("high thresh", winName))
    contour = int(cv2.getTrackbarPos("contours", winName))
    global updated

    converted = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Corrects the blur
    if blur == 0:
        blurred = image
    else:
        if (blur % 2) == 0:
            blur -= 1
            cv2.setTrackbarPos("blur", winName, blur)
        blurred = cv2.GaussianBlur(converted, (blur, blur), 0)
    
    # Adds contours if necessary
    if contour == 0:
        updated = cv2.Canny(blurred, low, high)
        newState = "contours off"
    elif contour == 1:
        edged = cv2.Canny(blurred, low, high)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        updated = image.copy()
        cv2.drawContours(updated, cnts, -1, (255, 0, 0), 2)
        newState = "contours on"
    
    cv2.imshow(winName, updated)

#-----------------------------------------------------------------------------#

def on_change_cartoon(val):
    """
    Purpose: Applies a cartoon effect to the image the user choose to turn it on
    Parameters: The slider val
    Return VAL: None
    """
    if val == 1:
        global updated

        edges = cv2.bitwise_not(cv2.Canny(image, 100, 200))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        dst = cv2.edgePreservingFilter(image, flags=2, sigma_s=64, sigma_r=0.25)
        updated = cv2.bitwise_and(dst, dst, mask=edges)

        cv2.imshow(winName, updated)
    else:
        cv2.imshow(winName, image)

#-----------------------------------------------------------------------------#
   
def on_change_sketch(val):
    """
    Purpose: Applies a sketch effect to the image based on slider values
    Parameters: The slider val
    Return VAL: None
    """
    type = int(cv2.getTrackbarPos("color", winName))
    sigma_s = int(cv2.getTrackbarPos("neighborhood", winName))
    sigma_r = int(cv2.getTrackbarPos("averaging", winName))
    shade_factor = int(cv2.getTrackbarPos("shade", winName))

    gray_sketch, color_sketch = cv2.pencilSketch(image, sigma_s = sigma_s, 
                                                 sigma_r = sigma_r/100, 
                                                 shade_factor = shade_factor/100)

    global updated

    if type == 1:
        updated = color_sketch
    else:
        updated = gray_sketch

    cv2.imshow(winName, updated)

#-----------------------------------------------------------------------------#

# Gets the image from the user
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])           # The image the user would like to use
winName = "Window"                          # Name of the window

# Lists of options
initialOptions = ["edit", "data", "save", "quit"]
initialNums = getNumVersion(initialOptions)
editOptions = ["draw", "move", "arithmetic", "blur", "sharpen", "threshold", 
               "edges", "cartoon", "sketch", "back"]
editNums = getNumVersion(editOptions)
dataOptions = ["show histogram", "back"]
dataNums = getNumVersion(dataOptions)


# State tracking variables
EDITED = False
CONTINUE = True

# Main loop
while CONTINUE:
    cv2.imshow(winName, image)              # Displays the window
    print("\n  -- MAIN MENU --\n")          # UI Display
    print("What would you like to do?")     # User prompt
    option = getInput(initialOptions, initialNums)        # Gets the user's input

    # Checks if the user would like to edit their image
    if option == "edit":
        print("\n  -- EDIT MENU --\n")
        option = getInput(editOptions, editNums)
        if option == "draw":
            # Creates the necessary trackbars and sets up moue function
            cv2.setMouseCallback(winName, draw_dot)
            cv2.createTrackbar('r', winName, 0, 255, on_change_nothing)
            cv2.createTrackbar('g', winName, 0, 255, on_change_nothing)
            cv2.createTrackbar('b', winName, 0, 255, on_change_nothing)
            cv2.createTrackbar('radius', winName, 0, 10, on_change_nothing)
        elif option == "move":
            # Creates the necessary trackbars and redefines their bounds
            cv2.createTrackbar('rotation', winName, 0, 360, on_change_move) 
            cv2.createTrackbar('x', winName, 0, 100, on_change_move) 
            cv2.setTrackbarMin('x', winName, -100) 
            cv2.createTrackbar('y', winName, 0, 100, on_change_move) 
            cv2.setTrackbarMin('y', winName, -100) 
        elif option == "arithmetic":
            # Creates the necessary trackbars
            cv2.createTrackbar('type', winName, 0, 1, on_change_arithmetic)
            cv2.createTrackbar('change', winName, 0, 255, on_change_arithmetic)
        elif option == "blur":
            # Creates the necessary trackbars
            cv2.createTrackbar('type', winName, 0, 2, on_change_blur)
            cv2.createTrackbar('intensity', winName, 0, 15, on_change_blur)
        elif option == "sharpen":
            # Creates the necessary trackbars
            cv2.createTrackbar('range', winName, 0, 15, on_change_sharpen)
            cv2.createTrackbar('intensity', winName, 0, 51, on_change_sharpen)
        elif option == "threshold":
            # Creates the necessary trackbars
            cv2.createTrackbar('type', winName, 0, 2, on_change_threshold)
            cv2.createTrackbar('blur', winName, 0, 51, on_change_threshold)
        elif option == "edges":
            # Creates the necessary trackbars
            cv2.createTrackbar('blur', winName, 0, 51, on_change_edge)
            cv2.createTrackbar('low thresh', winName, 0, 1000, on_change_edge)
            cv2.createTrackbar('high thresh', winName, 0, 1000, on_change_edge) 
            cv2.createTrackbar('contours', winName, 0, 1, on_change_edge) 
        elif option == "cartoon":
            cv2.createTrackbar('on/off', winName, 0, 1, on_change_cartoon)
        elif option == "sketch":
            cv2.createTrackbar('color', winName, 0, 1, on_change_sketch)
            cv2.createTrackbar('neighborhood', winName, 0, 200, on_change_sketch)
            cv2.createTrackbar('averaging', winName, 0, 10, on_change_sketch)
            cv2.createTrackbar('shade', winName, 0, 10, on_change_sketch)
        elif option == "back":
            pass
        else:
            print("ERROR: Recieved a 'valid' input with no function")
        
        cv2.waitKey(0)
        try:
            image = updated                 # Redefines the updated image
            EDITED = True                   # Allows the user to save edits
        except:
            pass

        cv2.destroyAllWindows() 
        
    # Checks if the user would like to view the images data
    elif option == "data":
        print("\n  -- DATA MENU --\n")      # Display
        option = getInput(dataOptions, dataNums)      # Recieves the user input
        if option == "show histogram":
            displayHistogram(image)         # Displays the histogram if chosen
        elif option == "back":
            pass
        else:
            print("ERROR: Recieved a 'valid' input with no function")

    # Checks if the user would like save the image
    elif option == "save":
        # Only lets the user save their image if it is edited
        if EDITED:
            # Gets the desired filename and saves it
            print("What would you like to name your image?")
            fname = str(input(" --> "))
            cv2.imwrite("edited/" + fname, image)
        else:
            print("You haven't changed the image!")

    # Checks if the user would like to quit
    elif option == "quit":
        CONTINUE = False

    # Displays error message if input is recieved but no action is take
    else:
        print("ERROR: Recieved a 'valid' input with no function")
        
cv2.destroyAllWindows()                     # Dstroys all remaining windows