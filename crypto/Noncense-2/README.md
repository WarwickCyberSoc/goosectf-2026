# Noncense 2
- Category: **crypto**
- Difficulty: **hard**
- Previous challenge: **Noncense 1**
## Author
Battersea

## Overview
2nd of 2 challenges around AES-GCM nonce reuse. Requires the user to encrypt a message and forge an authentication token for it.


## Description
Well I guess if you solved challenge 1, it can't have been that secure. Oh well - you won't be able to encrypt your own messages and corresponding authentication tags right? If you really want to try it, encrypt the phrase 'password1' and provide the authenticatin tag for it. The program is the same as last time (you can use the same instance) but the provided file now includes the logic for challenge 2.

## Flag
<details>
    <summary>Flag</summary>

    GooseCTF{dont_reuse_nonces_in_your_ISS_coursework}
</details>
