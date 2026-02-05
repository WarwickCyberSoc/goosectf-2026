#!/usr/bin/python3

from PIL import Image
import sys
import argparse

def toBits(msg):
    b = ''.join(format(ord(i), '08b') for i in msg)
    return b

def lsbEncode(b, img):
    width, height = img.size
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y)))
            #print(f'1: {pixel}')
            # [194, 190, 179]
            for (i, val) in enumerate(pixel):
                # i = 0, val = 123
                cval = list(f'{val:08b}') # 00110000
                if b: # Check if bits in input message, b = '1001000110...'
                    cval[7] = b[0] # Set last bit
                    b = b[1:] # Pop first item from msg
                else:
                    cval[7] = '0'
                pixel[i] = int(''.join(cval), 2) # Set pixel in base 2
            #print(f'2: {pixel}\n')
            img.putpixel((x, y), tuple(pixel))
    return(img)


def lsbDecode(img):
    b = list()

    width, height = img.size
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y))) # [194, 190, 179]
            for (i, val) in enumerate(pixel): # i = 0, val = 123
                cval = list(f'{val:08b}') # 00110000
                b.append(cval[7]) # get last bit
    byteList = [b[i:i+8] for i in range(0, len(b), 8)]
    charList = []
    for byte in byteList:
        asciiInt = int(''.join(byte), 2) # Converts to decimal number 
        if asciiInt != 0:
            char = chr(asciiInt) # Converts to character
            charList.append(char)
    return(''.join(charList))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='python lsb.py', description='Encodes and decodes messages in images using LSB steganography. It does this over all R,G, and B values for each pixel')
    parser.add_argument('-f', type=str, help='Path to image', required=True, metavar='FILEPATH')
    parser.add_argument('-m', type=str, help='Message to encode', metavar='MESSAGE')
    parser.add_argument('-o', type=str, help='Output file path, saves as PNG', metavar='OUTPUT')
    parser.add_argument('-v', action='store_true', help='View file once encoded')

    if not parser.parse_args().f:
        sys.exit()
    try:
        img = Image.open(parser.parse_args().f)
    except:
        print('Error: Image not found')
        sys.exit()

    if parser.parse_args().m == None:  # if no message, then encode
        print("Decoding Image...")
        msg = lsbDecode(img)
        print(msg)
        sys.exit()

    else: # If message, then encode
        print("Encoding Image...")
        bits = toBits(parser.parse_args().m)
        img = lsbEncode(bits, img)

        if parser.parse_args().o:
            try: # Save image in output path if o present
                # img.save(parser.parse_args().o)
                img.save(parser.parse_args().o, 'PNG')
            except:
                print('Error: Could not save image')

        if parser.parse_args().v or not parser.parse_args().o:
            # If -v or no -o (output), then show image
            img.show()

    sys.exit()
