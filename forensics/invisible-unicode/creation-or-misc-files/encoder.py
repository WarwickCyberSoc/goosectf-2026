plain = input('Enter plain text: ')
binary = ''.join(format(ord(char), '08b') for char in plain)
encoded = ''.join('\uFFA0' if bit == '0' else '\u3164' for bit in binary)

with open('encoded.txt', 'w', encoding='utf-8') as file:
    file.write(encoded)