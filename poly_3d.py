import math
from copy import deepcopy

import pygame

chin = [
    [-0.55, 2.15, -0.5],
    [0.55, 2.15, -0.5],
    [1, 0.25, -1],
    [-1, 0.25, -1],
]

left_eye = [
    [-0.33, 0.35, -1.2],
    [-0.4, 0.4, -1.2],
    [-0.47, 0.35, -1.2],
    [-0.5, 0.15, -1.2],
    [-0.47, 0.05, -1.2],
    [-0.4, 0, -1.2],
    [-0.33, 0.05, -1.2],
    [-0.3, 0.15, -1.2],
]

right_eye = [
    [0.33, 0.35, -1.2],
    [0.4, 0.4, -1.2],
    [0.47, 0.35, -1.2],
    [0.5, 0.15, -1.2],
    [0.47, 0.05, -1.2],
    [0.4, 0, -1.2],
    [0.33, 0.05, -1.2],
    [0.3, 0.15, -1.2],
]

mouth = [
    [0.1, 0.65, -1],
    [0, 0.7, -1],
    [-0.1, 0.65, -1],
    [0, 0.6, -1],
]

left_stripe = [face[-1], face[-2], face[-3], face[-4], face[-5]]
right_stripe = [face[0], face[1], face[2], face[3], face[4]]

left_ear = [face[-1], face[-2], [face[-3][0], face[-3][1] - 0.7, face[-3][2]], face[-4]]
right_ear = [face[0], face[1], [face[2][0], face[2][1] - 0.7, face[2][2]], face[3]]
left_ear_orig = deepcopy(left_ear)
right_ear_orig = deepcopy(right_ear)

face_polygons = {
    'chin': {'color': (21, 255, 41), 'poly': chin},
    'left_eye': {'color': (255, 0, 255), 'poly': left_eye_happy},
    'right_eye': {'color': (255, 0, 255), 'poly': right_eye_happy},
    'mouth': {'color': (255, 255, 255), 'poly': mouth},
}

FOV = 120

def offset_polygon(polygon, offset):
    for point in polygon:
        point[0] += offset[0]
        point[1] += offset[1]
        point[2] += offset[2]

def rotate_x(polygon, amt):
    for point in polygon:
        angle = math.atan2(point[1], point[2])
        angle += amt
        dis = math.sqrt(point[1] ** 2 + point[2] ** 2)
        point[1] = math.sin(angle) * dis
        point[2] = math.cos(angle) * dis

def rotate_y(polygon, amt):
    for point in polygon:
        angle = math.atan2(point[0], point[2])
        angle += amt
        dis = math.sqrt(point[0] ** 2 + point[2] ** 2)
        point[0] = math.sin(angle) * dis
        point[2] = math.cos(angle) * dis

def rotate_z(polygon, amt):
    for point in polygon:
        angle = math.atan2(point[1], point[0])
        angle += amt
        dis = math.sqrt(point[1] ** 2 + point[0] ** 2)
        point[1] = math.sin(angle) * dis
        point[0] = math.cos(angle) * dis

def project_polygon(polygon, display_size):
    projected_points = []
    for point in polygon:
        x_angle = math.atan2(point[0], point[2])
        y_angle = math.atan2(point[1], point[2])
        x = x_angle / math.radians(FOV) * display_size[0] + display_size[0] // 2
        y = y_angle / math.radians(FOV) * display_size[1] + display_size[1] // 2
        projected_points.append([x, y])
    return projected_points

def gen_polygon(polygon_base, polygon_data, display_size):
    generated_polygon = deepcopy(polygon_base)
    rotate_x(generated_polygon, polygon_data['rot'][0])
    rotate_y(generated_polygon, polygon_data['rot'][1])
    rotate_z(generated_polygon, polygon_data['rot'][2])
    offset_polygon(generated_polygon, polygon_data['pos'])
    return project_polygon(generated_polygon, display_size)

poly_data = {
    'pos': [0, 0, 3.5],
    'rot': [0, 0, 0],
    }
