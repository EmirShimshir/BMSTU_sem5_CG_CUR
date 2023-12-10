import math
import numpy as np


class Vec3D:
    def __init__(self, *args):
        if len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.w = 1
        else:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 1

    def copy(self):
        v_new = Vec3D()

        v_new.x = self.x
        v_new.y = self.y
        v_new.z = self.z
        v_new.w = self.w

        return v_new

    @staticmethod
    def sub(v1, v2):
        v_new = Vec3D()

        v_new.x = v1.x - v2.x
        v_new.y = v1.y - v2.y
        v_new.z = v1.z - v2.z

        return v_new

    @staticmethod
    def add(v1, v2):
        v_new = Vec3D()

        v_new.x = v1.x + v2.x
        v_new.y = v1.y + v2.y
        v_new.z = v1.z + v2.z

        return v_new

    @staticmethod
    def dp(v1, v2):
        return (v1.x * v2.x +
                v1.y * v2.y +
                v1.z * v2.z)

    @staticmethod
    def cp(v1, v2):
        v_new = Vec3D()

        v_new.x = v1.y * v2.z - v1.z * v2.y
        v_new.y = v1.z * v2.x - v1.x * v2.z
        v_new.z = v1.x * v2.y - v1.y * v2.x

        return v_new

    @staticmethod
    def mul_value(v1, f):
        v_new = Vec3D()

        v_new.x = v1.x * f
        v_new.y = v1.y * f
        v_new.z = v1.z * f

        return v_new

    @staticmethod
    def dist(v1, v2):
        return Vec3D.sub(v1, v2).length()

    @staticmethod
    def equal(v1, v2):
        if v1.x == v2.x and v1.y == v2.y and v1.z == v2.z:
            return True
        return False

    def length(self):
        return (self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5

    def mul(self, value):
        self.x *= value
        self.y *= value
        self.z *= value

        return self

    def div(self, value):
        if value != 0:
            self.x /= value
            self.y /= value
            self.z /= value

        return self

    def int(self):
        self.x = int(self.x)
        self.y = int(self.y)
        # self.z = int(self.z)

        return self

    def normalize(self):
        l = self.length()
        self.div(l)

        return self

    def string(self):
        return f"(x = {self.x}; y = {self.y}; z = {self.z})"


class Triangle:
    def __init__(self, *args):
        self.n = [Vec3D()] * 3
        self.p = [Vec3D()] * 3

        if len(args) == 3:
            self.p = [args[0], args[1], args[2]]
        elif len(args) == 6:
            self.p = [args[0], args[1], args[2]]
            self.n = [args[3], args[4], args[5]]

    def copy(self):
        new_tri = Triangle()

        new_tri.p[0] = self.p[0].copy()
        new_tri.p[1] = self.p[1].copy()
        new_tri.p[2] = self.p[2].copy()
        
        new_tri.n[0] = self.n[0].copy()
        new_tri.n[1] = self.n[1].copy()
        new_tri.n[2] = self.n[2].copy()

        return new_tri

    def string(self):
        return f"(p1 = {self.p[0].string()}; p2 = {self.p[1].string()}; p3 = {self.p[2].string()})"


class Mat4x4:
    def __init__(self):
        self.m = [[0.0] * 4 for _ in range(4)]

    def mul_vec(self, i):
        o = Vec3D()

        o.x = i.x * self.m[0][0] + i.y * self.m[1][0] + i.z * self.m[2][0] + i.w * self.m[3][0]
        o.y = i.x * self.m[0][1] + i.y * self.m[1][1] + i.z * self.m[2][1] + i.w * self.m[3][1]
        o.z = i.x * self.m[0][2] + i.y * self.m[1][2] + i.z * self.m[2][2] + i.w * self.m[3][2]
        o.w = i.x * self.m[0][3] + i.y * self.m[1][3] + i.z * self.m[2][3] + i.w * self.m[3][3]

        return o

    def mul_mat(self, i):
        o = Mat4x4()

        for r in range(4):
            for c in range(4):
                o.m[r][c] = self.m[r][0] * i.m[0][c] + \
                            self.m[r][1] * i.m[1][c] + \
                            self.m[r][2] * i.m[2][c] + \
                            self.m[r][3] * i.m[3][c]

        return o

    def transpose(self):
        o = Mat4x4()

        for r in range(4):
            for c in range(4):
                o.m[r][c] = self.m[c][r]

        return o

    def inverse(self):
        o = Mat4x4()

        np_matrix = np.array(self.m)

        det = np.linalg.det(np_matrix)

        if det == 0:
            return None

        inverse = np.linalg.inv(np_matrix)

        o.m = inverse.tolist()





        # # Находим определитель матрицы
        # det = (
        #         self.m[0][0] * (self.m[1][1] * self.m[2][2] - self.m[1][2] * self.m[2][1]) -
        #         self.m[0][1] * (self.m[1][0] * self.m[2][2] - self.m[1][2] * self.m[2][0]) +
        #         self.m[0][2] * (self.m[1][0] * self.m[2][1] - self.m[1][1] * self.m[2][0])
        # )
        #
        # # Проверяем, является ли матрица вырожденной (определитель равен 0)
        # if det == 0.0:
        #     return None
        #
        # # Находим обратную матрицу через алгебраическое дополнение
        # for r in range(4):
        #     for c in range(4):
        #         o.m[r][c] = (
        #                 (self.m[(r + 1) % 4][(c + 1) % 4] * self.m[(r + 2) % 4][(c + 2) % 4] - self.m[(r + 1) % 4][
        #                     (c + 2) % 4] * self.m[(r + 2) % 4][(c + 1) % 4]) / det
        #         )

        return o

    def print(self):
        for row in self.m:
            print(*row)


class MatProj(Mat4x4):
    def __init__(self, width, height):
        super().__init__()

        near = 0.1
        far = 1000.0
        fov = 90.0
        aspect_ratio = height / width
        fov_rad = 1 / math.tan(fov * 0.5 / 180 * math.pi)

        self.m[0][0] = aspect_ratio * fov_rad
        self.m[1][1] = fov_rad
        self.m[2][2] = far / (far - near)
        self.m[3][2] = (-far * near) / (far - near)
        self.m[2][3] = 1.0


class MatRotX(Mat4x4):
    def __init__(self, theta):
        super().__init__()

        self.m[0][0] = 1
        self.m[1][1] = math.cos(theta)
        self.m[1][2] = math.sin(theta)
        self.m[2][1] = -math.sin(theta)
        self.m[2][2] = math.cos(theta)
        self.m[3][3] = 1


class MatRotY(Mat4x4):
    def __init__(self, theta):
        super().__init__()

        self.m[0][0] = math.cos(theta)
        self.m[0][2] = math.sin(theta)
        self.m[2][0] = -math.sin(theta)
        self.m[1][1] = 1
        self.m[2][2] = math.cos(theta)
        self.m[3][3] = 1


class MatRotZ(Mat4x4):
    def __init__(self, theta):
        super().__init__()

        self.m[0][0] = math.cos(theta)
        self.m[0][1] = math.sin(theta)
        self.m[1][0] = -math.sin(theta)
        self.m[1][1] = math.cos(theta)
        self.m[2][2] = 1
        self.m[3][3] = 1


class MatTrans(Mat4x4):
    def __init__(self, x, y, z):
        super().__init__()

        self.m[0][0] = 1.0
        self.m[1][1] = 1.0
        self.m[2][2] = 1.0
        self.m[3][3] = 1.0
        self.m[3][0] = x
        self.m[3][1] = y
        self.m[3][2] = z


class MatIdentity(Mat4x4):
    def __init__(self):
        super().__init__()

        self.m[0][0] = 1.0
        self.m[1][1] = 1.0
        self.m[2][2] = 1.0
        self.m[3][3] = 1.0


class MatPointAt(Mat4x4):
    def __init__(self, pos, forward, up, right):
        super().__init__()

        self.m[0][0] = right.x
        self.m[0][1] = right.y
        self.m[0][2] = right.z
        self.m[0][3] = 0.0

        self.m[1][0] = up.x
        self.m[1][1] = up.y
        self.m[1][2] = up.z
        self.m[1][3] = 0.0

        self.m[2][0] = forward.x
        self.m[2][1] = forward.y
        self.m[2][2] = forward.z
        self.m[2][3] = 0.0

        self.m[3][0] = pos.x
        self.m[3][1] = pos.y
        self.m[3][2] = pos.z
        self.m[3][3] = 1.0

    def quick_inverse(self):
        new_m = Mat4x4()
        
        new_m.m[0][0] = self.m[0][0]
        new_m.m[0][1] = self.m[1][0]
        new_m.m[0][2] = self.m[2][0]
        new_m.m[0][3] = 0.0

        new_m.m[1][0] = self.m[0][1]
        new_m.m[1][1] = self.m[1][1]
        new_m.m[1][2] = self.m[2][1]
        new_m.m[1][3] = 0.0

        new_m.m[2][0] = self.m[0][2]
        new_m.m[2][1] = self.m[1][2]
        new_m.m[2][2] = self.m[2][2]
        new_m.m[2][3] = 0.0

        new_m.m[3][0] = -(self.m[3][0] * new_m.m[0][0] + self.m[3][1] * new_m.m[1][0] + self.m[3][2] * new_m.m[2][0])
        new_m.m[3][1] = -(self.m[3][0] * new_m.m[0][1] + self.m[3][1] * new_m.m[1][1] + self.m[3][2] * new_m.m[2][1])
        new_m.m[3][2] = -(self.m[3][0] * new_m.m[0][2] + self.m[3][1] * new_m.m[1][2] + self.m[3][2] * new_m.m[2][2])
        new_m.m[3][3] = 1.0

        return new_m
