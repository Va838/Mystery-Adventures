"""
Helper functions for Mystery Adventures.
Contains utility functions for text rendering, game reset, and time formatting.
"""

from utils.constants import MAIN_MENU

def draw_text(text, font, color, surface, x, y, align="center"):
    """
    Draw text on a surface with alignment options.
    
    Args:
        text: Text to display
        font: Pygame font object
        color: Text color (RGB tuple)
        surface: Surface to draw on
        x, y: Position coordinates
        align: Text alignment ("center" or "left")
        
    Returns:
        int: Height of the rendered text
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "left":
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect.height

def draw_wrapped_text(text, font, color, surface, x, y, max_width, align="left"):
    """
    Draw text that wraps to fit within a maximum width.
    
    Args:
        text: Text to display
        font: Pygame font object
        color: Text color (RGB tuple)
        surface: Surface to draw on
        x, y: Position coordinates
        max_width: Maximum width for text before wrapping
        align: Text alignment ("center" or "left")
        
    Returns:
        int: Total height of all rendered text lines
    """
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = font.size(test_line)[0]
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    total_height = 0
    for i, line in enumerate(lines):
        height = draw_text(line, font, color, surface, x, y + total_height, align)
        total_height += height + 5
    
    return total_height

def reset_game():
    """
    Reset the game state to start a new game.
    
    Note: This function modifies global variables in the main module.
    """
    import sys
    main_module = sys.modules['__main__']
    
    main_module.current_state = MAIN_MENU
    main_module.current_mystery = 0
    main_module.current_riddle = 0
    main_module.user_answer = ""
    main_module.message = ""
    main_module.show_hint = False
    main_module.total_time = 0

def format_time(seconds):
    """
    Format seconds into minutes:seconds string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        str: Formatted time string (MM:SS)
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
