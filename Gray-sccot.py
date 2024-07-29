#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygame
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Pygameの初期化
pygame.init()

# シミュレーションの各パラメータ
SPACE_GRID_SIZE = 256
dx = 0.01
dt = 1
VISUALIZATION_STEP = 8

# モデルの各パラメータ
Du = 2e-5
Dv = 1e-5
f, k = 0.04, 0.06  # amorphous

# 初期化
u = np.ones((SPACE_GRID_SIZE, SPACE_GRID_SIZE))
v = np.zeros((SPACE_GRID_SIZE, SPACE_GRID_SIZE))

# 初期条件
SQUARE_SIZE = 20
u[SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2,
  SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2] = 0.5
v[SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2,
  SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2] = 0.25

# 対称性を壊すために少しノイズを入れる
u += np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE) * 0.4
v += np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE) * 0.1

# ディスプレイの設定
screen = pygame.display.set_mode((SPACE_GRID_SIZE, SPACE_GRID_SIZE))
pygame.display.set_caption('Gray-Scott Reaction-Diffusion Simulation')

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for _ in range(VISUALIZATION_STEP):
        # ラプラシアンの計算
        laplacian_u = (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) +
                       np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4 * u) / (dx * dx)
        laplacian_v = (np.roll(v, 1, axis=0) + np.roll(v, -1, axis=0) +
                       np.roll(v, 1, axis=1) + np.roll(v, -1, axis=1) - 4 * v) / (dx * dx)

        # Gray-Scottモデル方程式
        dudt = Du * laplacian_u - u * v * v + f * (1.0 - u)
        dvdt = Dv * laplacian_v + u * v * v - (f + k) * v
        u += dt * dudt
        v += dt * dvdt

    # ディスプレイの更新
    display_surface = (u - u.min()) / (u.max() - u.min())
    display_surface = np.uint8(display_surface * 255)
    colormap = cm.viridis(display_surface)
    colormap_surface = np.uint8(colormap * 255)
    surface = pygame.surfarray.make_surface(colormap_surface[:, :, :3])
    screen.blit(surface, (0, 0))
    pygame.display.update()

pygame.quit()
