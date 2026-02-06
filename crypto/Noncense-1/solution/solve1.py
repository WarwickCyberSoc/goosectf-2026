ciphertexts = ["5e773dcb6983545de0", "297631dd538d655af5", "6a473df66fa53f24e6"]
known_plaintext = "GooseCTF{"

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

ciphertexts_bytes = []
for ciphertext in ciphertexts:
    ciphertext_bytes = bytes.fromhex(ciphertext)
    ciphertexts_bytes.append(ciphertext_bytes)
    
key_stream_bytes = xor_bytes(ciphertexts_bytes[0], known_plaintext.encode())

print(f"Keystream Bytes: {key_stream_bytes.hex()} (needed for challenge 2)")

# decrypt each ciphertext
plaintext = ""
for ciphertext_bytes in ciphertexts_bytes:
    plaintext_bytes = xor_bytes(ciphertext_bytes, key_stream_bytes)
    plaintext_section = plaintext_bytes.decode()
    plaintext += plaintext_section
    
print(f"PLAINTEXT: {plaintext}")