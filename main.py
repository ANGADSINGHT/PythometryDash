import pygame

pygame.init()
pygame.display.set_caption("Pythometry Dash")

class Data:
    # Colors
    WHITE: tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)

    # Misc
    FPS: int = 75

class modelResponse:
    finished: bool = False
    nextFrame: int = None

class ResponseTemplate:
    response = modelResponse

global screen, clock
screen = pygame.display.set_mode(vsync=True, flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

class StartingScreen(ResponseTemplate):
    def __init__(self, screen) -> None:
        self.screen = screen

    def main(self) -> modelResponse:
        screen.fill(Data.WHITE)
        return self.response

        

            

frames: dict[int, ResponseTemplate] = {0: StartingScreen}
frameCount: int = 0
loadedFrames: list[ResponseTemplate] = [frames[0](screen)]
currentFrame: ResponseTemplate = loadedFrames[0]

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        response = currentFrame.main()
        if response.finished:
            currentFrame = next(x for x in loadedFrames if isinstance(x, frames[response.nextFrame]))


        pygame.display.flip()
        clock.tick(75)