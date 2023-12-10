import math

from geometry import *


class Model:
    def __init__(self):
        self.tris = []

        self.color = (100, 100, 100)

        self.time = 0
        self.fps = 60

        self.mat_rot_x = MatRotX(0 / 180 * math.pi)
        self.mat_rot_y = MatRotY(0 / 180 * math.pi)
        self.mat_rot_z = MatRotZ(0 / 180 * math.pi)
        self.mat_trans = MatTrans(0, 0, 0)

    def append(self, tri):
        self.tris.append(tri)

    def update(self):
        pass

    def load(self, filename):
        with open(filename) as f:
            verts = []
            norms = []

            for line in f:
                line = line.strip()
                if line.startswith('v '):
                    _, x, y, z = line.split()
                    v = Vec3D(float(x), float(y), float(z))
                    verts.append(v)

                if line.startswith('vn '):
                    _, x, y, z = line.split()
                    n = Vec3D(float(x), float(y), float(z))
                    norms.append(n)

                if line.startswith('f '):
                    if len(line.split()) == 4:
                        _, f0, f1, f2 = line.split()
                    else:
                        _, f0, f1, f2, _ = line.split()

                    self.tris.append(Triangle(verts[int(f0.split('/')[0]) - 1], verts[int(f1.split('/')[0]) - 1],
                                              verts[int(f2.split('/')[0]) - 1],
                                              norms[int(f0.split('/')[2]) - 1], norms[int(f1.split('/')[2]) - 1],
                                              norms[int(f2.split('/')[2]) - 1]))


start_wave = False


class Wave(Model):
    def __init__(self, ro):
        global start_wave
        start_wave = False
        super().__init__()

        self.color = (15, 94, 156)

        self.mat_rot_x = MatRotX(90 / 180 * math.pi)
        self.mat_rot_y = MatRotY(0 / 180 * math.pi)
        self.mat_rot_z = MatRotZ(0 / 180 * math.pi)
        self.mat_trans = MatTrans(0, 2.9, 0.2)

        l = 0.7
        v = 3

        self.amplitude_start = 0
        self.amplitude_end = -0.00005 * ro + 0.15
        self.amplitude = self.amplitude_start
        # self.amplitude = self.amplitude_end
        self.k = 1
        self.frequency = 2 * math.pi / l
        self.fi = v * self.frequency
        self.c = Vec3D(0, 0, 0)

        start = -0.85
        stop = 0.85
        num = 21
        step = (stop - start) / (num - 1)
        x = [start + i * step for i in range(num)]

        z_def = 0

        for i in range((len(x) - 1)):
            for j in range((len(x) - 1)):
                mid = num // 2
                if i < mid and j < mid or i >= mid and j >= mid:
                    t1 = Triangle(Vec3D(x[i], x[j], z_def),
                                  Vec3D(x[i], x[j + 1], z_def),
                                  Vec3D(x[i + 1], x[j], z_def))
                    self.append(t1)

                    t2 = Triangle(Vec3D(x[i + 1], x[j], z_def),
                                  Vec3D(x[i], x[j + 1], z_def),
                                  Vec3D(x[i + 1], x[j + 1], z_def))
                    self.append(t2)
                else:
                    t1 = Triangle(Vec3D(x[i], x[j], z_def),
                                  Vec3D(x[i + 1], x[j + 1], z_def),
                                  Vec3D(x[i + 1], x[j], z_def),
                                  )
                    self.append(t1)

                    t2 = Triangle(Vec3D(x[i], x[j], z_def),
                                  Vec3D(x[i], x[j + 1], z_def),
                                  Vec3D(x[i + 1], x[j + 1], z_def),
                                  )
                    self.append(t2)

    def update(self):
        global start_wave
        self.time += 1 / self.fps

        k = 0.01

        if start_wave and self.amplitude < self.amplitude_end:
            self.amplitude += k

        for tri in self.tris:
            for p in tri.p:
                p.z = 0
                direction = Vec3D.sub(p, self.c)
                direction.normalize()
                s = Vec3D.dp(direction, p) * self.frequency - self.time * self.fi
                p.z = self.amplitude * ((math.sin(s) + 1) * 0.5) ** self.k

        self.count_normal()

    def count_normal(self):
        for tri in self.tris:
            for i in range(3):
                direction = Vec3D.sub(tri.p[i], self.c)
                direction.normalize()
                s = Vec3D.dp(direction, tri.p[i]) * self.frequency - self.time * self.fi

                df_dx = 0.5 * self.k * direction.x * self.frequency * self.amplitude * \
                        ((math.sin(s) + 1) * 0.5) ** (self.k - 1) * math.cos(s)

                df_dy = 0.5 * self.k * direction.y * self.frequency * self.amplitude * \
                        ((math.sin(s) + 1) * 0.5) ** (self.k - 1) * math.cos(s)

                tri.n[i] = Vec3D(df_dx, -df_dy, -1).normalize()


class Sink(Model):
    def __init__(self):
        super().__init__()

        self.color = (255, 255, 255)

        self.mat_rot_x = MatRotX(0 / 180 * math.pi)
        self.mat_rot_y = MatRotY(-90 / 180 * math.pi)
        self.mat_rot_z = MatRotZ(0 / 180 * math.pi)
        self.mat_trans = MatTrans(0, 2, 0)

        self.load("./data/sink_shading.obj")


class Blob(Model):
    def __init__(self, v, g):
        super().__init__()

        self.color = (15, 94, 156)

        self.v = v
        self.g = g

        self.y_start = 2.1
        self.y_end = 0.9
        self.y = self.y_start

        self.mat_rot_x = MatRotX(0 / 180 * math.pi)
        self.mat_rot_y = MatRotY(-90 / 180 * math.pi)
        self.mat_rot_z = MatRotZ(0 / 180 * math.pi)
        self.mat_trans = MatTrans(0, self.y, 0)

        self.load("./data/blob.obj")

    def update(self):
        global start_wave
        self.time += 1 / self.fps

        self.y = self.y_start - self.v * self.time - self.g * self.time ** 2 / 2

        if self.y < self.y_end:
            start_wave = True
            self.y = self.y_start
            self.time = 0

        self.mat_trans = MatTrans(0, self.y, 0)
