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