import numpy as np
from PIL import Image


class Model:
    """
    The Model class stores data related to current viewing angle and displays it as an image

    Args:
        angle (int): Viewing angle in degrees
        r (int): Radius of image in pixels

    Attributes:
        angle (int): Viewing angle in degrees
        r (int): Radius of image in pixels
        im (PIL Image): Simple AGN model image
        arrow (PIL Image): Arrow image used for representing viewing angle
        rad (float): Viewing angle in radians
        x (int): x coordinate in pixels for arrow to be pasted on image
        y (int): y coordinate in pixels for arrow to be pasted on image
    """
    def __init__(self, angle=0, r=1220):
        self.im = Image.open('assets/agn_new.png')
        self.arrow = Image.open('assets/arrow.webp').rotate(180, expand=True)
        self.arrow = self.arrow.resize((int(.7 * self.arrow.size[0]), int(.7 * self.arrow.size[1])))
        self.angle = angle
        self.arrow = self.arrow.rotate(self.angle, expand=True)
        self.r = r
        self.center_x = self.im.size[0] // 4 + 57
        self.center_y = self.im.size[1] // 2 - 100

        self.rad = np.radians(self.angle)
        # self.x = int(r * np.cos(self.rad))
        # self.y = int(r * np.sin(self.rad))
        self.x = self.center_x + int(r * np.cos(self.rad))
        self.y = self.center_y - int(r * np.sin(self.rad))

    def refresh(self):
        """
        Function that resets the im and arrow attributes to default after
        changing through pasting or rotation
        """
        self.im = Image.open('assets/agn_new.png')
        self.arrow = Image.open('assets/arrow.webp').rotate(180, expand=True)
        self.arrow = self.arrow.resize((int(.7 * self.arrow.size[0]), int(.7 * self.arrow.size[1])))

    def rotate(self, angle):
        """
        Function that changes the viewing angle and updates effected attributes
        and returns new pasting coordinates in tuple format

        Args:
            angle (int): New viewing angle in degrees

        Returns:
            pos (tuple): New x and y coordinates in pixels to paste arrow in tuple format
        """
        r = self.r
        self.angle = angle
        self.arrow = self.arrow.rotate(angle, expand=True)
        self.rad = np.radians(self.angle)
        x = self.center_x + int(r * np.cos(self.rad))
        y = self.center_y - int(r * np.sin(self.rad))
        self.x, self.y = x, y
        pos = (x, y)
        return pos

    def turn(self, angle):
        """
        Function to turn arrow

        Args:
            angle (int): Viewing angle in degrees

        Returns:
            (PIL Image): Rotated arrow
        """
        return self.arrow.rotate(angle, expand=True)

    def paste(self, angle):
        """
        Function to paste arrow onto image and return new combined image

        Args:
            angle (int): New Viewing Angle in degrees

        Returns:
            new_im (PIL Image): new image with arrow pasted

        """
        pos = self.rotate(angle)
        new_im = self.im.copy()
        x, y = pos
        new_im.paste(self.arrow, pos, self.arrow)
        return new_im




