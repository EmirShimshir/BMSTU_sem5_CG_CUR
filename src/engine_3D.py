from engine_base import EngineBase

from model import *

from PyQt5.QtGui import QColor


class Engine3D(EngineBase):

    def __init__(self):
        super().__init__()
        self.models = []
        self.matProj = MatProj(self.width, self.height)
        self.draw = self.fill_triangle_guro
        self.tri = False

    def update(self):
        self.fill(QColor(255, 204, 173).rgb())

        for model in self.models:
            model.update()

            mat_world = MatIdentity()
            mat_world = mat_world.mul_mat(model.mat_rot_x)
            mat_world = mat_world.mul_mat(model.mat_rot_y)
            mat_world = mat_world.mul_mat(model.mat_rot_z)
            mat_world = mat_world.mul_mat(model.mat_trans)
            mat_view = self.camera.get_view_mat()

            for tri in model.tris:
                tri_transformed = tri.copy()
                tri_transformed.p[0] = mat_world.mul_vec(tri.p[0])
                tri_transformed.p[1] = mat_world.mul_vec(tri.p[1])
                tri_transformed.p[2] = mat_world.mul_vec(tri.p[2])

                mat_world_t_inv = mat_world.transpose().inverse()
                tri_transformed.n[0] = mat_world_t_inv.mul_vec(tri.n[0])
                tri_transformed.n[1] = mat_world_t_inv.mul_vec(tri.n[1])
                tri_transformed.n[2] = mat_world_t_inv.mul_vec(tri.n[2])

                line1 = Vec3D.sub(tri_transformed.p[1], tri_transformed.p[0])
                line2 = Vec3D.sub(tri_transformed.p[2], tri_transformed.p[0])

                normal = Vec3D.cp(line1, line2)
                normal.normalize()

                v_cam_ray = Vec3D.sub(tri_transformed.p[0], self.camera.point)
                dp_cam_ray = Vec3D.dp(normal, v_cam_ray)

                if dp_cam_ray < 0:
                    tri_viewed = tri_transformed.copy()
                    tri_viewed.p[0] = mat_view.mul_vec(tri_transformed.p[0])
                    tri_viewed.p[1] = mat_view.mul_vec(tri_transformed.p[1])
                    tri_viewed.p[2] = mat_view.mul_vec(tri_transformed.p[2])

                    tri_projected = tri_viewed.copy()
                    tri_projected.p[0] = self.matProj.mul_vec(tri_viewed.p[0])
                    tri_projected.p[1] = self.matProj.mul_vec(tri_viewed.p[1])
                    tri_projected.p[2] = self.matProj.mul_vec(tri_viewed.p[2])
                    tri_projected.p[0].div(tri_projected.p[0].w)
                    tri_projected.p[1].div(tri_projected.p[1].w)
                    tri_projected.p[2].div(tri_projected.p[2].w)

                    # перенос на экран
                    offset_view = Vec3D(1, 1, 1)
                    tri_projected.p[0] = Vec3D.add(tri_projected.p[0], offset_view)
                    tri_projected.p[1] = Vec3D.add(tri_projected.p[1], offset_view)
                    tri_projected.p[2] = Vec3D.add(tri_projected.p[2], offset_view)

                    tri_projected.p[0].x *= 0.5 * self.width
                    tri_projected.p[0].y *= 0.5 * self.height
                    tri_projected.p[0].z *= 0.5 * self.depth
                    tri_projected.p[1].x *= 0.5 * self.width
                    tri_projected.p[1].y *= 0.5 * self.height
                    tri_projected.p[1].z *= 0.5 * self.depth
                    tri_projected.p[2].x *= 0.5 * self.width
                    tri_projected.p[2].y *= 0.5 * self.height
                    tri_projected.p[2].z *= 0.5 * self.depth

                    self.draw(tri_projected.p[0], tri_projected.p[1], tri_projected.p[2],
                              tri_projected.n[0], tri_projected.n[1], tri_projected.n[2], *model.color)

                    if self.tri:
                        self.draw_triangle(tri_projected.p[0], tri_projected.p[1], tri_projected.p[2],
                                           0, 120, 0)

    def clear_models(self):
        self.models = []

    def add_models(self, v, g, ro):
        self.models.append(Sink())
        self.models.append(Wave(ro))
        self.models.append(Blob(v, g))

    def drawer(self, guro, tri):
        self.tri = True if tri else False
        self.draw = self.fill_triangle_guro if guro else self.fill_triangle_fong
