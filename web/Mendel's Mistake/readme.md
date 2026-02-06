# Mendel's Mistake
- Category: Web
- Estimated Difficulty: hard

## Author
Peter Walker

## Overview
Prototype pollution challenge to gain "admin: true" on all user objects.

## Description
This is my prototype website - but for now its just a login page. But! it's super secure :)

## Topics
JavaScript <br>
Inheritance <br>
Unsanitised User Input

## Hints: please have these it needs one
- Where do developers often log debugging information?
    - Cost: 50
- Surely you didn't think '\_\_proto\_\_' would work? Try again.
    - Cost: 100

## Hosting Instructions

- Hosting files in `hosting_files`
- No files to user
- Create with `docker build . -t mendel`
    - Accessible on port 80 (default) with `docker run --rm -p 80:5000 mendel`

## Flag
<details>
<summary>THIS IS THE FLAG</summary>
GooseCTF{N0t_4_g00d_Pr0t0TYP3_wH0oP5}
</details>