# visualization.py
import pygame
import random
import threading
import math

class Visualization:
    def __init__(self, player, stop_callback=None):
        self.player = player
        self.stop_callback = stop_callback  # Store the callback function
        self.is_running = False
        self.visualization_thread = None
        self.fullscreen = False  # Track the fullscreen state

    def start_visualization(self):
        if not self.is_running:
            self.is_running = True
            self.visualization_thread = threading.Thread(target=self.run_visualization)
            self.visualization_thread.start()


    def run_visualization(self):
        pygame.init()

        # Set the desired windowed mode size
        windowed_size = (800, 600)  # You can adjust this to your preferred size
        self.screen = pygame.display.set_mode(windowed_size)
        pygame.display.set_caption('Music Visualization')

        last_click_time = 0
        double_click_threshold = 500  # Time in milliseconds

        self.fullscreen = False  # Start with fullscreen mode off

        while self.is_running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Exit fullscreen mode when Escape is pressed
                        self.fullscreen = False
                        self.screen = pygame.display.set_mode(windowed_size)  # Switch back to windowed mode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Check for double click
                        if current_time - last_click_time < double_click_threshold:
                            self.fullscreen = not self.fullscreen  # Toggle the fullscreen flag
                            if self.fullscreen:
                                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            else:
                                self.screen = pygame.display.set_mode(windowed_size)
                        last_click_time = current_time

            # Recalculate the center based on the current mode
            center_x, center_y = self.screen.get_width() // 2, self.screen.get_height() // 2
            base_radius = min(center_x, center_y) // 2  # Base radius for the pulsing circle

            self.screen.fill((0, 0, 0))  # Fill the screen with black background

            # Calculate the pulsing effect
            time_ms = pygame.time.get_ticks()
            pulse_radius = int(base_radius + math.sin(time_ms / 500) * 10 + 50)  # Adjust the base_radius if necessary
            
            # Draw the pulsing circle
            color = (255, 0, 0)  # Red color
            pygame.draw.circle(self.screen, color, (center_x, center_y), pulse_radius)

            pygame.display.flip()
            pygame.time.delay(50)

        pygame.display.quit()  # Quit only the display, not the entire Pygame




    def stop_visualization(self):
        self.is_running = False
        if self.visualization_thread:
            self.visualization_thread.join()
        pygame.display.quit()  # Ensure the display is quit properly

        if self.stop_callback:
            self.stop_callback()  # Call the callback function when visualization stops

# End of visualization.py
