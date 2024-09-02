import pygame
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageSequence

# 初始化pygame

pygame.init()

# 创建窗口大小 (与GIF一致) 并启用双缓冲
screen_width = 498
screen_height = 498
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)

# 设置黑色背景
background_color = (0, 0, 0)  # 黑色

# 加载GIF背景图像
gif_image = Image.open("cirno-touhou-project.gif")  # 替换为你的GIF文件路径
frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]
num_frames = len(frames)
current_frame = 0

# 加载静态背景图像
static_image = pygame.image.load("IMG_4003.jpg")  # 替换为你的静态背景图路径

# 加载背景音乐
pygame.mixer.music.load('music.mp3')  # 替换为你的音乐文件路径
pygame.mixer.music.play(-1)  # 无限循环播放

# 初始化切换状态
is_static = False

# 定义数学表达式
expressions_dynamic = [
    r"$\sqrt{9} + \frac{9}{9}$", r"$\frac{9 + \sqrt{9}}{9}$", r"$\frac{9}{9} + 9$",
    r"$\frac{9 + 9}{\sqrt{9}}$", r"$\sqrt{9} \times \sqrt{9} - 9$", r"$\frac{9 \times 9}{9}$",
    r"$9$", r"$\frac{9 - \sqrt{9}}{9} - \frac{9}{9}$", r"$\frac{9}{\sqrt{9}}$",
    r"$\frac{9}{9} - \sqrt{9}$", r"$\frac{\sqrt{9}}{9 - 9}$", r"$\sqrt{9} \times \frac{9}{9}$"
]

expressions_static = [
     r"$\frac{9 + 9}{\sqrt{9}}$",  # 12
    r"$\frac{9}{9}$",             # 1
    r"$\frac{9 + 9}{9}$",         # 2
    r"$\sqrt{9} + 9 - 9$",        # 3
    r"$\sqrt{9} + \frac{9}{9}$",  # 4
    r"$\sqrt{9}! - \frac{9}{9}$", # 5
    r"$9 - \frac{9}{\sqrt{9}}$",  # 6
    r"$9 - \sqrt{9} + \frac{9}{9}$", # 7 
    r"$9 - \frac{9}{9}$",         # 8
    r"$\sqrt[9]{9^9}$",           # 9
    r"$9 + \frac{9}{9}$",         # 10
    r"$\frac{99}{9}$"             # 11
]

# 绘制时钟的函数
def draw_clock(expressions, fontsize=15, color='black'):
    fig, ax = plt.subplots(figsize=(4.98, 4.98))  # 调整表盘大小，与GIF尺寸匹配

    # 隐藏边框和轴
    ax.set_frame_on(False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    
    # 绘制时钟的圆圈
    circle = plt.Circle((0.5, 0.5), 0.4, color='lightblue', fill=False, lw=5)
    ax.add_artist(circle)
    
    # 时钟数字的位置
    clock_positions = [
        (0.5, 0.9), (0.7, 0.85), (0.85, 0.7), (0.9, 0.5),
        (0.85, 0.3), (0.7, 0.15), (0.5, 0.1), (0.3, 0.15),
        (0.15, 0.3), (0.1, 0.5), (0.15, 0.7), (0.3, 0.85)
    ]
    
    for pos, expr in zip(clock_positions, expressions):
        ax.text(pos[0], pos[1], expr, ha='center', va='center', fontsize=fontsize, color=color)
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    # 保存时钟为图像
    plt.savefig("clock.png", bbox_inches='tight', transparent=True)
    plt.close()

# 绘制表针的函数
def draw_hands(screen, center_x, center_y):
    now = time.localtime()
    seconds = now.tm_sec
    minutes = now.tm_min
    hours = now.tm_hour % 12

    # 计算角度
    second_angle = math.radians((seconds / 60) * 360 - 90)
    minute_angle = math.radians((minutes / 60) * 360 - 90)
    hour_angle = math.radians((hours / 12) * 360 - 90 + (minutes / 60) * 30)

    # 表针长度
    second_length = 180
    minute_length = 140
    hour_length = 100

    # 计算指针的终点坐标
    second_hand = (center_x + second_length * math.cos(second_angle), center_y + second_length * math.sin(second_angle))
    minute_hand = (center_x + minute_length * math.cos(minute_angle), center_y + minute_length * math.sin(minute_angle))
    hour_hand = (center_x + hour_length * math.cos(hour_angle), center_y + hour_length * math.sin(hour_angle))

    # 绘制表针
    pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), second_hand, 2)  # 秒针
    pygame.draw.line(screen, (0, 255, 0), (center_x, center_y), minute_hand, 4)  # 分针
    pygame.draw.line(screen, (0, 0, 255), (center_x, center_y), hour_hand, 6)    # 时针

# 显示切换按钮
def draw_switch_button():
    font = pygame.font.Font(None, 34)
    text = font.render("Fix", True, (255, 0, 0))
    screen.blit(text, (screen_width - 50, 50))

# 主循环
running = True
draw_clock(expressions_dynamic)
clock_image = pygame.image.load("clock.png")

# 设置GIF帧率
frame_delay = 100  # 每帧100毫秒

while running:
    start_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if screen_width - 200 <= mouse_pos[0] <= screen_width and 50 <= mouse_pos[1] <= 124:
                is_static = not is_static
                if is_static:
                    draw_clock(expressions_static, fontsize=14, color='black')  # 使用更小的字体
                else:
                    draw_clock(expressions_dynamic)
                clock_image = pygame.image.load("clock.png")

    # 填充黑色背景
    screen.fill(background_color)

    if is_static:
        # 显示静态背景
        screen.blit(static_image, (0, 0))
    else:
        # 显示GIF背景
        gif_surface = pygame.image.fromstring(frames[current_frame].tobytes(), frames[current_frame].size, frames[current_frame].mode).convert()
        gif_surface.set_colorkey((0, 0, 0))  # 将黑色设置为透明色
        screen.blit(gif_surface, (0, 0))
        current_frame = (current_frame + 1) % num_frames  # 移动到下一帧

    # 显示时钟表盘并调整其位置为中心
    screen.blit(clock_image, (screen_width // 2 - clock_image.get_width() // 2, screen_height // 2 - clock_image.get_height() // 2))

    # 绘制表针
    draw_hands(screen, screen_width // 2, screen_height // 2)

    # 显示切换按钮
    draw_switch_button()

    # 更新显示
    pygame.display.flip()

    # 控制帧率，防止跳帧
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time < frame_delay:
        pygame.time.delay(frame_delay - elapsed_time)

pygame.quit()
