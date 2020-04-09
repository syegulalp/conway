import pyglet
import array
import random

from timer import Timer

pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

WIDTH = 400
HEIGHT = 300

from life import init, render, generation, randomize

class MyWindow(pyglet.window.Window):
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)

        self.batch = pyglet.graphics.Batch()
        self.texture = pyglet.image.Texture.create(WIDTH, HEIGHT, rectangle=True)

        self.life = [array.array("B", b"\x00" * WIDTH * HEIGHT) for _ in range(2)]
        self.buffer = array.array("B", b"\x00" * WIDTH * HEIGHT * 4)
        self.sprite = pyglet.sprite.Sprite(self.texture, 0, 0, batch=self.batch,)

        self.world = 0

        init()
        randomize(self)

        self.timer = Timer()

        pyglet.clock.schedule_interval(self.run, 1/60)
        pyglet.clock.schedule_interval(self.get_avg, 1.0)

    def get_avg(self, *a):
        print(self.timer.avg)

    def run(self, *a):
        with self.timer:
            generation(self)
        render(self)        
        self.texture.blit_into(
            pyglet.image.ImageData(WIDTH, HEIGHT, "RGBA", self.buffer.tobytes()), 0, 0, 0
        )
    
    def on_draw(self):        
        pyglet.gl.glViewport(0, 0, 400 * 9, 300 * 9)
        self.clear()
        self.batch.draw()

if __name__=="__main__":
    w = MyWindow(1200,900)
    pyglet.app.run()
