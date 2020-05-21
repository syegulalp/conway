# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision = True
# cython: always_allow_keywords =False
# cython: unraisable_tracebacks = True
# cython: binding = False

from libc.stdlib cimport rand

from cpython cimport array
import cython

DEF WIDTH = 400
DEF HEIGHT = 300

cdef signed int[WIDTH * HEIGHT * 8] lookup
cdef unsigned char[2][4] colors = [[0,0,0,255],[0,255,0,255]]

def init():
    global lookup
    cdef size_t index = 0
    cdef signed int y,x,y3,x3

    for y in range(0,HEIGHT):
        for x in range(0,WIDTH):
            for y3 in range(y-1, y+2):
                if y3<0:
                    y3=HEIGHT-1
                elif y3>HEIGHT-1:
                    y3=0
                for x3 in range (x-1, x+2):
                    if x3<0:
                        x3=WIDTH-1
                    elif x3>WIDTH-1:
                        x3=0
                    if x3 == x and y3 == y:
                        continue
                    lookup[index] = (y3 * WIDTH) + x3
                    index+=1

def randomize(self)->None:
    cdef array.array[unsigned char] _world = self.life[self.world]
    cdef size_t x

    world = _world.data.as_uchars    

    for x in range(0, HEIGHT*WIDTH):
        if rand() % 10 == 1:
            world[x]=1

def generation(self)->None:

    cdef int total, wt, y
    cdef size_t index = 0, xa
    cdef array.array[unsigned char] _w = self.life[self.world]
    cdef array.array[unsigned char] _w2 = self.life[1 - self.world]

    global lookup

    w = _w.data.as_uchars
    w2 = _w2.data.as_uchars

    for xa in range(0, WIDTH*HEIGHT):
        total = 0
        for y in range(0,8):
            total += w[lookup[index]]
            index +=1
        w2[xa] = (1<total<4) if w[xa] else (total==3)

    self.world = not self.world


def render(self)->None:

    cdef array.array[unsigned char] _world = self.life[self.world]
    cdef array.array[unsigned char] _imagebuffer = self.buffer
    cdef size_t j = 0, i, t
    cdef int t1

    world = _world.data.as_uchars
    imagebuffer = _imagebuffer.data.as_uchars    

    for i in range(0, WIDTH*HEIGHT*4, 4):        
        t1 = world[j]
        for t in range(0,4):
            imagebuffer[i+t] = colors[t1][t]
        j += 1