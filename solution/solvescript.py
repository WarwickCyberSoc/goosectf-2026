import wave
import struct
import numpy as np

def de_xor(flag, key):
    return bytes(
        flag[i] ^ key[i % len(key)]
        for i in range(len(flag))
    )

key = b"DungaDungaDunga"

with wave.open("0119.wav", "rb") as w:
    frame_bytes = w.readframes(w.getnframes())

sample = np.frombuffer(frame_bytes, dtype=np.int16)
bits = [str(s & 1) for s in sample]
cipher = bytearray()

cipher = bytearray()
for i in range(0, len(bits), 8):
    byte = int("".join(bits[i:i+8]), 2)
    if byte == 0:
        break
    cipher.append(byte)


flag = de_xor(cipher, key)
print(flag.decode())
