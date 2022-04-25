import time

from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

G = secp256k1.G
n = secp256k1.q
infinity = Point.IDENTITY_ELEMENT

fastec_elapsed = 0

def fastec_timer(func):
    def timing_wrapper(*args, **kwargs):
        global fastec_elapsed
        start = time.time()
        result = func(*args, **kwargs)
        fastec_elapsed += time.time() - start
        return result
    return timing_wrapper

@fastec_timer
def point_add(A, B):
    # Serializing / deserializing when sending points
    # over the network could cause a curve mismatch
    if A != infinity:
        A = Point(A.x, A.y, secp256k1)
    if B != infinity:
        B = Point(B.x, B.y, secp256k1)
    return A + B

@fastec_timer
def point_mul(A, k):
    return A * k

def bytes_from_int(x: int) -> bytes:
    return x.to_bytes(32, byteorder="big")

def bytes_from_point(P: Point) -> bytes:
    return bytes_from_int(P.x)

def int_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")
