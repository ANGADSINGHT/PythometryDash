SHOW_FPS = True

import pygame
from colorama import Fore, init
init()

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
    pmode: bool = False

    # Characters
    default_avatar = pygame.image.load("./characters/default.png")

    # Font Text
    logo = pygame.transform.scale(pygame.image.load("./fontart/logo.png"), (1055,332))
    font = pygame.font.Font("fonts/minecraft_font.ttf", 30)

    # Backgrounds
    squares1 = pygame.image.load("./backgrounds/squares1.png")
    squares2 = pygame.image.load("./backgrounds/squares2.png")

    # Logger Types
    INFO = 1

    @classmethod
    def log(_, type: int, msg: str) -> None:
        if type == Data.INFO:
            print(Fore.CYAN + "[Info] {}".format(msg) + Fore.RESET)

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
        self.velocity: int = 0
        self.force: int = 0
        self.what = 0
        self.jumping: bool = False
        self.jump_progress: int = 0
        self.jump_total_frames: int = 22
        self.start_rotation: int = 0

    def draw(self) -> None:
        if not Data.pmode:
            if self.jumping:
                if self.jump_progress == 0:
                    self.start_rotation = self.rotation
                self.jump_progress += 1

                self.rotation = self.start_rotation - int(90 * (self.jump_progress / self.jump_total_frames))
                change = self.force / 2 if self.force > 1 else 0

                self.velocity += self.force + -2
                self.force = change
                self.y -= self.velocity
                if self.y > 1067-self.height or self.jump_progress >= self.jump_total_frames:
                    self.jumping, self.velocity, self.force  = False, 0, 0
                    self.rotation = self.start_rotation + 90
                    self.jump_progress = 0
            
            rotated_avatar = pygame.transform.rotate(self.avatar, self.rotation)
            rect = rotated_avatar.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(rotated_avatar, rect.topleft)

    def jump(self) -> None:
        if not self.jumping:
            self.jumping = True
            self.force = 10
            self.jump_progress = 0

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
    def __init__(self, img, x: int, y: int, width: int = 0, height: int = 0, id: int = 0, forceDraw: bool = False) -> None:
        self.img = img
        self.x = x
        self.y = y
        self.id = id
        self.sub_rect = pygame.Rect(0, 0, 1920, 1080)
        self.forceDraw = forceDraw

    def draw(self) -> None:
        if not (self.forceDraw and Data.pmode):
            if self.img:
                screen.blit(self.img, (self.x, self.y), self.sub_rect)

class Notification:
    def __init__(self, text: str, time: int) -> None:
        self.text = text
        self.time = time
        self.expired = False
    
    def draw(self) -> None:
        rendered_text = Data.font.render(self.text, True, Data.WHITE)
        words = self.text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if Data.font.size(test_line)[0] > screen.get_width() - 1500:
                lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line = test_line

        lines.append(current_line.strip())

        y_offset = 10
        for line in lines:
            rendered_text = Data.font.render(line, True, Data.WHITE)
            screen.blit(rendered_text, (10, y_offset))
            y_offset += Data.font.get_linesize()
        
        self.time -= 1
        if self.time <= 0:
            self.expired = True

class StartingScreen(Template):
    def __init__(self, screen, mainPlayer) -> None:
        self.screen = screen
        self.bg1, self.bg2 = SimpleArt(Data.squares1, 0, 0, id=1), SimpleArt(Data.squares2, 1920, 0, id=1)
        self.lagTime: int = 0
        self.notifs: list[Notification] = []
        pygame.mixer.music.load("./music/menu.mp3")
        pygame.mixer.music.play(-1)

        self.objects.extend((self.bg1,
            self.bg2,
            mainPlayer,
            Text(Data.logo, 432, 0),
        ))

    def main(self, events) -> modelResponse:
        self.drawObjects()
        self.drawNotifications()

        if not mainPlayer.jumping: 
            mainPlayer.jump()
        
        if not Data.pmode:
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

        if clock.get_fps() < 5000:
            self.lagTime += 1

        if self.lagTime >= 360:
            self.notifs.append(Notification("The game is too laggy! Please quit.",300))
        elif self.lagTime >= 60 and not Data.pmode:
            Data.pmode = True
            self.notifs.append(Notification("Performance Mode was automatically turned on.",300))
            Data.log(Data.INFO, f"Performance mode automatically turned on")
            

        for event in events:
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_LCTRL] and event.key == pygame.K_p:
                    Data.pmode = not Data.pmode
                    Data.log(Data.INFO, f"Performance mode = {Data.pmode}")

        return self.response
    
    def drawObjects(self) -> None:
        for object in self.objects:
            object.draw()

    def drawNotifications(self) -> None:
        for notif in self.notifs:
            notif.draw()
            if notif.expired: 
                self.notifs.remove(notif)

frames: dict[int, Template] = {0: StartingScreen}
frameCount: int = 0
mainPlayer: Player = Player(id=2)
loadedFrames: list[Template] = [frames[0](screen, mainPlayer)]
currentFrame: Template = loadedFrames[0]

if __name__ == "__main__":
    while running:
        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        response = currentFrame.main(events)
        if response.finished:
            currentFrame = next(x for x in loadedFrames if isinstance(x, frames[response.nextFrame]))

        if SHOW_FPS:
            fps_text = Data.font.render(f"FPS: {int(clock.get_fps())}", True, Data.WHITE)
            screen.blit(fps_text, (0, 1080 - fps_text.get_height() - 10))


        pygame.display.flip()
        clock.tick(100)