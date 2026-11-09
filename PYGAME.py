import math
import os
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PYGAME')
clock = pygame.time.Clock()
big_font = pygame.font.SysFont('arial', 64)

car = pygame.image.load('PYGAME/pictures/car_blue_1.png').convert_alpha()
road = pygame.image.load('PYGAME/pictures/round.png').convert()
road = pygame.transform.scale(road, (800, 600))

ROAD_LEFT = 150
ROAD_RIGHT = 650
show_borders = False

enemy_imgs = []
for name in ['car_red_1.png', 'car_yellow_1.png', 'car_green_1.png', 'car_black_1.png']:
    path = 'PYGAME/pictures/' + name
    if os.path.exists(path):
        enemy_imgs.append(pygame.transform.rotate(pygame.image.load(path).convert_alpha(), 180))

if not enemy_imgs:
    for color in [(255, 80, 80), (255, 220, 60), (80, 220, 100), (120, 120, 120)]:
        tinted = pygame.transform.rotate(car, 180).copy()
        tinted.fill(color + (255,), special_flags=pygame.BLEND_RGBA_MULT)
        enemy_imgs.append(tinted)

x = (ROAD_LEFT + ROAD_RIGHT - car.get_width()) // 2
y = 600 - car.get_height() - 60
speed = 5
FORWARD_speed = 10
back_speed = 5
road_speed = 6
road_y = 0

brake_factor = 1
traffic_factor = 1

enemies = []
spawn_timer = 0
lives = 3
MAX_LIVES = 3

crashed = False
crash_timer = 0
crash_pos = (0, 0)
particles = []


def draw_heart(surf, cx, cy, size, filled):
    pts = []
    for i in range(60):
        t = math.pi * 2 * i / 60
        px = 16 * math.sin(t) ** 3
        py = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + px * size / 34, cy - py * size / 34))
    if filled:
        pygame.draw.polygon(surf, (230, 30, 60), pts)
        pygame.draw.polygon(surf, (120, 0, 20), pts, 3)
        pygame.draw.circle(surf, (255, 170, 185), (int(cx - size * 0.22), int(cy - size * 0.2)), max(2, size // 10))
    else:
        pygame.draw.polygon(surf, (40, 40, 40), pts)
        pygame.draw.polygon(surf, (110, 110, 110), pts, 3)


def start_crash(cx, cy):
    global crashed, crash_timer, crash_pos, particles, lives
    crashed = True
    crash_timer = 0
    crash_pos = (cx, cy)
    lives -= 1
    particles = []
    for _ in range(60):
        particles.append({
            'x': cx,
            'y': cy,
            'vx': random.uniform(-7, 7),
            'vy': random.uniform(-7, 7),
            'life': random.randint(25, 60),
            'max': 60,
            'r': random.randint(4, 10),
        })


def reset(full):
    global x, y, enemies, spawn_timer, crashed, particles, lives, traffic_factor
    x = (ROAD_LEFT + ROAD_RIGHT - car.get_width()) // 2
    y = 600 - car.get_height() - 60
    enemies = []
    spawn_timer = 0
    crashed = False
    particles = []
    traffic_factor = 1.0
    if full:
        lives = MAX_LIVES


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_b:
                show_borders = not show_borders

    keys = pygame.key.get_pressed()

    if not crashed:
        braking = keys[pygame.K_DOWN] or keys[pygame.K_s]

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y -= FORWARD_speed
        if braking:
            y += back_speed

        x = max(ROAD_LEFT, min(x, ROAD_RIGHT - car.get_width()))
        y = max(0, min(y, 600 - car.get_height()))

        target = brake_factor if braking else 1.0
        traffic_factor += (target - traffic_factor) * 0.1

        road_y = (road_y + road_speed * traffic_factor) % 600

        spawn_timer += traffic_factor
        if spawn_timer >= random.randint(50, 90):
            spawn_timer = 0
            img = random.choice(enemy_imgs)
            ex = random.randint(ROAD_LEFT, ROAD_RIGHT - img.get_width())
            enemies.append({
                'img': img,
                'x': ex,
                'y': -img.get_height(),
                'speed': random.randint(7, 10),
            })

        player_rect = pygame.Rect(x, y, car.get_width(), car.get_height()).inflate(-12, -12)
        for e in enemies[:]:
            e['y'] += e['speed'] * traffic_factor
            e_rect = pygame.Rect(e['x'], e['y'], e['img'].get_width(), e['img'].get_height()).inflate(-12, -12)
            if e['y'] > 600:
                enemies.remove(e)
            elif e_rect.colliderect(player_rect):
                hit = e_rect.clip(player_rect)
                start_crash(hit.centerx, hit.centery)
                break
    else:
        crash_timer += 1
        for p in particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vx'] *= 0.95
            p['vy'] *= 0.95
            p['life'] -= 1
        particles = [p for p in particles if p['life'] > 0]
        if crash_timer > 120:
            reset(full=(lives <= 0))

    ox = oy = 0
    if crashed and crash_timer < 25:
        ox = random.randint(-8, 8)
        oy = random.randint(-8, 8)

    screen.blit(road, (ox, road_y + oy))
    screen.blit(road, (ox, road_y - 600 + oy))

    for e in enemies:
        if not (crashed and crash_timer > 8):
            screen.blit(e['img'], (e['x'] + ox, e['y'] + oy))

    if not (crashed and crash_timer > 8):
        screen.blit(car, (x + ox, y + oy))

    if crashed:
        if crash_timer < 15:
            radius = crash_timer * 7
            flash = pygame.Surface((800, 600), pygame.SRCALPHA)
            pygame.draw.circle(flash, (255, 255, 255, max(0, 255 - crash_timer * 16)), crash_pos, radius)
            screen.blit(flash, (0, 0))
        for p in particles:
            t = p['life'] / p['max']
            color = (255, int(60 + 180 * t), int(40 * t))
            pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), max(1, int(p['r'] * t)))
        if crash_timer > 25:
            msg = 'ИГРА ОКОНЧЕНА' if lives <= 0 else 'АВАРИЯ!'
            text = big_font.render(msg, True, (255, 60, 60))
            screen.blit(text, (400 - text.get_width() // 2, 260))

    if show_borders:
        pygame.draw.line(screen, (255, 0, 0), (ROAD_LEFT, 0), (ROAD_LEFT, 600), 2)
        pygame.draw.line(screen, (255, 0, 0), (ROAD_RIGHT, 0), (ROAD_RIGHT, 600), 2)

    for i in range(MAX_LIVES):
        draw_heart(screen, 35 + i * 45, 35, 30, i < lives)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
