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

    # Characters
    default_avatar = pygame.image.load("./characters/default.png")

    # Font Text
    logo = pygame.transform.scale(pygame.image.load("./fontart/logo.png"), (1055,332))

    # Backgrounds
    squares1 = pygame.image.load("./backgrounds/squares1.png")
    squares2 = pygame.image.load("./backgrounds/squares2.png")

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
        self.id: int = id
        self.rotation: int = 0
        self.velocity: int = 0
        self.force: int = 0

        self.jumping: bool = False

    def draw(self) -> None:
        screen.blit(self.avatar, (self.x, self.y))

        if self.jumping:
            if self.force >= 1:
                self.velocity = -5 + (self.force/2)
                self.force -= 1
                self.y -= self.velocity

        if self.y >= 1080-self.height:
            self.jumping, self.velocity, self.force = False, 0, 0
            self.y = 1080-self.height

    def jump(self) -> None:
        if not self.jumping:
            self.force = 20
            self.jumping = True

class Text:
    def __init__(self, img, x: int, y: int, id: int = 0) -> None:
        self.img = img
        self.x: int = x
        self.y: int = y
        self.width: int = 0
        self.height: int = 0
        self.id: int = id

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

        self.bg1, self.bg2 = SimpleArt(Data.squares1, 0, 0, id=1), SimpleArt(Data.squares2, 1920, 0, id=1)

        self.objects.extend((self.bg1,
            self.bg2,
            mainPlayer,
            Text(Data.logo, 432, 0),
        ))

    def main(self) -> modelResponse:
        screen.fill(Data.GREENBLUE)
        self.drawObjects()
        
        for obj in self.objects:
            if obj.id == 1:
                obj.x -= 1
                if obj.x < -1920:
                    obj.x = 1920
            elif obj.id == 2:
                obj.x += 7
                if obj.x > 1920+obj.width:
                    obj.x = 0-obj.width

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            mainPlayer.jump()

        return self.response
    
    def drawObjects(self) -> None:
        for object in self.objects:
            object.draw()

frames: dict[int, Template] = {0: StartingScreen}
frameCount: int = 0
mainPlayer: Player = Player(id=2)
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
        clock.tick(100)