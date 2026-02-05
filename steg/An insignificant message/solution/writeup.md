# Writeup
This image has an encoded flag using Least Significant Bit (LSB) steganography. 

### What is LSB steganography?
LSB is a technique used to hide data by replacing the smallest (least significant) bit of each number (usually a pixel in an image) with each bit of a secret message.

### How does it work?
A pixel's colour is encoded with 3 numerical values: Red, Green, and Blue (RGB). Each of these values range from 0 to 255.

Some image formats like PNG have a 4th pixel called Alpha, which represents transparency.

Here is an example of an orange pixel encoding (with Alpha, so RGBA):
- In decimal:`[231, 165, 0, 255]`
- In binary:`[11100111, 10100101, 00000000, 11111111]`

We can hide our message in the least significant bit (the last and lowest bit) of each pixel's RGB values.

To hide the letter `A`, we can encode it as its ASCII value in binary.
- In English: `A`
- In ASCII: 65
- In binary: `[0, 1, 0, 0, 0, 0, 0, 1]`

Assuming we are using three of the same orange pixels as described above, we can hide each bit of our binary character in the final bit of each RGBA value. This gives us the pixels:
- \[1110011<ins>0</ins>, 1010010<ins>1</ins>, 0000000<ins>0</ins>], 1111111<ins>0</ins>],
- \[1110011<ins>0</ins>, 1010010<ins>0</ins>, 0000000<ins>0</ins>], 1111111<ins>1</ins>],

or in decimal:
- `[230, 165, 0, 254], [230, 164, 0, 255]`

Notice how each pixel has barely changed from the original `[231, 165, 0, 255]`, meaning that the image will have visually changed very little, and yet looking at the least significant bits of each number reveals our secret character `A`.

# How to Solve This Challenge
This challenge encodes using LSB in the R, G, B and Alpha values for each pixel going top-to-bottom, left-to-right.

One way to spot this could be to look at each "bit plane" viually using a tool like [StegOnline](https://georgeom.net/StegOnline/upload).
If you look through the bit plane images you'll spot that Red 0, Green 0, Blue 0  and Alpha 0 all have suspicious values on the left hand
side of the image, going downwards.

If you then use the "extract files/data" tool, select those four bits, and select "columns" instead of "rows", for the default ordering,
you can extract the flag. You could also write a Python script like the one used to create this challenge to achieve the same thing.

# How was it implemented here?
The LSB steganography here was implemented using a custom python script. This script should be made available with this writeup.
The Python Imaging Library (**PIL**) allows image manipulation and processing via a python script.
The script works by enumerating each pixel, and encoding the message over each plane (Red, Green, Blue and Alpha) as described above.

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
