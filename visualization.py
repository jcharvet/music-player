# visualization.py
import pygame
import random
import threading

class Visualization:
    def __init__(self, player):
        self.player = player
        self.is_running = False
        self.visualization_thread = None

    def start_visualization(self):
        if not self.is_running:
            self.is_running = True
            self.visualization_thread = threading.Thread(target=self.run_visualization)
            self.visualization_thread.start()

    def run_visualization(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Start in windowed mode
        pygame.display.set_caption('Music Visualization')

        last_click_time = 0
        double_click_threshold = 500  # Time in milliseconds

        while self.is_running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Check for double click
                        if current_time - last_click_time < double_click_threshold:
                            pygame.display.toggle_fullscreen()  # Toggle fullscreen
                        last_click_time = current_time

            self.screen.fill((0, 0, 0))  # Fill the screen with black background

            for _ in range(5):  # Draw random circles
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                x = random.randint(0, 800)
                y = random.randint(0, 600)
                radius = random.randint(10, 50)
                pygame.draw.circle(self.screen, color, (x, y), radius)

            pygame.display.flip()
            pygame.time.delay(50)

        pygame.display.quit()  # Quit only the display, not the entire Pygame

    def stop_visualization(self):
        self.is_running = False
        if self.visualization_thread:
            self.visualization_thread.join()

# End of visualization.py
