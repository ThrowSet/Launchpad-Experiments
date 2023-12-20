import sys
import random as rand

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
    lp.LedCtrlString("Simon Game", 0, 63, 0, -1, waitms=50)

    # Initial setup for SimonGame
    previousButtons = list(())
    userButtons = list(())

    # Primary gameplay loop
    while True:
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

            # Compute hashcode of button
            colorcode = hashcode(tempx, tempy)

            # Play button on launchpad
            lp.LedCtrlXYByCode(tempx, tempy, colorcode)




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
