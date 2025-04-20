import pygame

pygame.init()
pygame.display.set_caption("Pythometry Dash")

global screen, clock
screen = pygame.display.set_mode(vsync=True, flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

class Data:
    # Colors
    WHITE: tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)

    # Misc
    FPS: int = 75

    # Characters
    default_avatar = pygame.image.load("./characters/default.png")

class modelResponse:
    finished: bool = False
    nextFrame: int = None
class Template:
    response = modelResponse
    objects = []

class Player:
    def __init__(self) -> None:
        self.avatar = Data.default_avatar
        self.width: int = 60
        self.height: int = 60
        self.rotation = 0
        self.x: int = 1920/2
        self.y: int = 1080 - self.height

    def draw(self) -> None:
        screen.blit(self.avatar, (self.x, self.y))

class StartingScreen(Template):
    def __init__(self, screen, mainPlayer) -> None:
        self.screen = screen
        self.objects.append(mainPlayer)

    def main(self) -> modelResponse:
        screen.fill(Data.WHITE)
        self.drawObjects()
        return self.response
    
    def drawObjects(self) -> None:
        for object in self.objects:
            object.draw()
            

frames: dict[int, Template] = {0: StartingScreen}
frameCount: int = 0
mainPlayer: Player = Player()
loadedFrames: list[Template] = [frames[0](screen, mainPlayer)]
currentFrame: Template = loadedFrames[0]

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