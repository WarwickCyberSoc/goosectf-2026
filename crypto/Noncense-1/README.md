# Noncence 1
- Category: **crypto**
- Estimated Difficulty: **easy**

## Author
Battersea

## Overview
1st of 2 challenges around AES-GCM nonce reuse. Requires user to decrypt flag.

## Hosting Instructions
Both challenges should be hosted using the Docker image defined in `hosting-files`. Just use one instance for both.

Docker image listens on port 1337 internally.

## Description
AES-GCM is really really super secure so I've used it to encrypt the flag. It's so secure that I'll even give you the source code (see the provided file).

You will need to connect to the specified instance for this challenge. To do this, you can run the following command:

nc IP_ADDRESS PORT_NUMBER

(You will need to be on the VPN.)

## Flag
<details>
    <summary>Flag</summary>

    GooseCTF{0nce_MeAns_oNce??}
</details>
