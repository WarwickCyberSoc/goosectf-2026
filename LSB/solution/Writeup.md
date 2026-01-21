# Writeup
This image has an encoded flag using Least Significant Bit (LSB) steganography. 

### What is LSB steganography?
LSB is a technique used to hide data by replacing the smallest (least significant) bit of each number (usually a pixel in an image) with each bit of a secret message.

### How does it work?
A pixel is encoded with 3 numerical values: Red, Green, and Blue (RGB). Each of these values range from 0 to 255.

Here is an example of an orange pixel encoding:

In decimal:`[231, 165, 0]`

In binary:`[11100111, 10100101, 00000000]`

We can hide our message in the least significant bit (the last and lowest bit) of each pixel's RGB values.

To hide the letter `A`, we can encode it as its ASCII value in binary.
- In English: `A`
- In ASCII: 65
- In binary: `[0, 1, 0, 0, 0, 0, 0, 1]`

Assuming we are using three of the same orange pixels as described above, we can hide each bit of our binary character in the final bit of each RGB value. This gives us the pixels:
- \[1110011<ins>0</ins>, 1010010<ins>1</ins>, 0000000<ins>0</ins>],
- \[1110011<ins>0</ins>, 1010010<ins>0</ins>, 0000000<ins>0</ins>],
- \[1110011<ins>0</ins>, 1010010<ins>1</ins>, ...

or in decimal:
- `[230, 165, 0], [230, 164, 0], [230, 165, 0]`

Notice how each pixel has barely changed from the original `[231, 165, 0]`, meaning that the image will have visually changed very little, and yet looking at the least significant bits of each number reveals our secret character `A`.

# How was it implemented here?
The LSB steganography here was implemented using a custom python script. This script should be made available with this writeup.
The Python Imaging Library (**PIL**) allows image manipulation and processing via a python script.
The script works by enumerating each pixel, and encoding the message over each plane (Red, Green, and Blue) as described above.

### Decoding
```
def lsbDecode(img):
	# img = image object
		
    b = list()

	# Get image dimensions (in pixels)
    width, height = img.size
		
	# Loop through each pixel
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y))) 
            # In the form [194, 190, 179]
						
			 Loop through each RGB value
            for (i, val) in enumerate(pixel):
                cval = list(f'{val:08b}') 
				# cval in the form: '00110000'
								
				# Get the last bit of value
                b.append(cval[7]) 
								
	# Combine every 8 bits into one byte, and store in a list
    byteList = [b[i:i+8] for i in range(0, len(b), 8)]
		
	# Convert each byte into its ASCII character
    charList = []
    for byte in byteList:
				
		# Converts from base 2 to decimal number
        asciiInt = int(''.join(byte), 2) 
				
        if asciiInt != 0:
			# Converts to character 
			# and appends to decoded message list
            char = chr(asciiInt) 
            charList.append(char)
						
	# Converts list to string to return
    return(''.join(charList))
```
