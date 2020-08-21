from .draw import Image, Colour, Rectangle, Circle, Line


def main():
    rect = Rectangle((30, 30), (80, 80), Colour.BLACK)
    circle = Circle((250, 250), 30, Colour.RED)
    line = Line((400, 400), (450, 400), Colour.PURPLE, 5)

    img1 = Image(640, 480, 'image1')
    img2 = Image(480, 640, 'image2')

    img1.add_shape(rect)
    img1.add_shape(circle)

    img2.add_shape(circle)
    img2.add_shape(line)

    input('Press enter to move circle')
    circle.move(50, 0)

    input('Press enter to move rectangle')
    rect.move(-20, 100)

    input('Press enter to move line')
    line.move(-100, -100)


if __name__ == '__main__':
    main()
