"""
UI components for Mystery Adventures.
Contains the Button class for interactive UI elements.
"""

import pygame

class Button:
    """
    Button class for creating interactive UI elements.
    """
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        """
        Initialize a new button.
        
        Args:
            x, y: Position coordinates
            width, height: Button dimensions
            text: Button label
            color: Normal button color
            hover_color: Color when mouse hovers over button
            text_color: Color of the button text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        """
        Draw the button on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        from utils.constants import BLACK, button_font
        
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)  # Border
        
        text_surf = button_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, mouse_pos):
        """
        Check if mouse is hovering over button.
        
        Args:
            mouse_pos: Current mouse position (x, y)
            
        Returns:
            bool: True if mouse is over button
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        """
        Check if button is clicked.
        
        Args:
            mouse_pos: Current mouse position (x, y)
            mouse_click: Boolean indicating if mouse was clicked
            
        Returns:
            bool: True if button was clicked
        """
        return self.rect.collidepoint(mouse_pos) and mouse_click
