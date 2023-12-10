from mainwindow import MainWindow
from renderwidget import RenderWidget

from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QApplication

from geometry import Vec3D
from camera import Camera

import sys


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

    def update(self):
        self.array = [float('+inf')] * self.width * self.height


class EngineBase:
    def __init__(self):
        self.width = 675
        self.height = 675
        self.depth = 255

        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.renderWidget = RenderWidget(self.width, self.height, self.window)

        self.timer = QTimer()
        self.timer.timeout.connect(self.render_image)
        self.timer.start(30)

        self.time = QTime()
        self.time.start()

        self.camera = Camera()

        self.z_buffer = ZBuffer(self.width, self.height)

    def render_image(self):

        self.z_buffer.update()
        self.update()
        self.renderWidget.update()

    def start(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def set_pixel(self, x, y, r, g, b):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.renderWidget.set_pixel(x, self.width - 1 - y, r, g, b)

    def fill(self, rgb):
        self.renderWidget.fill(rgb)

    def draw_line(self, rp0, rp1, r, g, b):
        p0 = rp0.copy()
        p1 = rp1.copy()

        transposed = False
        if abs(p0.x - p1.x) < abs(p0.y - p1.y):
            p0.x, p0.y = p0.y, p0.x
            p1.x, p1.y = p1.y, p1.x
            transposed = True

        if p0.x > p1.x:
            p0, p1 = p1, p0

        dx = p1.x - p0.x
        dy = p1.y - p0.y
        derror2 = abs(dy) * 2
        error2 = 0
        y = p0.y

        for x in range(int(p0.x), int(p1.x) + 1):
            if transposed:
                self.set_pixel(y, x, r, g, b)
            else:
                self.set_pixel(x, y, r, g, b)
            error2 += derror2
            if error2 > dx:
                y += 1 if p1.y > p0.y else -1
                error2 -= dx * 2

    def draw_triangle(self, p0, p1, p2, r, g, b):
        self.draw_line(p0, p1, r, g, b)
        self.draw_line(p1, p2, r, g, b)
        self.draw_line(p2, p0, r, g, b)

    def fill_triangle_guro(self, rp0, rp1, rp2, rn0, rn1, rn2, red, green, blue):
        p0 = rp0.copy()
        p1 = rp1.copy()
        p2 = rp2.copy()

        n0 = rn0.copy().normalize()
        n1 = rn1.copy().normalize()
        n2 = rn2.copy().normalize()

        p0.int()
        p1.int()
        p2.int()

        light_dir = Vec3D(1, 2, -0.5)
        light_dir.normalize()

        kd = 1

        i0 = min(max(0.05, Vec3D.dp(n0, light_dir)) * kd, 1)
        i1 = min(max(0.05, Vec3D.dp(n1, light_dir)) * kd, 1)
        i2 = min(max(0.05, Vec3D.dp(n2, light_dir)) * kd, 1)

        if p0.y == p1.y and p0.y == p2.y:
            return
        if p0.y > p1.y:
            p0, p1 = p1, p0
            i0, i1 = i1, i0
        if p0.y > p2.y:
            p0, p2 = p2, p0
            i0, i2 = i2, i0
        if p1.y > p2.y:
            p1, p2 = p2, p1
            i1, i2 = i2, i1

        total_height = p2.y - p0.y

        for i in range(total_height):
            second_half = i > p1.y - p0.y or p1.y == p0.y
            segment_height = p2.y - p1.y if second_half else p1.y - p0.y
            alpha = i / total_height
            beta = (i - (p1.y - p0.y)) / segment_height if second_half else i / segment_height

            a = Vec3D.add(p0, Vec3D.sub(p2, p0).mul(alpha))
            a.int()

            ia = i0 + (i2 - i0) * alpha

            b = Vec3D.add(p1, Vec3D.sub(p2, p1).mul(beta)) if second_half else \
                Vec3D.add(p0, Vec3D.sub(p1, p0).mul(beta))
            b.int()

            ib = i1 + (i2 - i1) * beta if second_half else \
                i0 + (i1 - i0) * beta

            if a.x > b.x:
                a, b = b, a
                ia, ib = ib, ia

            for j in range(int(a.x), int(b.x) + 1):
                phi = 1 if b.x == a.x else (j - a.x) / (b.x - a.x)

                p = Vec3D.add(a, Vec3D.sub(b, a).mul(phi))
                p.int()

                ip = ia + (ib - ia) * phi

                if self.z_buffer.get(p.x, p0.y + i) > p.z:
                    self.z_buffer.set(p.x, p0.y + i, p.z)
                    self.set_pixel(p.x, p0.y + i, ip * red, ip * green, ip * blue)

    def fill_triangle_fong(self, rp0, rp1, rp2, rn0, rn1, rn2, red, green, blue):
        p0 = rp0.copy()
        p1 = rp1.copy()
        p2 = rp2.copy()

        n0 = rn0.copy().normalize()
        n1 = rn1.copy().normalize()
        n2 = rn2.copy().normalize()

        p0.int()
        p1.int()
        p2.int()

        if p0.y == p1.y and p0.y == p2.y:
            return
        if p0.y > p1.y:
            p0, p1 = p1, p0
            n0, n1 = n1, n0
        if p0.y > p2.y:
            p0, p2 = p2, p0
            n0, n2 = n2, n0
        if p1.y > p2.y:
            p1, p2 = p2, p1
            n1, n2 = n2, n1

        total_height = p2.y - p0.y

        for i in range(total_height):
            second_half = i > p1.y - p0.y or p1.y == p0.y
            segment_height = p2.y - p1.y if second_half else p1.y - p0.y
            alpha = i / total_height
            beta = (i - (p1.y - p0.y)) / segment_height if second_half else i / segment_height

            a = Vec3D.add(p0, Vec3D.sub(p2, p0).mul(alpha))
            a.int()

            u = Vec3D.dist(p0, a) / Vec3D.dist(p2, p0)
            n_a = Vec3D.add(Vec3D.mul_value(n0, 1 - u), Vec3D.mul_value(n2, u)).normalize()

            b = Vec3D.add(p1, Vec3D.sub(p2, p1).mul(beta)) if second_half else \
                Vec3D.add(p0, Vec3D.sub(p1, p0).mul(beta))
            b.int()

            w = Vec3D.dist(p1, b) / Vec3D.dist(p2, p1) if second_half else \
                Vec3D.dist(p0, b) / Vec3D.dist(p1, p0)

            n_b = Vec3D.add(Vec3D.mul_value(n1, 1 - w), Vec3D.mul_value(n2, w)).normalize() if second_half else \
                Vec3D.add(Vec3D.mul_value(n0, 1 - w), Vec3D.mul_value(n1, w)).normalize()

            if a.x > b.x:
                a, b = b, a
                n_a, n_b = n_b, n_a

            for j in range(a.x, b.x + 1):
                phi = 1 if b.x == a.x else (j - a.x) / (b.x - a.x)

                p = Vec3D.add(a, Vec3D.sub(b, a).mul(phi))
                p.int()

                n = n_a.copy()
                if not Vec3D.equal(a, b):
                    t = Vec3D.dist(a, p) / Vec3D.dist(b, a)
                    n = Vec3D.add(Vec3D.mul_value(n_a, 1 - t), Vec3D.mul_value(n_b, t)).normalize()

                light_pos = Vec3D(1000, 2000, -500)
                light_dir = Vec3D.sub(light_pos, p)
                light_dir.normalize()

                eye_dir = Vec3D.sub(self.camera.point, p)
                eye_dir.normalize()

                reflect_dir = Vec3D.sub(Vec3D.mul_value(n, 2 * Vec3D.dp(n, light_dir)), light_dir).mul(-1)
                reflect_dir.normalize()

                kd = 0.75
                ks = 0.25
                spect_alpha = 8

                ambient = 0.25
                diffuse = Vec3D.dp(n, light_dir)
                spect = Vec3D.dp(reflect_dir, eye_dir) ** spect_alpha
                intensity = ks * spect + kd * diffuse + kd * ambient

                if intensity > 1:
                    intensity = 1

                if self.z_buffer.get(p.x, p0.y + i) > p.z:
                    self.z_buffer.set(p.x, p0.y + i, p.z)
                    self.set_pixel(p.x, p0.y + i, intensity * red, intensity * green, intensity * blue)

    def create(self):
        pass

    def update(self):
        pass
