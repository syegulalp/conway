import pyglet

pyglet.options["debug_gl"] = False
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

import array
import random

from timer import Timer

WIDTH = 400
HEIGHT = 300
ZOOM = 3


class MyWindow(pyglet.window.Window):
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)

        self.batch = pyglet.graphics.Batch()
        self.texture = pyglet.image.Texture.create(WIDTH, HEIGHT, rectangle=True)

        self.life = [array.array("B", b"\x00" * WIDTH * HEIGHT) for _ in range(2)]
        self.buffer = array.array("B", b"\x00" * WIDTH * HEIGHT * 4)
        self.sprite = pyglet.sprite.Sprite(
            self.texture,
            0,
            0,
            batch=self.batch,
        )

        self.colors = [
            array.array("B", b"\x00\x00\x00\xff"),
            array.array("B", b"\x00\xff\x00\xff"),
        ]

        self.world = 0

        self.lookup = []

        # Create lookup table for generation

        for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                for y3 in range(y - 1, y + 2):
                    if y3 < 0:
                        y3 = HEIGHT - 1
                    elif y3 > HEIGHT - 1:
                        y3 = 0
                    for x3 in range(x - 1, x + 2):
                        if x3 < 0:
                            x3 = WIDTH - 1
                        elif x3 > WIDTH - 1:
                            x3 = 0
                        if x3 == x and y3 == y:
                            continue
                        self.lookup.append((y3 * WIDTH) + x3)

        self.randomize()

        self.life_timer = Timer()
        self.render_timer = Timer()
        self.draw_timer = Timer()

        pyglet.clock.schedule_interval(self.run, 1 / 60)
        pyglet.clock.schedule_interval(self.get_avg, 1.0)

        print("New generation / Display rendering / Draw")

    def get_avg(self, *a):
        print(self.life_timer.avg, self.render_timer.avg, self.draw_timer.avg)

    def randomize(self):
        """
        Fill field with random blocks.
        """
        b = self.life[self.world]
        c = random.choice

        for n in range(WIDTH * HEIGHT):
            b[n] = 1 if random.randrange(0, 9) == 1 else 0

    def generation(self):
        """
        Optimized generation algorithm using lookup table.
        """

        index = 0
        lookup = self.lookup
        w = self.life[self.world]
        w2 = self.life[not self.world]
        r = range(0, 8)

        for xa in range(0, WIDTH * HEIGHT):
            total = 0
            for y in r:
                total += w[lookup[index]]
                index += 1
            w2[xa] = (1 < total < 4) if w[xa] else (total == 3)

        self.world = not self.world

    def render(self):
        """
        Render current generation to screen buffer.
        """
        b = self.life[self.world]
        bd = self.buffer
        c = self.colors
        i = 0
        for n in range(0, HEIGHT * WIDTH):
            bd[i : i + 4] = c[b[n] > 0]
            i += 4

        self.texture.blit_into(
            pyglet.image.ImageData(WIDTH, HEIGHT, "RGBA", self.buffer.tobytes()),
            0,
            0,
            0,
        )

    def run(self, *a):

        # TODO: don't block the main thread

        with self.life_timer:
            self.generation()
        with self.render_timer:
            self.render()

    def on_draw(self):
        with self.draw_timer:
            pyglet.gl.glViewport(0, 0, WIDTH * (ZOOM ** 2), HEIGHT * (ZOOM ** 2))
            self.clear()
            self.batch.draw()


def main():
    w = MyWindow(WIDTH * ZOOM, HEIGHT * ZOOM)
    import gc

    gc.freeze()
    pyglet.app.run()


if __name__ == "__main__":
    main()
