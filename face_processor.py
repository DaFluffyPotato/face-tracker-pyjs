import sys
import json
import math
import os
import random

import pygame
from pygame.locals import *

import text
import poly_3d

X_ROT_SCALE = 3
AVERAGE_DISTANCE = 100
RESTING_MOUTH_WIDTH = 0.67

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((800, 800),0,32)

def get_data():
    f = open('face-api.js/examples/examples-browser/out.json', 'r')
    dat = json.loads(f.read())
    f.close()
    return dat

def blit_center(target_surf, surf, pos):
    target_surf.blit(surf, (- surf.get_width() // 2 + pos[0], - surf.get_height() // 2 + pos[1]))

def normalize(val, amt):
    if val > amt:
        val -= amt
    elif val < amt:
        val += amt
    else:
        val = 0
    return val

main_font = text.Font('fonts/large_font.png', (255, 255, 255))

rot_histories = [[0], [0], [0]]
pos_histories = [[0], [0], [0]]

points = []
position = [0, 0, 0]
# pos, vel, size
particles = []

px = 0
py = 0
pz = 0

current_emotion = ['neutral', 0]
while True:
    screen.fill((0, 255, 0))

    current_emotion[1] += 1

    prev_avg_pos = [px, py, pz]
    px = sum(pos_histories[0]) / len(pos_histories[0])
    py = sum(pos_histories[1]) / len(pos_histories[1])
    pz = sum(pos_histories[2]) / len(pos_histories[2])

    try:
        all_data = get_data()
        face_dat = all_data['landmarks']['_positions']
        points = []
        for p in face_dat:
            points.append((int(p['_x']), int(p['_y'])))
    except:
        pass

    chin = points[:17]
    left_eyebrow = points[17:22]
    right_eyebrow = points[22:27]
    nose = points[27:36]
    left_eye = points[36:42]
    right_eye = points[42:48]
    mouth = points[48:]
    if 1:
        pygame.draw.lines(screen, (255, 255, 255), False, chin)
        pygame.draw.lines(screen, (255, 0, 0), False, left_eyebrow)
        pygame.draw.lines(screen, (255, 0, 0), False, right_eyebrow)
        pygame.draw.lines(screen, (255, 255, 0), False, nose)
        pygame.draw.lines(screen, (255, 255, 255), False, [left_eye[1], right_eye[2]])
        pygame.draw.lines(screen, (255, 255, 255), False, [nose[3], nose[6]])
        pygame.draw.lines(screen, (255, 0, 255), True, left_eye)
        pygame.draw.lines(screen, (255, 0, 255), True, right_eye)
        pygame.draw.lines(screen, (0, 255, 255), True, mouth)
    

    eye_dis = math.sqrt((right_eye[2][1] - left_eye[1][1]) ** 2 + (right_eye[2][0] - left_eye[1][0]) ** 2)
    rot_z = math.atan2((right_eye[2][1] - left_eye[1][1]), (right_eye[2][0] - left_eye[1][0]))
    main_font.render('rotz: ' + str(round(math.degrees(rot_z), 2)), screen, (4, 250))

    left_eyebrow_length = math.sqrt((left_eyebrow[-1][0] - left_eyebrow[0][0]) ** 2 + (left_eyebrow[-1][1] - left_eyebrow[0][1]) ** 2) / eye_dis
    right_eyebrow_length = math.sqrt((right_eyebrow[-1][0] - right_eyebrow[0][0]) ** 2 + (right_eyebrow[-1][1] - right_eyebrow[0][1]) ** 2) / eye_dis
    eyebrow_implications = left_eyebrow_length - right_eyebrow_length
    rot_y = math.radians(eyebrow_implications * 90) * 0.85
    main_font.render('roty: ' + str(round(math.degrees(rot_y), 2)), screen, (4, 290))

    nose_length = nose[6][1] - nose[3][1] #math.sqrt((nose[6][0] - nose[3][0]) ** 2 + (nose[6][1] - nose[3][1]) ** 2)
    prev_pos = position.copy()
    position = [nose[6][0] / all_data['detection']['_imageDims']['_width'] - 0.5, nose[6][1] / all_data['detection']['_imageDims']['_height'] - 0.5, eye_dis / AVERAGE_DISTANCE]
    pos_change = [px - prev_avg_pos[0], py - prev_avg_pos[1], pz - prev_avg_pos[2]]
    for i in range(3):
        if i < 2:
            poly_3d.left_ear[2][i] += pos_change[i] * -4
            poly_3d.right_ear[2][i] += pos_change[i] * -4
        else:
            poly_3d.left_ear[2][i] += pos_change[i] * 4
            poly_3d.right_ear[2][i] += pos_change[i] * 4
        poly_3d.left_ear[2][i] += (poly_3d.left_ear_orig[2][i] - poly_3d.left_ear[2][i]) / 20
        poly_3d.right_ear[2][i] += (poly_3d.right_ear_orig[2][i] - poly_3d.right_ear[2][i]) / 20
    #cheek_top = chin[0]
    #cheek_top[0] += math.cos(rot_z)
    #cheek_top[1] += math.sin(rot_x)
    rot_x = math.radians(math.degrees((-math.atan2(nose_length / eye_dis, 0.05) + math.radians(66))) * X_ROT_SCALE) + abs(rot_y) * py
    main_font.render('rotx: ' + str(round(math.degrees(rot_x), 2)), screen, (4, 270))
    #pygame.draw.line(screen, (255, 255, 255), (100, 100), (100 + 40 * math.cos(rot_x), 100 + 40 * math.sin(rot_x)))

    main_font.render('scale: ' + str(round(eye_dis, 2)), screen, (4, 310))

    mouth_height = math.sqrt((mouth[14][0] - mouth[18][0]) ** 2 + (mouth[14][1] - mouth[18][1]) ** 2) / eye_dis
    mouth_width = math.sqrt((mouth[0][0] - mouth[6][0]) ** 2 + (mouth[0][1] - mouth[6][1]) ** 2) / eye_dis - RESTING_MOUTH_WIDTH
    main_font.render('mouth height: ' + str(round(mouth_height, 2)), screen, (4, 330))
    main_font.render('mouth width: ' + str(round(mouth_width, 2)), screen, (4, 350))
    #pygame.draw.circle(screen, (255, 0, 0), mouth[0], 3)
    #pygame.draw.circle(screen, (255, 0, 0), mouth[6], 3)

    expressions = [[all_data['expressions'][exp], exp] for exp in all_data['expressions']]
    expressions.sort(reverse=True)
    for i, exp in enumerate(expressions):
        if exp[0] > 0.2:
            main_font.render(exp[1] + ': ' + str(round(exp[0], 2)), screen, (4, 4 + i * 20))
    if current_emotion[1] > 40:
        if expressions[0][1] == 'happy':
            if current_emotion[0] != 'happy':
                current_emotion = ['happy', 0]
        elif (expressions[0][1] == 'disgusted') and (expressions[0][0] > 0.7):
            if current_emotion[0] != 'disgust':
                current_emotion = ['disgust', 0]
        else:
            if current_emotion[0] != 'neutral':
                current_emotion = ['neutral', 0]
    if current_emotion[0] == 'happy':
        poly_3d.face_polygons['left_eye']['poly'] = poly_3d.left_eye_happy
        poly_3d.face_polygons['right_eye']['poly'] = poly_3d.right_eye_happy
    elif current_emotion[0] == 'disgust':
        poly_3d.face_polygons['left_eye']['poly'] = poly_3d.left_eye_disgust
        poly_3d.face_polygons['right_eye']['poly'] = poly_3d.right_eye_disgust
    else:
        poly_3d.face_polygons['left_eye']['poly'] = poly_3d.left_eye
        poly_3d.face_polygons['right_eye']['poly'] = poly_3d.right_eye

    #blit_center(screen, pygame.transform.rotate(cube_3d.draw_cube(math.degrees(-rot_x), math.degrees(rot_y), 100, (50, 50, 50), 2), math.degrees(-rot_z)), (250, 450))
    for i, rot in enumerate([-rot_x, -rot_y, rot_z]):
        rot_histories[i].append(rot)
        rot_histories[i] = rot_histories[i][-20:]
    for i, p in enumerate(position):
        pos_histories[i].append(position[i])
        pos_histories[i] = pos_histories[i][-10:]

    for i, particle in sorted(enumerate(particles), reverse=True):
        particle[1][1] += 0.1
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        pygame.draw.circle(screen, (227, 49, 75), particle[0], particle[2])
        if particle[2] > 1:
            pygame.draw.circle(screen, (21, 10, 41), particle[0], particle[2] - 1)
        particle[2] -= 0.05
        if particle[2] <= 0:
            particles.pop(i)

    poly_3d.poly_data['rot'][0] = max(sum(rot_histories[0]) / len(rot_histories[0]), -math.radians(40))
    poly_3d.poly_data['rot'][1] = sum(rot_histories[1]) / len(rot_histories[1])
    poly_3d.poly_data['rot'][2] = sum(rot_histories[2]) / len(rot_histories[2]) * 1.3
    poly_3d.poly_data['pos'] = [0, 0, 5.5 - pz * 2]
    poly_3d.mouth[3][1] = poly_3d.mouth[0][1] - mouth_height * 0.275 + 0.025
    poly_3d.mouth[1][1] = poly_3d.mouth[0][1] + mouth_height * 0.7 + 0.033
    poly_3d.mouth[0][0] = poly_3d.mouth[3][0] - 0.175 - mouth_width * 0.5
    poly_3d.mouth[2][0] = poly_3d.mouth[3][0] + 0.175 + mouth_width * 0.5
    face_surf = pygame.Surface((300, 300))
    face_surf.fill((100, 0, 0))
    face_surf.set_colorkey((100, 0, 0))
    for polygon in poly_3d.face_polygons:
        render_poly = poly_3d.gen_polygon(poly_3d.face_polygons[polygon]['poly'], poly_3d.poly_data, (300, 300))
        pygame.draw.polygon(face_surf, poly_3d.face_polygons[polygon]['color'], render_poly)
        if polygon == 'chin':
            lr = [int(render_poly[3][0]), int(render_poly[2][0])]
            if abs(lr[0] - lr[1]) > face_surf.get_height() // 5:
                if random.randint(1, 2) == 1:
                    particles.append([[random.randint(min(lr) + face_surf.get_height() // 20, max(lr) - face_surf.get_height() // 20) + px * 300 + 100, (render_poly[3][1] + render_poly[2][1]) / 2 + py * 300 + 400], [0, 0], random.randint(int(4 * pz ** 1.7), int(8 * pz ** 1.7))])
    screen.blit(face_surf, (100 + px * 300, 400 + py * 300))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
    pygame.display.update()
    clock.tick(60)
    
