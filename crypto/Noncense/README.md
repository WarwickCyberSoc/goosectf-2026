# Noncense
- Category: **crypto**

## Author
Battersea

## Overview
2 challenges that involve nonce reuse with AES-GCM. (Challenge 2 should be locked until challenge 1 has been completed.) Challenge 1 is to decrypt messages. Challenge 2 is to encrypt a message and forge the authentication tag for it.

## Topics
- AES

## Hosting Instructions

For challenge 1, provide the user with [chal1.py](./user-files/chal1.py) from the [user-files](./user-files/) directory. For challenge 2, provide the user with [chal2.py](./user-files/chal2.py) from the [user-files](./user-files/) directory.

The [Dockerfile](./hosting-files/Dockerfile) along with files copied to the container are provided in the [hosting-files](./hosting-files/) directory. Host using the provided [Dockerfile](./hosting-files/Dockerfile). The process listens on port `1337` but any port can be used externally.

Challenge 2 is dependent on challenge 1. Therefore challenge 2 should not be unlocked until challenge 1 has been completed.

### File Structure
The provided files are structured as follows:

```
.
├── hosting-files
│   ├── Dockerfile
│   ├── flag1.txt
│   ├── flag2.txt
│   ├── key.txt
│   ├── nonce.txt
│   └── program.py
├── solution
│   ├── solve1.py
│   ├── solve2.py
│   └── writeup.md
├── user-files
│   ├── chal1.py
│   └── chal2.md
└── README.md
```

## Challenge 1

- Estimated Difficulty: **easy**

### Description

AES-GCM is really really super secure so I've used it to encrypt the flag. It's so secure that I'll even give you the source code (see the provided file).

You will need to connect to the specified instance for this challenge. To do this, you can run the following command:

nc IP_ADDRESS PORT_NUMBER

(You will need to be on the VPN.)

### Flag
<details>
    <summary>Flag</summary>

    GooseCTF{0nce_MeAns_oNce??}
</details>

## Challenge 2

- Estimated Difficulty: **hard**

### Description
Well I guess if you solved challenge 1, it can't have been that secure. Oh well - you won't be able to encrypt your own messages and corresponding authentication tags right? If you really want to try it, encrypt the phrase 'password1' and provide the authenticatin tag for it. The program is the same as last time (you can use the same instance) but the provided file now includes the logic for challenge 2.

### Flag
<details>
    <summary>Flag</summary>

    GooseCTF{dont_reuse_nonces_in_your_ISS_coursework}
</details>