# A Different ROT13

- Category: **Rev**
- Estimated Difficulty: **Easy**

## Author

Vulcan

## Overview

A reverse engineering challenge involving bitwise operations.

## Description

Fun fact: In 1337 BC Julius Caesar invented binary numbers and bitwise operations. In fact, he is well known for using this wisdom to encrypt his military communications!

Source: me

## Topics

- C lang
- Bitwise operations
- Reverse Engineering

## Hosting Instructions

The [hosting-files](./hosting-files/) directory contains the files used by the container, along with the [dockerfile](./hosting-files/Dockerfile). `socat` listents internally on port `1337`.

### File Structure

The provided files are structured as follows:

```
.
│   README.md
├───creation-files
│       rot_13_or_smth_else.c
├───hosting-files
│       Dockerfile
│       flag.txt
│       rot_13_or_smth_else 
├───solution
│       disas1.png
│       disas2.png
│       solution.py
└───user-files
        flag.txt
        rot_13_or_not
```

## Flag

<details>
    <summary>Flag</summary>

    GooseCTF{C4354r_4PPr0V35_81N4rY}
</details>