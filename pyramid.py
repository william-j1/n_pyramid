'''
William Johnson <williamj.inbox@gmail.com>
---
My method: Model the _origin_ edge of the base into an empty 2-dimensional space. 

1. Start with the origin equal to v1(0, 0)
2. The secondary vertex which defines the origin edge is always equal to v2(length, 0)
3. Divide a full circumference by n_sides to yield an angle of change denoted _theta_
4. Given _theta_, always borrow the properties from the last vertex to define the next edge and add the original length
5. Perform a transformation on this vertex to plot the next point that need exist on the invisible circumference 
6. Repeat from step 4 until origin point is reached using _delta_ to sum the "angle of change"
7. Given a vertex (or edge list) obtain a midpoint (centroid) and render a triangle
8. Solve its area, multiply for n_sides and finally multiply the apex height and scale 1/3.
'''
import argparse
import math
import sys

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def rotate(self, degrees, pivot):
        t1 = self.x - pivot.x
        t2 = self.y - pivot.y
        radians = (degrees * math.pi) / 180.0
        s = math.sin(radians)
        c = math.cos(radians)
        dx = t1 * c - t2 * s
        dy = t1 * s + t2 * c
        self.x = dx + pivot.x
        self.y = dy + pivot.y
    def x(self):
        return self.x
    def y(self):
        return self.y

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def v1(self):
        return self.v1
    def v2(self):
        return self.v2

class Triangle:
    def __init__(self, p, q, r):
        self.p = p
        self.q = q
        self.r = r
    def area(self):
        # Heron - greek mathematician used the _semi_ parameter
        # for obtaining the area in respect to variable length sides
        d1 = math.pow(math.pow(self.p.x-self.q.x, 2) + math.pow(self.p.y-self.q.y, 2), 0.5)
        d2 = math.pow(math.pow(self.q.x-self.r.x, 2) + math.pow(self.q.y-self.r.y, 2), 0.5)
        d3 = math.pow(math.pow(self.r.x-self.p.x, 2) + math.pow(self.r.y-self.p.y, 2), 0.5)
        s = (d1 + d2 + d3) / 2
        return math.pow(s * (s - d1) * (s - d2) * (s - d3), 0.5)

def main():

    try:
        p = argparse.ArgumentParser(description="parameters for n-sided pyramid")
        p.add_argument('n', type=int, help='the number (n) of sides')
        p.add_argument('l', type=float, help='the uniform base edge length (l)')
        p.add_argument('h', type=float, help='apex height for n-sided pyramid ')
        args = p.parse_args()
    except:
        print('parameter(s) missing or of the wrong data type')
        sys.exit()

    # if is less-than 3 sides or edge length equal to zero
    if args.n < 3 or args.l == 0:
        sys.exit()

    # angle of change (theta)
    theta = 360.0 / args.n

    # baseline (origin)
    p = Vertex(0, 0)

    # offset inherits length property l
    q = Vertex(args.l, 0)

    # last edge defined
    r = Edge(p, q)

    # intermediate change inside boundary
    delta = theta

    # sigma (x, y)
    sx = args.l
    sy = 0

    # for n-1
    for n in range(1, args.n):

        # copy _of_ last vertex
        p = r.v2

        # offset using length property l
        q = Vertex(r.v2.x + args.l, r.v2.y)

        # rotate vertex q using angular offset
        q.rotate(delta, p)

        # last edge defined
        r = Edge(p, q)

        # vertex sigma
        sx += q.x
        sy += q.y

        # adjust angular offset
        delta += theta

    # divide by n vertices to obtain centroid
    sx /= args.n
    sy /= args.n

    # construct triangular object
    t = Triangle(Vertex(0, 0), Vertex(args.l, 0), Vertex(sx, sy))

    # sides * area * apex height * (1/3)
    v = args.n * t.area() * args.h * 1/3
    print(str(v))

if __name__ == "__main__":
    main()
