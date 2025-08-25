import pygame

class FirstPersonInput:
    def __init__(self, sensitivity=0.12):
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self.sensitivity = sensitivity
        self._quit = False

    def quit_pressed(self):
        for e in pygame.event.get(pygame.QUIT):
            self._quit = True
        for e in pygame.event.get(pygame.KEYDOWN):
            if e.key == pygame.K_ESCAPE:
                self._quit = True
        return self._quit

    def keys(self):
        return pygame.key.get_pressed()

    def sprinting(self):
        return pygame.key.get_pressed()[pygame.K_LSHIFT]

    def update_mouse(self, yaw, pitch):
        dx, dy = pygame.mouse.get_rel()
        yaw += dx * self.sensitivity
        pitch -= dy * self.sensitivity
        pitch = max(-89.9, min(89.9, pitch))
        return yaw, pitch
