    def update(self):
        self.time += 1 / self.fps

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