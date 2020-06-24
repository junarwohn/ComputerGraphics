#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image


def unitize(v):
    return v / np.sqrt(v @ v)


class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma=2.2):
        inverseGamma = 1.0 / gamma;
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0, 1)*255).astype(np.uint8)


class Camera:
    def __init__(self):
        self.viewPoint = [0, 0, 0]
        self.viewDir = np.array([0, 0, -1]).astype(np.float)
        self.viewUp = np.array([0, 1, 0]).astype(np.float)
        self.projDistance = 1.0
        self.viewProjNormal = -1 * self.viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
        self.viewWidth = 1.0
        self.viewHeight = 1.0
        self.u = 0
        self.v = 0
        self.w = 0
        self.u_unit = 0
        self.v_unit = 0
        self.plain_origin = []

    def load(self, root, img_size):
        c = root.find('camera')
        self.viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float)
        self.viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
        self.viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
        self.viewProjNormal = - 1 * self.viewDir
        if c.findtext('projNormal'):
            self.viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float)
        self.viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float)
        self.viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float)
        if c.findtext('projDistance'):
            self.projDistance = np.array(c.findtext('projDistance').split()).astype(np.float)
        self.u = unitize(np.cross(self.viewDir, self.viewUp))
        self.v = unitize(np.cross(self.u, self.viewDir))
        self.w = unitize(np.cross(self.u, self.v))
        self.u_unit = self.viewWidth / img_size[0]
        self.v_unit = self.viewHeight / img_size[1]
        self.plain_origin = - 1 * (self.projDistance * self.w + self.viewWidth / 2 * self.u + self.viewHeight / 2 * self.v)


class Shader:
    def __init__(self, shader_xml):
        self.name = shader_xml.get('name')
        self.type = shader_xml.get('type')
        self.diffuseColor = np.array(shader_xml.findtext('diffuseColor').split()).astype(np.float)
        if self.type == "Phong":
            self.specularColor = np.array(shader_xml.findtext('specularColor').split()).astype(np.float)
            self.exponent = np.array(shader_xml.findtext('exponent').split()).astype(np.float)


class Surface:
    def __init__(self, surface_xml, shader):
        self.type = surface_xml.get('type')
        self.ref = surface_xml.find('shader').get('ref')
        if self.type == "Box":
            self.minPt = np.array(surface_xml.findtext('minPt').split()).astype(np.float)
            self.maxPt = np.array(surface_xml.findtext('maxPt').split()).astype(np.float)
        if self.type == "Sphere":
            self.radius = np.array(surface_xml.findtext('radius').split()).astype(np.float)
            self.center = np.array(surface_xml.findtext('center').split()).astype(np.float)
        self.shader = shader


class Light:
    def __init__(self, light):
        self.position = np.array(light.findtext('position').split()).astype(np.float)
        self.intensity = np.array(light.findtext('intensity').split()).astype(np.float)


# since assume the box plane parallel to xyz plain
def ray_box_intersection(camera_viewpoint, view_dir, surface):
    t_min = (surface.minPt - camera_viewpoint) / view_dir
    t_max = (surface.maxPt - camera_viewpoint) / view_dir
    for i in range(3):
        if t_min[i] > t_max[i]:
            tmp = t_min[i]
            t_min[i] = t_max[i]
            t_max[i] = tmp
    intersection = np.array([max(t_min), min(t_max)]).astype(np.float)
    ret = intersection[0] < intersection[1] and min(intersection) > 0

    inter_point = np.array(camera_viewpoint + view_dir * min(intersection)).astype(np.float)
    if ret:
        normal_v = [0, 0, 0]
        checkbox = (np.around(inter_point, decimals=10) == np.around(surface.minPt, decimals=10))
        for i, b in enumerate(checkbox):
            if b:
                normal_v[i] = 1
        if normal_v == [0, 0, 0]:
            checkbox = (np.around(inter_point, decimals=10) == np.around(surface.maxPt, decimals=10))
            for i, b in enumerate(checkbox):
                if b:
                    normal_v[i] = 1
        return ret, intersection[0], inter_point, np.array(normal_v).astype(np.float)
    else:
        return False, [0, 0, 0], [0, 0, 0], [0, 0, 0]


def ray_sphere_intersection(camera_viewpoint, view_dir, surface):
    vec_p = camera_viewpoint - surface.center
    vec_d = view_dir
    tm = -1 * (vec_d @ vec_p)
    td = tm**2 - (vec_p @ vec_p) + surface.radius**2
    if td < 0:
        return False, 0, [0, 0, 0], [0, 0, 0]
    else:
        td = np.sqrt(td)
        t_min = tm - td
        if t_min < 0:
            t_min = tm + td
        if t_min < 0:
            return False, 0, [0, 0, 0], [0, 0, 0]
        inter_point = camera_viewpoint + t_min * view_dir
        normal_v = inter_point - surface.center
        return True, t_min, inter_point, normal_v


def ray_intersection(camera_viewpoint, view_dir, surface):
    if surface.type == 'Box':
        ret, t_min, inter_point, nor_v = ray_box_intersection(camera_viewpoint, view_dir, surface)
    elif surface.type == 'Sphere':
        ret, t_min, inter_point, nor_v = ray_sphere_intersection(camera_viewpoint, view_dir, surface)
    return ret, t_min, inter_point, nor_v


def lambertian(surface, light, inter_point, normal_plain):
    l_vec = unitize(light.position - inter_point)
    n_vec = unitize(normal_plain)
    lam = (light.intensity * max(0, n_vec @ l_vec)) * surface.shader.diffuseColor
    return lam


def phong(camera_viewpoint, light, surface, normal_plain, inter_point):
    l_vec = unitize(light.position - inter_point)
    v_vec = unitize(camera_viewpoint - inter_point)
    h_vec = unitize(l_vec + v_vec)
    cos_a = max(0, h_vec @ unitize(normal_plain))
    ls = (light.intensity * np.power(cos_a, surface.shader.exponent)) * surface.shader.specularColor
    ld = lambertian(surface=surface, light=light, inter_point=inter_point, normal_plain=normal_plain)
    return ls + ld


def is_shadow(light, surfaces, s_index, inter_point):
    for si, s in enumerate(surfaces):
        if si == s_index:
            continue
        ret = ray_intersection(camera_viewpoint=inter_point, view_dir=unitize(light.position-inter_point), surface=s)
        if ret[0]:
            return True
    return False


def shade(camera_viewpoint, lights, l_index, surfaces, s_index, normal_plain, inter_point):
    if is_shadow(light=lights[l_index], surfaces=surfaces, s_index=s_index, inter_point=inter_point):
        sh = [0, 0, 0]
    elif surfaces[s_index].shader.type == 'Phong':
        sh = phong(camera_viewpoint=camera_viewpoint, light=lights[l_index], surface=surfaces[s_index], inter_point=inter_point, normal_plain=normal_plain)
    elif surfaces[s_index].shader.type == 'Lambertian':
        sh = lambertian(light=lights[l_index], surface=surfaces[s_index], inter_point=inter_point, normal_plain=normal_plain)
    return sh


def main():

    tree = ET.parse(sys.argv[1])
    # tree = ET.parse("scenes\one-sphere.xml")
    # tree = ET.parse("scenes\one-box.xml")
    # tree = ET.parse("scenes\\two-boxes.xml")
    # tree = ET.parse("scenes\\wire-box-axon.xml")
    # tree = ET.parse("scenes\\wire-box-per.xml")
    # tree = ET.parse("scenes\\four-spheres.xml")
    # tree = ET.parse("scenes\\onebig-spheres.xml")
    # tree = ET.parse("scenes\\one-s-on-one-box.xml")

    np.seterr(divide='ignore', invalid='ignore')

    root = tree.getroot()

    # initialize Image
    imgSize = np.array(root.findtext('image').split()).astype(np.int)
    # Create an empty image
    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:, :] = 0

    # replace the code block below!
    for i in np.arange(imgSize[1]):
        white = Color(1, 1, 1)
        red = Color(1, 0, 0)
        blue = Color(0, 0, 1)

    # Initialize camera
    cam = Camera()
    cam.load(root, imgSize)

    shaders = []

    for c in root.findall('shader'):
        shaders.append(Shader(c))

    surfaces = []

    for c in root.findall('surface'):
        ref_shader = c.find('shader').get('ref')
        for s in shaders:
            if s.name == ref_shader:
                surfaces.append(Surface(c, s))
                break
    lights = []

    for c in root.findall('light'):
        lights.append(Light(c))

    for x in range(imgSize[0]):
        for y in range(imgSize[1]):
            u = cam.u_unit * x
            v = cam.v_unit * y
            view_dir = unitize(cam.plain_origin + u * cam.u + v * cam.v)
            ray_result = []
            for s_index, s in enumerate(surfaces):
                ret, t_min, inter_point, nor_v = ray_intersection(cam.viewPoint, view_dir, s)
                if ret:
                    ray_result.append([s_index, t_min, inter_point, nor_v])
            if len(ray_result) != 0:
                ray_result = sorted(ray_result, key=lambda x:x[1])
                sh = np.array([0,0,0]).astype(float)
                for li, light in enumerate(lights):
                    si, tm, ip, nor_p = ray_result[0]
                    sh += shade(camera_viewpoint=cam.viewPoint, lights=lights, l_index=li, surfaces=surfaces, s_index=si, inter_point=ip, normal_plain=nor_p)
                res = Color(sh[0], sh[1], sh[2])
                res.gammaCorrect()
                img[imgSize[1] - y - 1][x] = res.toUINT8()

    rawimg = Image.fromarray(img, 'RGB')
    # rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    # rawimg.save("results\\" + sys.argv[1]+'.png')


if __name__=="__main__":
    main()