# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision = True
# cython: always_allow_keywords =False
# cython: unraisable_tracebacks = True
# cython: binding = False

from libc.stdlib cimport rand

from cpython.mem cimport PyMem_Malloc
from cpython cimport array
import cython

cdef class MemObj:
    
    cdef signed int* data
    cdef int height, width, array_size, display_size, size

    def __cinit__(self, int width, int height):
        self.height = height
        self.width = width
        self.size = height * width
        self.array_size = self.size * 8
        self.display_size = self.size * 4
        self.data = <signed int*> PyMem_Malloc(self.array_size * sizeof(signed int))

        cdef size_t index = 0
        cdef signed int y,x,y3,x3,y4

        for y in range(0,height):
            for x in range(0,width):
                for y3 in range(y-1, y+2):
                    if y3<0:
                        y3=height-1
                    elif y3>height-1:
                        y3=0
                    y4 = y3 * width
                    for x3 in range (x-1, x+2):
                        if x3<0:
                            x3=width-1
                        elif x3>width-1:
                            x3=0
                        if x3 == x and y3 == y:
                            continue
                        self.data[index] = y4 + x3
                        index+=1    


cdef unsigned char[2][4] colors = [[0,0,0,255],[0,255,0,255]]
cdef MemObj lookup

def init(int width, int height):
    global lookup
    lookup = MemObj(width, height)    


def randomize(self)->None:
    cdef array.array[unsigned char] _world = self.life[self.world]
    cdef size_t x, s

    world = _world.data.as_uchars    
    s = lookup.size

    for x in range(0, s):
        if rand() % 10 == 1:
            world[x]=1

def generation(self)->None:

    cdef int total, wt, y
    cdef size_t index = 0, xa, s
    cdef array.array[unsigned char] _w = self.life[self.world]
    cdef array.array[unsigned char] _w2 = self.life[1 - self.world]

    l= lookup.data
    s = lookup.size

    w = _w.data.as_uchars
    w2 = _w2.data.as_uchars

    for xa in range(0, s):
        total = 0
        for y in range(0,8):
            total += w[l[index]]
            index +=1
        w2[xa] = (1<total<4) if w[xa] else (total==3)

    self.world = not self.world


def render(self)->None:

    cdef array.array[unsigned char] _world = self.life[self.world]
    cdef array.array[unsigned char] _imagebuffer = self.buffer
    cdef size_t j = 0, i, t, s
    cdef int t1

    world = _world.data.as_uchars
    imagebuffer = _imagebuffer.data.as_uchars    
    s = lookup.display_size

    for i in range(0, s, 4):        
        t1 = world[j]
        for t in range(0,4):
            imagebuffer[i+t] = colors[t1][t]
        j += 1