# Virtuel Calculator by EMAN SARFRAZ

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import math

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Calculator Layout
display_top_left = (50, 50)
display_bottom_right = (750, 130)

# Buttons now start lower, with added vertical margin (start_y offset)
start_y = 170
keys = [["7", "8", "9", "/", "!"], 
        ["4", "5", "6", "*", "pow"],
        ["1", "2", "3", "-", "."],
        ["C", "0", "=", "+", "←"]]

finalText = ""  # Stores the user input
clickDetected = False  # Prevents multiple clicks

class Button:
    def __init__(self, pos, text, size=[90, 90]):
        self.pos = pos
        self.size = size
        self.text = text
        self.defaultColor = (100, 100, 250)
        self.hoverColor = (150, 150, 255)
        self.clickColor = (255, 0, 100)

# Create Button Objects
buttonList = []
padding = 20  # Space between buttons
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        x = 50 + j * (90 + padding)
        y = start_y + i * (90 + padding)
        buttonList.append(Button([x, y], key))

# Function to draw the display on the screen
def drawDisplay(img, text):
    # Draw the display area (background color + border)
    cv2.rectangle(img, display_top_left, display_bottom_right, (50, 50, 200), cv2.FILLED)
    cv2.rectangle(img, display_top_left, display_bottom_right, (255, 255, 255), 3)
    
    # Add the text (calculation result or user input)
    cv2.putText(img, text, (display_top_left[0] + 10, display_bottom_right[1] - 20),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    return img

# Function to draw all buttons on the screen
def drawAll(img, buttonList, finalText):
    img = drawDisplay(img, finalText)  # Draw the display at the top
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw the button background with color
        cv2.rectangle(img, (x, y), (x + w, y + h), button.defaultColor, cv2.FILLED)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)  # Draw rounded corners for buttons
        
        # Center the button text
        textSize = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 3, 4)[0]
        textX = x + (w - textSize[0]) // 2
        textY = y + (h + textSize[1]) // 2
        cv2.putText(img, button.text, (textX, textY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
    return img

# Function to calculate factorial
def factorial(n):
    """Function to calculate factorial."""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror effect for natural interaction
    img = detector.findHands(img)  # Detect hands
    lmList, bboxInfo = detector.findPosition(img)  # Get hand landmarks
    img = drawAll(img, buttonList, finalText)  # Draw everything on the image

    if lmList:
        l, _, _ = detector.findDistance(8, 12, img, draw=False)  # Measure the distance between the thumb and index finger
        buttonProcessed = False

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if the index finger is over a button
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x, y), (x + w, y + h), button.hoverColor, cv2.FILLED)  # Hover effect
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
                cv2.putText(img, button.text, (x + 25, y + 60),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)

                # Check if pinch gesture was detected (if thumb and index are close together)
                if l < 30 and not clickDetected:
                    clickDetected = True
                    buttonProcessed = True

                    # Visual click feedback (button highlight on click)
                    cv2.rectangle(img, (x, y), (x + w, y + h), button.clickColor, cv2.FILLED)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
                    cv2.putText(img, button.text, (x + 25, y + 60),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)

                    # Process the button press event based on the text on the button
                    if button.text == "=":
                        try:
                            if "!" in finalText:  # Check for factorial calculation
                                num = int(finalText[:-1])  
                                finalText = str(factorial(num))
                            else:
                                finalText = str(eval(finalText))  # Evaluate the expression
                        except:
                            finalText = "Error"
                    elif button.text == "C":
                        finalText = ""  # Clear the display
                    elif button.text == "←":
                        finalText = finalText[:-1]  # Remove the last character (backspace)
                    elif button.text == "pow":
                        finalText += "**"  # Use Python's exponentiation operator for "pow"
                    elif button.text == "!":
                        finalText += "!"  # Add the factorial symbol to the text
                    else:
                        finalText += button.text  # Add the button's text to the final expression

                    break

        if l > 30:  # Reset the click detection when thumb and index are far apart
            clickDetected = False

    cv2.imshow("Virtual Calculator", img)  # Display the image
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit when 'q' is pressed
        break

cap.release()  # Release the camera resource
cv2.destroyAllWindows()  # Close the window

