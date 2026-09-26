
import math

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, h, **kargs):
        for i in range(x, x + h):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(y, y + w):
            self.set_pixel(x, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        slope = (x2 - x1) / (y2 - y1)

        for y in range(y1, y2):
            x = x1 + int(slope * (y - y1))
            self.set_pixel(x, y, **kargs)

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def perimeter_points(self):
        raise NotImplementedError

    def contains(self, x, y):
        raise NotImplementedError

    def paint(self, canvas):
        raise NotImplementedError

    def overlaps(self, other):
        for x, y in self.perimeter_points():
            if other.contains(x, y):
                return True

        for x, y in other.perimeter_points():
            if self.contains(x, y):
                return True

        return False


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def __repr__(self):
        return (
            "Rectangle("
            + repr(self.__length) + ", "
            + repr(self.__width) + ", "
            + repr(self.__x) + ", "
            + repr(self.__y) + ")"
        )

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        return [
            (self.__x, self.__y),
            (self.__x + self.__length, self.__y),
            (self.__x + self.__length, self.__y + self.__width),
            (self.__x, self.__y + self.__width)
        ]

    def contains(self, x, y):
        return (
            self.__x <= x <= self.__x + self.__length
            and
            self.__y <= y <= self.__y + self.__width
        )

    def paint(self, canvas):
        canvas.h_line(
            self.__x,
            self.__y,
            self.__width + 1
        )

        canvas.h_line(
            self.__x + self.__length,
            self.__y,
            self.__width + 1
        )

        canvas.v_line(
            self.__x,
            self.__y,
            self.__length + 1
        )

        canvas.v_line(
            self.__x,
            self.__y + self.__width,
            self.__length + 1
        )


class Circle(Shape):
    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y

    def __repr__(self):
        return (
            "Circle("
            + repr(self.__radius) + ", "
            + repr(self.__x) + ", "
            + repr(self.__y) + ")"
        )

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.__radius

    def get_radius(self):
        return self.__radius

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16

            x = self.__x + self.__radius * math.cos(angle)
            y = self.__y + self.__radius * math.sin(angle)

            points.append((x, y))

        return points

    def contains(self, x, y):
        distance = (
            (x - self.__x) ** 2
            + (y - self.__y) ** 2
        )

        return distance <= self.__radius ** 2

    def paint(self, canvas):
        for x, y in self.perimeter_points():
            row = round(x)
            col = round(y)

            if (
                0 <= row < canvas.height
                and 0 <= col < canvas.width
            ):
                canvas.set_pixel(row, col)


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.__x1 = x1
        self.__y1 = y1

        self.__x2 = x2
        self.__y2 = y2

        self.__x3 = x3
        self.__y3 = y3

    def __repr__(self):
        return (
            "Triangle("
            + repr(self.__x1) + ", "
            + repr(self.__y1) + ", "
            + repr(self.__x2) + ", "
            + repr(self.__y2) + ", "
            + repr(self.__x3) + ", "
            + repr(self.__y3) + ")"
        )

    def area(self):
        return abs(
            self.__x1 * (self.__y2 - self.__y3)
            + self.__x2 * (self.__y3 - self.__y1)
            + self.__x3 * (self.__y1 - self.__y2)
        ) / 2

    def perimeter(self):
        side1 = (
            (self.__x2 - self.__x1) ** 2
            + (self.__y2 - self.__y1) ** 2
        ) ** 0.5

        side2 = (
            (self.__x3 - self.__x2) ** 2
            + (self.__y3 - self.__y2) ** 2
        ) ** 0.5

        side3 = (
            (self.__x1 - self.__x3) ** 2
            + (self.__y1 - self.__y3) ** 2
        ) ** 0.5

        return side1 + side2 + side3

    def get_x1(self):
        return self.__x1

    def get_y1(self):
        return self.__y1

    def get_x2(self):
        return self.__x2

    def get_y2(self):
        return self.__y2

    def get_x3(self):
        return self.__x3

    def get_y3(self):
        return self.__y3

    def perimeter_points(self):
        return [
            (self.__x1, self.__y1),
            (self.__x2, self.__y2),
            (self.__x3, self.__y3)
        ]

    def contains(self, x, y):
        def sign(px, py, ax, ay, bx, by):
            return (
                (px - bx) * (ay - by)
                - (ax - bx) * (py - by)
            )

        d1 = sign(
            x, y,
            self.__x1, self.__y1,
            self.__x2, self.__y2
        )

        d2 = sign(
            x, y,
            self.__x2, self.__y2,
            self.__x3, self.__y3
        )

        d3 = sign(
            x, y,
            self.__x3, self.__y3,
            self.__x1, self.__y1
        )

        has_negative = d1 < 0 or d2 < 0 or d3 < 0
        has_positive = d1 > 0 or d2 > 0 or d3 > 0

        return not (has_negative and has_positive)

    def paint(self, canvas):

        def draw_line(x1, y1, x2, y2):
            steps = max(
                abs(x2 - x1),
                abs(y2 - y1)
            )

            if steps == 0:
                canvas.set_pixel(x1, y1)
                return

            for i in range(steps + 1):
                x = round(
                    x1 + (x2 - x1) * i / steps
                )

                y = round(
                    y1 + (y2 - y1) * i / steps
                )

                if (
                    0 <= x < canvas.height
                    and 0 <= y < canvas.width
                ):
                    canvas.set_pixel(x, y)

        draw_line(
            self.__x1, self.__y1,
            self.__x2, self.__y2
        )

        draw_line(
            self.__x2, self.__y2,
            self.__x3, self.__y3
        )

        draw_line(
            self.__x3, self.__y3,
            self.__x1, self.__y1
        )


class CompoundShape(Shape):
    def __init__(self, shapes=None):
        if shapes is None:
            self.shapes = []
        else:
            self.shapes = shapes

    def add(self, shape):
        self.shapes.append(shape)

    def area(self):
        total = 0

        for shape in self.shapes:
            total += shape.area()

        return total

    def perimeter(self):
        total = 0

        for shape in self.shapes:
            total += shape.perimeter()

        return total

    def perimeter_points(self):
        points = []

        for shape in self.shapes:
            points.extend(shape.perimeter_points())

        return points[:16]

    def contains(self, x, y):
        for shape in self.shapes:
            if shape.contains(x, y):
                return True

        return False

    def paint(self, canvas):
        for shape in self.shapes:
            shape.paint(canvas)

    def __repr__(self):
        return "CompoundShape(" + repr(self.shapes) + ")"

class RasterDrawing:
    def __init__(self, width, height, shapes=None):
        self.canvas = Canvas(width, height)

        if shapes is None:
            self.shapes = []
        else:
            self.shapes = shapes

    def add(self, shape):
        self.shapes.append(shape)

    def remove(self, shape):
        self.shapes.remove(shape)

    def paint(self):
        self.canvas.clear_canvas()

        for shape in self.shapes:
            shape.paint(self.canvas)

        self.canvas.display()

    def __repr__(self):
        return (
            "RasterDrawing("
            + repr(self.canvas.width) + ", "
            + repr(self.canvas.height) + ", "
            + repr(self.shapes) + ")"
        )

    def save(self, filename):
        f = open(filename, "w")
        f.write(repr(self))
        f.close()

def raster_drawing_loader(filename):
    f = open(filename, "r")
    drawing = eval(f.read())
    f.close()

    return drawing

