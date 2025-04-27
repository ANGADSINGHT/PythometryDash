SHOW_FPS = True
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

import arcade
from colorama import Fore, init
init()
global screen, clock
running = True

class Data:
    # Misc
    FPS: int = 75
    pmode: bool = False

    # Characters
    default_avatar = arcade.load_texture("./characters/default.png")

    # Font Text
    logo = arcade.load_texture("./fontart/logo.png")

    # Backgrounds
    squares1 = arcade.load_texture("./backgrounds/squares1.png")
    squares2 = arcade.load_texture("./backgrounds/squares2.png")

    # Logger Types
    INFO = 1

    # Colors
    BLACK = arcade.color.BLACK
    WHITE = arcade.color.WHITE

    @classmethod
    def log(cls, type: int, msg: str) -> None:
        if type == cls.INFO:
            print(Fore.CYAN + "[Info] {}".format(msg) + Fore.RESET)

class modelResponse:
    finished: bool = False
    nextFrame: int = None
class Template:
    response = modelResponse
    objects = []

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("./characters/default.png")
        self.width = 60
        self.height = 60
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 60
        self.rotation = 0
        self.velocity = 0
        self.force = 0
        self.jumping = False
        self.jump_progress = 0
        self.jump_total_frames = 22
        self.start_rotation = 0

    def update(self):
        print(self._position)
        if self.jumping:
            if self.jump_progress == 0:
                self.start_rotation = self.angle
            self.jump_progress += 1

            self.angle = self.start_rotation - int(90 * (self.jump_progress / self.jump_total_frames))
            change = self.force / 2 if self.force > 1 else 0

            if self.center_y > SCREEN_HEIGHT - 13 - self.height or self.jump_progress >= self.jump_total_frames:
                self.jumping = False
                self.velocity = 0
                self.force = 0
                self.angle = self.start_rotation + 90
                self.jump_progress = 0

            self.velocity += self.force + -2
            self.force = change
            self.center_y -= self.velocity

    def jump(self) -> None:
        if not self.jumping:
            self.jumping = True
            self.force = 10
            self.jump_progress = 0


player = arcade.Sprite()

class SimpleArt:
    def __init__(self, texture, left: int, right: int, x: int, y: int, bottom: int, top: int, width: int, height: int):
        self.texture = texture
        self.left, self.right, self.x, self.y, self.bottom, self.top, self.width, self.height = left, right, x, y, bottom, top, width, height

    def draw(self):
        my_rect = arcade.Rect(
            left=self.left,
            right=self.right,
            x=self.x,
            y=self.y,
            bottom=self.bottom,
            top=self.top,
            width=self.width,
            height=self.height
        )
        arcade.draw_texture_rect(
            texture=self.texture,
            rect=my_rect,
        )


class Notification:
    def __init__(self, text: str, time: int):
        self.text = text
        self.time = time
        self.expired = False

    def update(self):
        self.time -= 1
        if self.time <= 0:
            self.expired = True

    def draw(self):
        notif = arcade.Text(text=self.text, x=10, y=10, color=Data.WHITE, anchor_y="top")
        notif.draw()

class StartingScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg1 = SimpleArt(Data.squares1, 0, 0, 0, 540, 0, 0, 1920, 1080)
        self.bg2 = SimpleArt(Data.squares2, 0, 1920, 1920, 540, 0, 0, 1920, 1080)
        self.sprites = arcade.SpriteList()
        self.player = Player()
        self.notifs = []
        self.lagTime = 0
        self.menu_music = arcade.Sound("./music/menu.mp3")
        self.music_player = None
        self.sprites.extend((
            self.player,
        ))
        self.to_update = (self.player,)

    def on_show(self):
        arcade.set_background_color(Data.BLACK)

    def on_draw(self):
        if self.music_player is None or not self.music_player.playing:
            self.music_player = self.menu_music.play(loop=True)

        self.bg1.draw()
        self.bg2.draw()
        self.sprites.draw()

        my_rect = arcade.Rect(
            left=0,
            right=0,
            x=960,
            y=860,
            bottom=0,
            top=0,
            width=1055,
            height=332
        )
        arcade.draw_texture_rect(rect=my_rect, texture=Data.logo)

        for notif in self.notifs:
            notif.update()
            notif.draw()

        if SHOW_FPS:
            fps = arcade.get_fps()
            fps_text = arcade.Text(f"FPS: {int(fps)}", 10, 10, arcade.color.WHITE, 14)
            fps_text.draw()

    def on_update(self, delta_time):
        for obj in self.to_update:
            obj.update()

        if not Data.pmode:
            self.bg1.x -= 1
            if self.bg1.x < -1920:
                self.bg1.x = 1920

            self.bg2.x -= 1
            if self.bg2.x < -1920:
                self.bg2.x = 1920

        for notif in self.notifs:
            notif.update()
        self.notifs = [notif for notif in self.notifs if not notif.expired]

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player.jump()
        if key == arcade.key.P and modifiers & arcade.key.MOD_CTRL:
            Data.pmode = not Data.pmode
            Data.log(Data.INFO, f"Performance mode = {Data.pmode}")
        if key == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pythometry Dash", fullscreen=True)
    start_screen = StartingScreen()
    window.show_view(start_screen)
    arcade.run()

if __name__ == "__main__":
    main()