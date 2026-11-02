import math
import os
import sys

import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60
SPEED = 300
SCALE = 2
ANIM_FPS = 20

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHEET_PATH = os.path.join(BASE_DIR, "car_sheet.png")
FRAME_W, FRAME_H = 122, 35

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Машинка: стрелки или WASD, Esc - выход")
clock = pygame.time.Clock()


def load_car_frames():
    sheet = pygame.image.load(SHEET_PATH).convert_alpha()
    count = sheet.get_width() // FRAME_W
    frames = []
    for i in range(count):
        frame = sheet.subsurface((i * FRAME_W, 0, FRAME_W, FRAME_H))
        frame = pygame.transform.smoothscale(frame, (FRAME_W * SCALE, FRAME_H * SCALE))
        frames.append(frame)
    return frames


def make_fallback_frame(wheel_angle):
    surf = pygame.Surface((120, 60), pygame.SRCALPHA)
    pygame.draw.rect(surf, (220, 40, 40), (5, 25, 110, 22), border_radius=8)
    pygame.draw.polygon(surf, (200, 30, 30), [(28, 25), (42, 6), (80, 6), (96, 25)])
    pygame.draw.polygon(surf, (170, 220, 255), [(35, 24), (45, 10), (59, 10), (59, 24)])
    pygame.draw.polygon(surf, (170, 220, 255), [(64, 24), (64, 10), (78, 10), (88, 24)])
    for cx in (28, 92):
        cy = 46
        pygame.draw.circle(surf, (30, 30, 30), (cx, cy), 12)
        pygame.draw.circle(surf, (170, 170, 170), (cx, cy), 7)
        for k in range(4):
            a = math.radians(wheel_angle + k * 90)
            end = (cx + 7 * math.cos(a), cy + 7 * math.sin(a))
            pygame.draw.line(surf, (60, 60, 60), (cx, cy), end, 2)
    return surf


if os.path.exists(SHEET_PATH):
    frames = load_car_frames()
else:
    print("car_sheet.png не найден рядом со скриптом - рисую запасную машинку")
    frames = [make_fallback_frame(i * 90 / 8) for i in range(8)]

rect = frames[0].get_rect(center=(WIDTH // 2, HEIGHT // 2))
pos = pygame.Vector2(rect.center)
facing_right = True
frame_index = 0.0

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

    move = pygame.Vector2(dx, dy)
    if move.length_squared() > 0:
        move = move.normalize()
        pos += move * SPEED * dt
        if dx != 0:
            facing_right = dx > 0
        frame_index = (frame_index + ANIM_FPS * dt) % len(frames)

    pos.x = max(rect.width / 2, min(WIDTH - rect.width / 2, pos.x))
    pos.y = max(rect.height / 2, min(HEIGHT - rect.height / 2, pos.y))
    rect.center = (round(pos.x), round(pos.y))

    image = frames[int(frame_index) % len(frames)]
    if not facing_right:
        image = pygame.transform.flip(image, True, False)

    screen.fill((90, 150, 90))
    screen.blit(image, rect)
    pygame.display.flip()

pygame.quit()
sys.exit()