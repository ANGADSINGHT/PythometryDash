import pygame
import os

pygame.init()
pygame.display.set_caption("Pythometry Dash")

global screen, clock
screen = pygame.display.set_mode(vsync=True, flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

class Data:
    # Colors
    SATURATION = 50
    WHITE: tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)
    GREENBLUE: tuple[int, int, int] = (15+SATURATION, 45+SATURATION, 205+SATURATION)

    # Misc
    FPS: int = 75
    squares: list = []

    # Characters
    default_avatar = pygame.image.load("./characters/default.png")

    # Font Text
    logo = pygame.transform.scale(pygame.image.load("./fontart/logo.png"), (1055,332))

    # Squares
    @classmethod
    def load_squares(cls):
        for i in range(1, 17):
            setattr(cls, f"square{i}", SimpleArt(pygame.image.load(f"./squares/square{i}.png"), 0, 0, 0, 0, 1))
        cls.squares.extend(
            getattr(cls, f"square{i}") for i in range(1, 17)
        )

class modelResponse:
    finished: bool = False
    nextFrame: int = None
class Template:
    response = modelResponse
    objects = []

class Player:
    def __init__(self, id: int = 0) -> None:
        self.avatar = Data.default_avatar
        self.width: int = 60
        self.height: int = 60
        self.rotation = 0
        self.x: int = 960
        self.y: int = 1080 - self.height
        self.id = id

    def draw(self) -> None:
        screen.blit(self.avatar, (self.x, self.y))

class Text:
    def __init__(self, img, x: int, y: int, id: int = 0) -> None:
        self.img = img
        self.x = x
        self.y = y
        self.width, height = 0, 0
        self.id = id

    def draw(self) -> None:
        if self.img:
            screen.blit(self.img, (self.x, self.y))

class SimpleArt:
    def __init__(self, img, x: int, y: int, width: int = 0, height: int = 0, id: int = 0):
        self.img = img
        self.x = x
        self.y = y
        self.id = id

    def draw(self):
        if self.img:
            screen.blit(self.img, (self.x, self.y))


class StartingScreen(Template):
    def __init__(self, screen, mainPlayer) -> None:
        self.screen = screen
        # Square Positions
        Data.load_squares()
        Data.square1.xo, Data.square1.yo, Data.square1.width = (0,0, 429)
        Data.square2.xo, Data.square2.yo, Data.square2.width = (0, 426, 568)
        Data.square3.xo, Data.square3.yo, Data.square3.width = (0, 793, 443)
        Data.square4.xo, Data.square4.yo, Data.square4.width = (314, 0, 620)
        Data.square5.xo, Data.square5.yo, Data.square5.width = (314, 189, 460)
        Data.square6.xo, Data.square6.yo, Data.square6.width = (312, 675, 461)
        Data.square7.xo, Data.square7.yo, Data.square7.width = (803, 193, 133)
        Data.square8.xo, Data.square8.yo, Data.square8.width = (803, 345, 133)
        Data.square9.xo, Data.square9.yo, Data.square9.width = (808, 498, 644)
        Data.square10.xo, Data.square10.yo, Data.square10.width = (965, 0, 483)
        Data.square11.xo, Data.square11.yo, Data.square11.width = (1477, 0, 343)
        Data.square12.xo, Data.square12.yo, Data.square12.width = (1476, 68, 337)
        Data.square13.xo, Data.square13.yo, Data.square13.width = (1473, 430, 204)
        Data.square14.xo, Data.square14.yo, Data.square14.width = (1731, 429, 195)
        Data.square15.xo, Data.square15.yo, Data.square15.width = (1476, 663, 460)
        Data.square16.xo, Data.square16.yo, Data.square16.width = (1852, 2, 81)
        for sqr in Data.squares: sqr.x, sqr.y = sqr.xo, sqr.yo

        self.objects.extend(Data.squares)
        self.objects.extend((mainPlayer,
            Text(Data.logo, 432, 0),
        ))

    def main(self) -> modelResponse:
        screen.fill(Data.GREENBLUE)
        self.drawObjects()
        for obj in self.objects:
            if obj.id == 1:
                obj.x -= 1
            if obj.x <= 0-obj.width:
                obj.x = 1920 + obj.xo

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