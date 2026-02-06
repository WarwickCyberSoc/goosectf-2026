# Library
- Category: **pwn**
- Estimated Difficulty: **hard**

## Author
Sasha Shaw

## Description
You're trapped in a 9-5 j-o-b as an editor for the Warwick library. Can you clock out early?

## Topics
- Directory traversal
- /proc/self/mem
- Heap exploitation

## Hosting Instructions
Run the docker using `./build_docker.sh`.

## Hints

- The `/proc/self/` folder is quite interesting.
- Which files are both readable and writable in `/proc/self/`?

## Flag
<details>
    <summary>Flag</summary>

    GooseCTF{p4Th_Tr4v3rSaL_t0_3Sc4pE_tH3_L1bR4rY}
</details>
