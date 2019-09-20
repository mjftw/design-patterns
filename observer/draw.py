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

    def move(self, x, y):
        raise NotImplementedError

    def _init_images(self):
        if not hasattr(self, 'images'):
            self.images = []

    def link_image(self, image):
        self._init_images()

        if image not in self.images:
            self.images.append(image)

    def unlink_image(self, image):
        self._init_images()

        if image in self.images:
            self.images.remove(image)

    def update_images(self):
        self._init_images()

        for image in self.images:
            image.update()


class Rectangle(Shape):
    def __init__(self, pt1, pt2, colour=None, line_px=None):
        self.pt1 = pt1
        self.pt2 = pt2
        self.colour = colour or Colour.BLACK
        self.line_px = line_px or -1

    def draw(self, image):
        cv2.rectangle(image, self.pt1, self.pt2, self.colour, self.line_px)

    def move(self, x, y):
        self.pt1 = (self.pt1[0] + x, self.pt1[1] + y)
        self.pt2 = (self.pt2[0] + x, self.pt2[1] + y)

        self.update_images()


class Line(Shape):
    def __init__(self, pt1, pt2, colour=None, line_px=None):
        self.pt1 = pt1
        self.pt2 = pt2
        self.colour = colour or Colour.BLACK
        self.line_px = line_px or 1

    def draw(self, image):
        cv2.line(image, self.pt1, self.pt2, self.colour, self.line_px)

    def move(self, x, y):
        self.pt1 = (self.pt1[0] + x, self.pt1[1] + y)
        self.pt2 = (self.pt2[0] + x, self.pt2[1] + y)

        self.update_images()

class Circle(Shape):
    def __init__(self, centre, radius, colour=None, line_px=None):
        self.centre = centre
        self.radius = radius
        self.colour = colour or Colour.BLACK
        self.line_px = line_px or -1

    def draw(self, image):
        cv2.circle(image, self.centre, self.radius, self.colour, self.line_px)

    def move(self, x, y):
        self.centre = (self.centre[0] + x, self.centre[1] + y)

        self.update_images()

class Text(Shape):
    def __init__(self, text, position,
            colour=None, size=None, thickness=None, font=None):
        self.text = text
        self.position = position
        self.colour = colour or Colour.BLACK
        self.size = size or 1
        self.thickness = thickness or 1
        self.font = font or cv2.FONT_HERSHEY_SIMPLEX

    def draw(self, image):
        cv2.putText(image, self.text, self.position, self.font,
            self.size, self.colour, self.thickness, cv2.LINE_AA)

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

        self.update_images()

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

    def update(self):
        if self._drawn:
            self.draw()

    def close(self):
        cv2.destroyWindow(self.name)
        self._drawn = False

    def add_shape(self, shape):
        assert isinstance(shape, Shape)

        self._shapes.append(shape)
        shape.link_image(self)

        self.update()

    def remove_shape(self, shape):
        if shape in self._shapes:
            self._shapes.remove(shape)
            shape.unlink_image(self)

        self.update()

    def clear_shapes(self):
        for shape in self.shapes:
            shape.unlink_image(self)

        self._shapes = []
        self.update()
