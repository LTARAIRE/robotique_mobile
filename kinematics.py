import constants
import math
import numpy as np

def computeDK(teta1, teta2, teta3):
    # coordonées de P1
    x1 = constants.constL1 * math.cos(teta1)
    y1 = constants.constL1 * math.sin(teta1)
    z1 = 0

    # coorconées de P2
    l2proj = constants.constL2 * math.cos(teta2)
    x2 = (constants.constL1 + l2proj) * math.cos(teta1)
    y2 = (constants.constL1 + l2proj) * math.sin(teta1)
    z2 = constants.constL2 * math.sin(teta2)

    # coordonées de P3
    alpha = teta3 + teta2
    l3proj = constants.constL3 * math.cos(alpha)
    dp = constants.constL3 * math.sin(alpha)
    lproj = constants.constL1 + l2proj + l3proj
    x3 = lproj * math.cos(teta1)
    y3 = lproj * math.sin(teta1)
    z3 = z2 + dp

    return [x3, y3, -z3]

def computeIK(x3, y3, z3):

    L1=constants.constL1
    L2=constants.constL2
    L3=constants.constL3
    lproj = math.sqrt(x3 ** 2 + y3 ** 2)
    d13 = lproj - constants.constL1
    d = math.sqrt(z3 ** 2 + d13 ** 2)
    a = math.atan2(z3, d13)
    b= alkashi(L2,d,L3)

    teta1 = math.atan2(y3, x3)
    teta2 = a + b
    teta3 = alkashi(L2,L3,d)+math.pi

    return [teta1, -teta2, -teta3]

def alkashi(a,b,c):
    if a == 0 or b == 0:
        return 0
    c=((a**2+b**2-c**2)/(2*a*b))
    if c > 1:
        c = 1
    elif c < -1:
        c = -1
    #return math.acos(max(-1,min(1,(a**2+b**2-c**2)/(2*a*b))))
    return math.acos(c)


def triangle(x, z, h, w, t):

    points = [
        np.array([x, w/2, z]),
        np.array([x, -w/2, z]),
        np.array([x, 0, h+z])
    ]

    """
    alpha=t%1

    A= points[int(t)%3] 
    B= points[(int(t)+1)%3]

    M= [
        alpha * (B[0]-A[0])+A[0],
        alpha * (B[1]-A[1])+A[1],
        alpha * (B[2]-A[2])+A[2]
    ]
    """
    """
    M=[
        points[2][0],points[2][1],points[2][2]
    ]
    """
    print(f"temps:{t}")
    alpha=math.fmod(t,1)
    print(f"alpha:{alpha}")
    #M=points[2]
    #M=alpha *(B-A)+B
    point1=points[int(t)%3]
    point2=points[int(t+1)%3]

    M=alpha*(point2-point1)+point1
    print(int(t)%3)

    return computeIK(M[0],M[1],M[2])

def segment(x1,y1,z1,x2,y2,z2,t, duration):
    points = [
        np.array([x1,y1,z1]),
        np.array([x2,y2,z2])
    ]
    alpha = math.fmod(t,duration)/duration
    point1=points[int(t/duration)%2]
    point2=points[int(t/duration+1)%2]
    #point1=points[0]
    #point2=points[1]

    M=alpha*(point2-point1)+point1
    #print(duration)
    #print(t)
    print(int(t/duration)%2)
    print(int(t / duration+1) % 2)
    #print(alpha)

    return computeIK(M[0],M[1],M[2])