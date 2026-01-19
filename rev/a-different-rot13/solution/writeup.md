# A Different ROT13

## Disassembling

This is a usual reverse engineering challenge where you use a tool like Ghidra or Binary Ninja. Disassembling `main()` yields the following in Pseudo C:

![Dissasembled `main()`](./disas1.png)

So basically, the program reads the flag as a string and maps it into a different string with the function (`sub_4011e9`). The second argument is hard-coded to be `6`. Let's inspect this second function:

![Dissasembled `sub_401179()`](./disas2.png)

## Bitwise operations

The first argument is masked by `0x7f`, thus setting the first bit to 0 (this makes sense because we don't care about the sign bit when dealing with ASCII). Then, we have two integers being OR'd and then masked again. Let's call them `x` and `y`, and ignore the casting for a second.

```c
int x = rax_2 >> (7 - arg2)
int y = rax_2 << arg2
```

But we know that `arg2=6`, so

```c
int x = arg1 >> 1
int y = arg1 << 6
```

Then, these two parts are 'joined' via an OR operation.

So, the program is rotating the bits of each character. Following the theme of the challenge's name, the bits are rotated 13 times to the left. But since there are only eight bits in an ASCII character, and the sign bit is ignored, the actual number of rotations is $13-7=6$ times.

## Writing a Solution

It is really simple to reverse the bitwise operations. We just need to do the opposite:

```c
int x = arg1 << 1
int y = arg1 >> 6
```

See [solution.py](./solution.py) for a complete script.
