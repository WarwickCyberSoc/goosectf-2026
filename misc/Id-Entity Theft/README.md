# Id-Entity Theft
- Category: **misc** (Linux priv esc)
- Estimated Difficulty: **medium**

## Author
Battersea

## Overview
This challenge follows on from [Breaking & Entitying](/web/Breaking%20&%20Entitying/). It involves using the same exploit to read `/etc/passwd`, bruteforcing a user's SSH password and then exploiting misconfigured `sudo` privileges to get a root shell.

## Description

This challenge follows on from Breaking & Entitying. There is a user on the server with a weak password. Exploit the vulnerability from the Breaking & Entitying challenge to identify what user this could be. Then, find their password and use it to gain access to the server. This user also has a misconfigured privilege. Find this and exploit it. The flag is stored in /root/root.txt.

If you need a wordlist at any point, use the provided wordlist.txt.

## Topics
- XXE
- SSH Bruteforce
- Sudo privileges

## Hosting Instructions

This challenge follows on from [Breaking & Entitying](/web/Breaking%20&%20Entitying/) and therefore should be hidden until that one has been completed.

The [dockerfile](./hosting-files/dockerfile) along with files copied to the container are provided in the [hosting-files](./hosting-files/) directory. Host using the provided [dockerfile](./hosting-files/dockerfile). The website is accessible on port `5000` internally but any port can be used externally. SSH is possible on port `22`, this needs to remain on port `22` externally.

The hosting files are the same for both challenges (the same instance can be used to sovle both).

Provide users with the [wordlist.txt](./user-files/wordlist.txt) from the [user-files](./user-files/) directory.

### File Structure
The provided files are structured as follows:

```
.
├── hosting-files/
│   ├── static/
│   │   ├── home.js
│   │   └── style.css
│   ├── templates/
│   │   ├── home.html
│   │   └── index.html
│   ├── dockerfile
│   ├── flag.txt
│   ├── pic.png
│   ├── root.txt
│   ├── server.py
│   └── supervisord.conf
├── solution/
│   ├── images/
│   └── writeup.md
├── user-files/
│   └── wordlist.txt
└── README.md
```

## Flag
<details>
    <summary>Flag</summary>

    GooseCTF{exit_vim_(bonus_challenge)}
</details>