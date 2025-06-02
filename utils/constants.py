"""
Constants for the Mystery Adventures game.
Contains colors, fonts, window dimensions, and game states.
"""

import pygame

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Fonts
pygame.font.init()  # Ensure fonts are initialized
title_font = pygame.font.SysFont('Arial', 48, bold=True)
heading_font = pygame.font.SysFont('Arial', 36, bold=True)
text_font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 28)

# Game states
MAIN_MENU = 'main_menu'
MYSTERY_INTRO = 'mystery_intro'
RIDDLE = 'riddle'
RIDDLE_RESULT = 'riddle_result'
MYSTERY_COMPLETE = 'mystery_complete'
GAME_COMPLETE = 'game_complete'
