def fill_triangle_guro(self, rp0, rp1, rp2, rn0, rn1, rn2, red, green, blue):        
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