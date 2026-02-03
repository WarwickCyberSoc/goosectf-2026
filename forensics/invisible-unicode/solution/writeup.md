# Invisible Unicode
## Step 1
First you must realise that the description of the challenge can be highlighted and copied. This shows that there are invisible unicode characters.

## Step 2
You must then realise that there are two unique invisble characters in this string, the [U+FFA0 Halfwidth Hangul Filler](https://www.compart.com/en/unicode/U+FFA0), and the [U+3164 Hangul Filler](https://www.compart.com/en/unicode/U+3164).

## Step 3
This can then be determined to represent a binary sequence where U+FFA0 represents 0, and U+3164 represents 1.

## Step 4
The binary can then be converted into ASCII, revealing the flag.

## Python Script
All of this can be done using the `decoder.py` script.

## Sources
- https://aem1k.com/invisible/encoder/
- https://aem1k.com/invisible/
- https://www.youtube.com/watch?v=0XumkGQFEEk