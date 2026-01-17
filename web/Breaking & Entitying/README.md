# Breaking & Entitying
- Category: **web**
- Estimated Difficulty: **medium**

## Author
Battersea

## Overview
A challenge that involves bruteforcing a weak JWT signing key to manipulate the name field of the JWT and use it to perform XXE.

## Description

The flag is stored in `flag.txt` in root directory (i.e. `/flag.txt`). It seems the website has a handy feature to generate PDFs. If only you were an admin and could generate these PDFs and then make them include the flag.

If you need a wordlist at any point, use the provided wordlist.txt.

## Topics
- JWT (weak secrets)
- XXE

## Hosting Instructions

The [dockerfile](./hosting-files/dockerfile) along with files copied to the container are provided in the [hosting-files](./hosting-files/) directory. Host using the provided [dockerfile](./hosting-files/dockerfile). The website is accessible on port `5000` internally but any port can be used externally. SSH is possible on port `22`, this needs to remain on port `22` externally.

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

    GooseCTF{Silly_G0ose}
</details>