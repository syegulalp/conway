import pyglet

pyglet.options["debug_gl"] = False
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

import array

from timer import Timer

WIDTH = 400
HEIGHT = 300
ZOOM = 3

from life import init, render, generation, randomize


class MyWindow(pyglet.window.Window):
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)
        init(WIDTH, HEIGHT)

        self.batch = pyglet.graphics.Batch()
        self.texture = pyglet.image.Texture.create(WIDTH, HEIGHT)

        self.life = [array.array("B", b"\x00" * WIDTH * HEIGHT) for _ in range(2)]
        self.buffer = array.array("B", b"\x00" * WIDTH * HEIGHT * 4)
        self.sprite = pyglet.sprite.Sprite(
            self.texture,
            0,
            0,
            batch=self.batch,
        )

        self.world = 0

        randomize(self)

        self.life_timer = Timer()
        self.render_timer = Timer()
        self.draw_timer = Timer()

        pyglet.clock.schedule_interval(self.run, 1 / 60)
        pyglet.clock.schedule_interval(self.get_avg, 1.0)

        print("New generation / Display rendering / Draw")

    def get_avg(self, *a):
        print(self.life_timer.avg, self.render_timer.avg, self.draw_timer.avg)

    def run(self, *a):
        with self.life_timer:
            generation(self)
        with self.render_timer:
            render(self)
        self.texture.blit_into(
            pyglet.image.ImageData(WIDTH, HEIGHT, "RGBA", self.buffer.tobytes()),
            0,
            0,
            0,
        )


    def on_draw(self):
        with self.draw_timer:
            pyglet.gl.glViewport(0, 0, WIDTH * (ZOOM**2), HEIGHT * (ZOOM**2))
            self.clear()
            self.batch.draw()


def main():
    w = MyWindow(WIDTH * ZOOM, HEIGHT * ZOOM)
    import gc
    gc.freeze()
    pyglet.app.run()


if __name__ == "__main__":
    main()
