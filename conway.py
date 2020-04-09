import pyglet
import array
import random

from timer import Timer

pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

WIDTH = 400
HEIGHT = 300


class MyWindow(pyglet.window.Window):
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)

        self.batch = pyglet.graphics.Batch()
        self.texture = pyglet.image.Texture.create(WIDTH, HEIGHT, rectangle=True)

        self.life = [array.array("B", b"\x00" * WIDTH * HEIGHT) for _ in range(2)]
        self.buffer = array.array("B", b"\x00" * WIDTH * HEIGHT * 4)
        self.sprite = pyglet.sprite.Sprite(self.texture, 0, 0, batch=self.batch,)

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
                        self.lookup.append((y3 * WIDTH) + x3)

        self.randomize()

        self.timer = Timer()

        pyglet.clock.schedule_interval(self.run, 1 / 60)
        pyglet.clock.schedule_interval(self.get_avg, 1.0)

    def get_avg(self, *a):
        print(self.timer.avg)

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

        for xa in range(0, WIDTH * HEIGHT):
            total = 0
            for y in range(0, 9):
                total += 1 if w[lookup[index]] != 0 else 0
                index += 1
            wt = w[xa]
            if wt != 0:
                total -= 1
            w2[xa] = (1 < total < 4) if wt != 0 else (total == 3)

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
        with self.timer:
            self.generation()
        self.render()

    def on_draw(self):
        pyglet.gl.glViewport(0, 0, 400 * 9, 300 * 9)
        self.clear()
        self.batch.draw()


if __name__ == "__main__":
    w = MyWindow(1200, 900)
    pyglet.app.run()
