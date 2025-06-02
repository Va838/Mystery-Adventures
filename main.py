"""
Mystery Adventures
A puzzle-solving adventure game featuring multiple mysteries and riddles.

Developed by: Vainavi
Version: 1.0
Date: June 2, 2025
License: MIT
"""

import pygame
import sys
import time
from pygame.locals import *

from utils.constants import *
from utils.game_data import mysteries
from utils.ui import Button
from utils.helpers import draw_text, draw_wrapped_text, reset_game, format_time

# Initialize pygame
pygame.init()

# Set up the window
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mystery Adventures')

# Game state variables
current_state = MAIN_MENU
current_mystery = 0
current_riddle = 0
user_answer = ""
message = ""
show_hint = False
input_active = False
start_time = 0
elapsed_time = 0
total_time = 0

# Create buttons
start_button = Button(300, 300, 200, 60, "Start Game", GREEN, (100, 255, 100), BLACK)
hint_button = Button(600, 400, 150, 50, "Show Hint", BLUE, (100, 100, 255), WHITE)
submit_button = Button(400, 450, 200, 50, "Submit Answer", GREEN, (100, 255, 100), BLACK)
continue_button = Button(300, 400, 200, 60, "Continue", BLUE, (100, 100, 255), WHITE)
next_mystery_button = Button(300, 400, 200, 60, "Next Mystery", PURPLE, (200, 100, 255), WHITE)
play_again_button = Button(300, 400, 200, 60, "Play Again", GREEN, (100, 255, 100), BLACK)

# Main game loop
def main():
    global current_state, current_mystery, current_riddle, user_answer, message, show_hint, input_active
    global start_time, elapsed_time, total_time
    
    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_click = False
        mouse_pos = pygame.mouse.get_pos()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_click = True
                    if current_state == RIDDLE and pygame.Rect(200, 350, 400, 40).collidepoint(mouse_pos):
                        input_active = True
                    else:
                        input_active = False
            
            elif event.type == KEYDOWN:
                if current_state == RIDDLE and input_active:
                    if event.key == K_BACKSPACE:
                        user_answer = user_answer[:-1]
                    elif event.key == K_RETURN:
                        # Submit answer when Enter is pressed
                        input_active = False
                        if user_answer.lower().strip() == mysteries[current_mystery]['riddles'][current_riddle]['answer']:
                            message = "Correct! You solved the riddle."
                            current_state = RIDDLE_RESULT
                        else:
                            message = "Incorrect. Try again."
                    else:
                        user_answer += event.unicode
        
        # Update game state
        update_game_state(mouse_pos, mouse_click)
        
        # Render game
        render_game(window_surface, mouse_pos)
        
        # Update the display
        pygame.display.update()
        clock.tick(60)

def update_game_state(mouse_pos, mouse_click):
    global current_state, current_mystery, current_riddle, user_answer, message, show_hint
    global start_time, elapsed_time, total_time
    
    if current_state == MAIN_MENU:
        if start_button.is_clicked(mouse_pos, mouse_click):
            current_state = MYSTERY_INTRO
            start_time = time.time()
    
    elif current_state == MYSTERY_INTRO:
        if continue_button.is_clicked(mouse_pos, mouse_click):
            current_state = RIDDLE
            user_answer = ""
            show_hint = False
    
    elif current_state == RIDDLE:
        hint_button.check_hover(mouse_pos)
        submit_button.check_hover(mouse_pos)
        
        if hint_button.is_clicked(mouse_pos, mouse_click):
            show_hint = True
        
        if submit_button.is_clicked(mouse_pos, mouse_click):
            if user_answer.lower().strip() == mysteries[current_mystery]['riddles'][current_riddle]['answer']:
                message = "Correct! You solved the riddle."
                current_state = RIDDLE_RESULT
            else:
                message = "Incorrect. Try again."
    
    elif current_state == RIDDLE_RESULT:
        continue_button.check_hover(mouse_pos)
        
        if continue_button.is_clicked(mouse_pos, mouse_click):
            current_riddle += 1
            user_answer = ""
            show_hint = False
            
            if current_riddle >= len(mysteries[current_mystery]['riddles']):
                current_state = MYSTERY_COMPLETE
                current_riddle = 0
            else:
                current_state = RIDDLE
    
    elif current_state == MYSTERY_COMPLETE:
        next_mystery_button.check_hover(mouse_pos)
        
        if next_mystery_button.is_clicked(mouse_pos, mouse_click):
            current_mystery += 1
            
            if current_mystery >= len(mysteries):
                elapsed_time = time.time() - start_time
                total_time += elapsed_time
                current_state = GAME_COMPLETE
            else:
                current_state = MYSTERY_INTRO
    
    elif current_state == GAME_COMPLETE:
        play_again_button.check_hover(mouse_pos)
        
        if play_again_button.is_clicked(mouse_pos, mouse_click):
            reset_game()

def render_game(surface, mouse_pos):
    surface.fill(WHITE)
    
    if current_state == MAIN_MENU:
        render_main_menu(surface, mouse_pos)
    elif current_state == MYSTERY_INTRO:
        render_mystery_intro(surface, mouse_pos)
    elif current_state == RIDDLE:
        render_riddle(surface, mouse_pos)
    elif current_state == RIDDLE_RESULT:
        render_riddle_result(surface, mouse_pos)
    elif current_state == MYSTERY_COMPLETE:
        render_mystery_complete(surface, mouse_pos)
    elif current_state == GAME_COMPLETE:
        render_game_complete(surface, mouse_pos)

def render_main_menu(surface, mouse_pos):
    # Draw title
    title_text = "Mystery Adventures"
    draw_text(title_text, title_font, PURPLE, surface, WINDOW_WIDTH // 2, 150)
    
    # Draw subtitle
    subtitle_text = "Solve mysteries, uncover secrets"
    draw_text(subtitle_text, heading_font, BLUE, surface, WINDOW_WIDTH // 2, 220)
    
    # Draw start button
    start_button.check_hover(mouse_pos)
    start_button.draw(surface)

def render_mystery_intro(surface, mouse_pos):
    # Draw mystery title
    mystery_title = mysteries[current_mystery]['name']
    draw_text(f"Mystery {current_mystery + 1}: {mystery_title}", heading_font, BLUE, surface, WINDOW_WIDTH // 2, 100)
    
    # Draw mystery description
    mystery_desc = mysteries[current_mystery]['description']
    draw_wrapped_text(mystery_desc, text_font, BLACK, surface, WINDOW_WIDTH // 2, 180, 600, "center")
    
    # Draw continue button
    continue_button.check_hover(mouse_pos)
    continue_button.draw(surface)

def render_riddle(surface, mouse_pos):
    # Draw mystery title
    mystery_title = mysteries[current_mystery]['name']
    draw_text(f"Mystery {current_mystery + 1}: {mystery_title}", heading_font, BLUE, surface, WINDOW_WIDTH // 2, 80)
    
    # Draw riddle number
    draw_text(f"Riddle {current_riddle + 1} of 3", text_font, PURPLE, surface, WINDOW_WIDTH // 2, 130)
    
    # Draw riddle question
    riddle_text = mysteries[current_mystery]['riddles'][current_riddle]['question']
    draw_wrapped_text(riddle_text, text_font, BLACK, surface, WINDOW_WIDTH // 2, 180, 600, "center")
    
    # Draw input box
    input_color = GREEN if input_active else GRAY
    pygame.draw.rect(surface, input_color, (200, 350, 400, 40), 2, border_radius=5)
    
    # Draw user input
    input_text = text_font.render(user_answer, True, BLACK)
    surface.blit(input_text, (210, 360))
    
    # Draw hint if requested
    if show_hint:
        hint_text = "Hint: " + mysteries[current_mystery]['riddles'][current_riddle]['hint']
        draw_wrapped_text(hint_text, text_font, RED, surface, WINDOW_WIDTH // 2, 300, 600, "center")
    
    # Draw hint and submit buttons
    hint_button.draw(surface)
    submit_button.draw(surface)
    
    # Draw message if there is one
    if message:
        draw_text(message, text_font, RED, surface, WINDOW_WIDTH // 2, 520)

def render_riddle_result(surface, mouse_pos):
    # Draw success message
    draw_text("Correct Answer!", heading_font, GREEN, surface, WINDOW_WIDTH // 2, 150)
    
    # Draw the riddle and answer
    riddle_text = mysteries[current_mystery]['riddles'][current_riddle]['question']
    answer_text = mysteries[current_mystery]['riddles'][current_riddle]['answer'].capitalize()
    
    draw_wrapped_text(riddle_text, text_font, BLACK, surface, WINDOW_WIDTH // 2, 220, 600, "center")
    draw_text(f"Answer: {answer_text}", text_font, BLUE, surface, WINDOW_WIDTH // 2, 300)
    
    # Draw continue button
    continue_button.check_hover(mouse_pos)
    continue_button.draw(surface)

def render_mystery_complete(surface, mouse_pos):
    # Draw completion message
    mystery_title = mysteries[current_mystery]['name']
    draw_text(f"Mystery {current_mystery + 1} Complete!", heading_font, GREEN, surface, WINDOW_WIDTH // 2, 150)
    draw_text(f"You solved '{mystery_title}'", text_font, BLUE, surface, WINDOW_WIDTH // 2, 220)
    
    # Draw next mystery button or completion message
    if current_mystery < len(mysteries) - 1:
        next_mystery_button.check_hover(mouse_pos)
        next_mystery_button.draw(surface)
        next_mystery_name = mysteries[current_mystery + 1]['name']
        draw_text(f"Next: {next_mystery_name}", text_font, PURPLE, surface, WINDOW_WIDTH // 2, 480)
    else:
        next_mystery_button.text = "Complete Game"
        next_mystery_button.check_hover(mouse_pos)
        next_mystery_button.draw(surface)

def render_game_complete(surface, mouse_pos):
    # Draw completion message
    draw_text("Congratulations!", title_font, GREEN, surface, WINDOW_WIDTH // 2, 150)
    draw_text("You have solved all the mysteries!", heading_font, BLUE, surface, WINDOW_WIDTH // 2, 220)
    
    # Draw completion time
    time_text = f"Total time: {format_time(total_time)}"
    draw_text(time_text, text_font, PURPLE, surface, WINDOW_WIDTH // 2, 280)
    
    # Draw play again button
    play_again_button.check_hover(mouse_pos)
    play_again_button.draw(surface)

if __name__ == "__main__":
    main()
