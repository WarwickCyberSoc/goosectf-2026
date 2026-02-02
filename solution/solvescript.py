import wave
import struct
import numpy as np

def de_xor(flag, key):
    return bytes(
        flag[i] ^ key[i % len(key)]
        for i in range(len(flag))
    )

key = b"DungaDungaDunga"

wave = wave.open("0119.wav", "rb") 
frame_bytes = wave.readframes(wave.getnframes())
sample = np.frombuffer(frame_bytes, dtype=np.int16)
bits = [str(s & 1) for s in sample]
cipher = bytearray()

for i in range(0, len(bits), 8):
    byte = int("".join(bits[i:i+8]), 2)
    cipher.append(byte)


flag = de_xor(cipher, key)
print(cipher)
print(flag.decode())
