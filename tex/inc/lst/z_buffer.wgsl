class ZBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.array = [float('+inf')] * width * height

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.array[x + y * self.width]

        return float('+inf')

    def set(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.array[x + y * self.width] = value
