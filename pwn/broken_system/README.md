# Broken System
- Category: **pwn**
- Estimated Difficulty: **medium**

## Author
Sasha Shaw

## Overview
An example challenge, designed to show how challenges being submitted to GooseCTF 2026 should be formatted.

## Description
Our system has been corrupted, can you regain control?
The flag file is at `flag.txt`.

## Topics
- Stack overflow
- Seccomp
- ROP

## Hosting Instructions
Run the docker using `./build_docker.sh`.

## Hints

- What does `load_seccomp` do?
- How can you read a file without a shell?

## Flag
<details>
    <summary>Flag</summary>

    GooseCTF{pwN1nG_3v3N_w1tH_A_bR0k3n_sYst3m}
</details>