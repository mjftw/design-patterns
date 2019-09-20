import cv2
import numpy as np


class Colour():
    '''BGR Colour'''
    BLACK = (0, 0, 0)
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    PURPLE = (255, 0, 255)
    YELLOW = (0, 255, 255)
    CYAN = (255, 255, 0)
    WHITE = (255, 255, 255)


class Shape:
    def draw(self, image):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, pt1, pt2, colour=None, line_px=None):
        self.pt1 = pt1

    def draw(self, image):
        cv2.rectangle(image, self.pt1, self.pt2, self.colour, self.line_px)


class Line(Shape):
    def __init__(self, pt1, pt2, colour=None, line_px=None):
        self.pt1 = pt1
        self.pt2 = pt2
        self.colour = colour or Colour.BLACK
        self.line_px = line_px or 1

    def draw(self, image):
        cv2.line(image, self.pt1, self.pt2, self.colour, self.line_px)
        self.pt2 = pt2
        self.colour = colour or Colour.BLACK
        self.line_px = line_px or -1


class Circle(Shape):
    def __init__(self, centre, radius, colour=None, line_px=None):
        self.centre = centre
        self.radius = radius
        self.colour = colour or Colour.BLACK
        self.line_px = line_px or -1

    def draw(self, image):
        cv2.circle(image, self.centre, self.radius, self.colour, self.line_px)


class Image:
    def __init__(self, width, height, name=None):
        self.width = width
        self.height = height
        self.name = name

        self._shapes = []
        self._drawn = False

        self.draw()

    def draw(self):
        image = 255 * np.ones((self.width, self.height, 3), np.uint8)

        for shape in self._shapes:
            shape.draw(image)

        cv2.imshow(self.name, image)
        cv2.waitKey(50)

        self._drawn = True

    def _update(self):
        if self._drawn:
            self.draw()

    def close(self):
        cv2.destroyWindow(self.name)
        self._drawn = False

    def add_shape(self, shape):
        assert isinstance(shape, Shape)

        self._shapes.append(shape)
        self._update()

    def remove_shape(self, shape):
        if shape in self._shapes:
            self._shapes.remove(shape)
        self._update()

    def clear_shapes(self):
        self._shapes = []
        self._update()
