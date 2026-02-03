encoded = input('Enter encoded text: ')
binary = ''.join('0' if char == '\uFFA0' else '1' if char == '\u3164' else '' for char in encoded)
plain = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

print('"', plain, '"', sep='')