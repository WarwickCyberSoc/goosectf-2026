import sys

BIT_COUNT = 7

def rotate_right(num, rot_count):
    return (num >> rot_count) | (num << BIT_COUNT - rot_count) & 0x7F

cyphered = sys.stdin.buffer.read()
flag = "".join(chr(rotate_right(b, 6)) for b in cyphered)
print(flag)