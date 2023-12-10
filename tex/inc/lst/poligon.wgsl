
    def gen_poligon(self)
        start = -0.85
        stop = 0.85
        num = 11
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