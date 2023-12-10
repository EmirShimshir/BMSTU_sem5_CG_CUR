def fill_triangle_fong(self, rp0, rp1, rp2, rn0, rn1, rn2, red, green, blue):
    total_height = p2.y - p0.y
    for i in range(total_height):
        second_half = i > p1.y - p0.y or p1.y == p0.y
        segment_height = p2.y - p1.y if second_half else p1.y - p0.y
        alpha = i / total_height
        beta = (i - (p1.y - p0.y)) / segment_height if second_half else i / segment_height
        a = Vec3D.add(p0, Vec3D.sub(p2, p0).mul(alpha))
        u = Vec3D.dist(p0, a) / Vec3D.dist(p2, p0)
        n_a = Vec3D.add(Vec3D.mul_value(n0, 1 - u), Vec3D.mul_value(n2, u)).normalize()
        b = Vec3D.add(p1, Vec3D.sub(p2, p1).mul(beta)) if second_half else Vec3D.add(p0, Vec3D.sub(p1, p0).mul(beta))
        w = Vec3D.dist(p1, b) / Vec3D.dist(p2, p1) if second_half else Vec3D.dist(p0, b) / Vec3D.dist(p1, p0)
        n_b = Vec3D.add(Vec3D.mul_value(n1, 1 - w), Vec3D.mul_value(n2, w)).normalize() if second_half else Vec3D.add(Vec3D.mul_value(n0, 1 - w), Vec3D.mul_value(n1, w)).normalize()
        if a.x > b.x:
            a, b = b, a
            n_a, n_b = n_b, n_a
        for j in range(int(a.x), int(b.x) + 1):
            phi = 1 if b.x == a.x else (j - a.x) / (b.x - a.x)
            p = Vec3D.add(a, Vec3D.sub(b, a).mul(phi))
            p.int()
            n = n_a.copy()
            if not Vec3D.equal(a, b):
                t = Vec3D.dist(a, p) / Vec3D.dist(b, a)
                n = Vec3D.add(Vec3D.mul_value(n_a, 1 - t), Vec3D.mul_value(n_b, t)).normalize()
