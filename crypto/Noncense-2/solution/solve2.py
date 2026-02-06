from Crypto.Util.number import long_to_bytes, bytes_to_long

# from challenge 1
ciphertexts = ["5e773dcb6983545de0", "297631dd538d655af5"]
tags = ["0f4aa99168f070fc9e3b6a8e0fe7f971", "e00588f92f365f7c629d250d68a79866"]
keystream_bytes = bytes.fromhex("191852b80cc0001b9b")

target_plaintext = b"password1"

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pad16(bytes):
    padding = b"\x00" * (16 - len(bytes))
    padded = bytes + padding
    return padded

# the reduction constant
R = 0xe1000000000000000000000000000000

# multiply binary as polynomials and reduce them - for the ghash function
def gf_mul(x, y):
    z = 0
    for i in range(128):
        if (y >> (127 - i)) & 1:
            z ^= x
        if x & 1:
            x = (x >> 1) ^ R
        else:
            x >>= 1
    return z

# calculate the inverse for the polynomial - for the ghash function
def gf_inv(x):
    r = x
    for _ in range(126):
        r = gf_mul(r, r)
        r = gf_mul(r, x)
    r = gf_mul(r, r)
    return r

# encrypt the password
c3 = xor(target_plaintext, keystream_bytes)
print(f"CIPHERTEXT: {c3.hex()}")

# solve for H^2
c1_padded = pad16(bytes.fromhex(ciphertexts[0]))
c2_padded = pad16(bytes.fromhex(ciphertexts[1]))
c3_padded = pad16(c3)

t1 = bytes.fromhex(tags[0])
t2 = bytes.fromhex(tags[1])

c1_xor_c2 = bytes_to_long(xor(c1_padded, c2_padded))
t1_xor_t2 = bytes_to_long(xor(t1, t2))

inv_c1_xor_c2 = gf_inv(c1_xor_c2)

h2 = gf_mul(t1_xor_t2, inv_c1_xor_c2)

# forge the new authentication tag
c1_xor_c3 = bytes_to_long(xor(c1_padded, c3_padded))
h_c1_xor_c3 = gf_mul(h2, c1_xor_c3)
t3 = xor(long_to_bytes(h_c1_xor_c3, 16), t1)

print(f"AUTHENTICATION TAG: {t3.hex()}")