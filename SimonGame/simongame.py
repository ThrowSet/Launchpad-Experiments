# @author Seth Stemen
# The classic "Simon Says Game", now with 64 buttons instead of 4 :)
import sys
import random as rand
from pygame import time

# Import launchpad_py to be used in project
try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")


def main():
    # Initial setup of Launchpad
    # Current project supports Launchpad Mk2 only, sorry to any Launchpad Pro owners out there
    if launchpad.LaunchpadMk2().Check(0):
        lp = launchpad.LaunchpadMk2()
        if lp.Open(0, "mk2"):
            print("Launchpad Mk2")
            mode = "Mk2"
    else:
        sys.exit("Failed to find a compatible Launchpad")

    # Display welcome message
    lp.ButtonFlush()
    lp.LedCtrlString("Simon Game", 0, 63, 0, -1, waitms=20)

    # Initial setup for SimonGame
    previousButtons = list(())
    userButtons = list(())

    time.wait(1000)

    # Allow user to replay should they lose
    superGamePlay = True
    while superGamePlay:

        # Primary gameplay loop
        goodGame = True
        while goodGame:
            userButtons.clear()

            # Generate new X,Y coordinate for next button press within playable matrix (Excluding X=8 and Y=0)
            x = rand.randint(0, 7)
            y = rand.randint(1, 8)
            previousButtons.append([x, y])

            # Play through all previous buttons that have been pushed, along with their corresponding button color
            for i in previousButtons:
                # Extract matrix coordinates from list
                tempx = i[0]
                tempy = i[1]

                print("X: ", tempx, " Y: ", tempy)

                # Compute hashcode of button
                colorcode = hashcode(tempx, tempy)

                # Play button on launchpad
                lp.LedCtrlXYByCode(tempx, tempy, colorcode)
                time.wait(500)
                lp.Reset()

            # Prompt for user turn
            lp.LedCtrlFlashXYByCode(8,8, 3)

            # Get and store user input in userButtons
            buttonLength = len(previousButtons)
            c = 0
            while c < buttonLength:
                buttonDetected = False
                while not buttonDetected:
                    buttonPush = lp.ButtonStateXY()

                    if len(buttonPush) != 0:
                        if buttonPush[2] != 127:
                            pressedX = buttonPush[0]
                            pressedY = buttonPush[1]

                            colorcode = hashcode(pressedX, pressedY)

                            lp.LedCtrlXYByCode(pressedX, pressedY, colorcode)

                            time.wait(300)

                            userButtons.append([buttonPush[0], buttonPush[1]])
                            buttonDetected = True
                            buttonPush.clear()
                            c += 1
                            lp.Reset()

            lp.Reset()
            lp.LedCtrlXYByCode(8, 8, 3)
            time.wait(500)

            # Verify that the user input matches the expected input
            c = 0
            while c < buttonLength:
                expectedInput = previousButtons[c]
                actualInput = userButtons[c]

                # Check X and Y variables in both and verify that they match
                if expectedInput[0] == actualInput[0] and expectedInput[1] == actualInput[1]:
                    print("Valid")
                    lp.LedCtrlXYByCode(8, 8, 64)
                    time.wait(100)
                    lp.Reset()
                    time.wait(50)
                else:
                    # Incorrect input detected, user loses
                    print("Game Over!")
                    lp.LedAllOn(72)
                    goodGame = False

                    time.wait(1000)

                    break
                c += 1

        # Prompt for playing again
        lp.Reset()
        lp.LedCtrlString("Play Again?", 0, 63, 0, -1, waitms=20)

        lp.LedCtrlPulseXYByCode(8, 1, 64)
        lp.LedCtrlPulseXYByCode(8, 2, 72)

        buttonDetected = False
        while not buttonDetected:
            buttonPush = lp.ButtonStateXY()

            if len(buttonPush) != 0:
                if buttonPush[2] != 127:
                    pressedX = buttonPush[0]
                    pressedY = buttonPush[1]

                    if pressedX == 8 and pressedY == 1:
                        # Continue gameplay
                        buttonDetected = True
                        buttonPush.clear()
                        lp.Reset()
                        previousButtons.clear()
                        break
                    elif pressedX == 8 and pressedY == 2:
                        # End gameplay
                        buttonDetected = True
                        superGamePlay = False
                        buttonPush.clear()
                        lp.LedCtrlString("Goodbye!", 0, 63, 0, -1, waitms=20)
                        break

    # Close launchpad
    lp.Reset()
    lp.Close()


# Computes the hashCode for a button press given an X,Y coordinate for a button press.
def hashcode(x, y):
    if x == 8 or y == 0:
        # Invalid bucket
        return 0
    if x < 4:
        # Must be in quadrant 1 or 3
        return 64 if y < 5 else 12
    else:
        # Must be in quadrant 2 or 4
        return 120 if y < 5 else 80


if __name__ == '__main__':
    main()
