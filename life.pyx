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

cdef signed int[WIDTH * HEIGHT * 9] lookup

cdef array.array green = array.array("B", b'\x00\xff\x00\xff')
cdef array.array black = array.array("B", b'\x00\x00\x00\xff')

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
                    lookup[index] = (y3 * WIDTH) + x3
                    index+=1

def randomize(self)->None:
    cdef array.array[unsigned char] _world = self.life[self.world]
    world = _world.data.as_uchars
    cdef int y,x

    for y in range(0,HEIGHT):
        for x in range(0, WIDTH):
            if rand() % 10 == 1:
                world[(y*WIDTH)+x]=1

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
        for y in range(0,9):
            total += w[lookup[index]]
            index +=1
        wt = w[xa]
        total -=wt
        w2[xa] = (1<total<4) if wt!=0 else (total==3)

    self.world = not self.world

def render(self)->None:
    cdef array.array[unsigned char] _world = self.life[self.world]
    cdef array.array[unsigned char] _imagebuffer = self.buffer
    cdef size_t j = 0, i, t
    cdef unsigned char[4] color

    g2 = green.data.as_uchars
    b2 = black.data.as_uchars

    world = _world.data.as_uchars
    imagebuffer = _imagebuffer.data.as_uchars    

    for i in range(0, WIDTH*HEIGHT*4, 4):        
        color = g2 if world[j] else b2
        for t in range(0,4):
            imagebuffer[i+t] = color[t]
        j += 1    