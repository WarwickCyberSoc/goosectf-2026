# Example
- Category: **misc**
- Estimated Difficulty: **easy**

## Author
Jane Doe

## Overview
An example challenge, designed to show how challenges being submitted to GooseCTF 2026 should be formatted.

## Description
If you can see this challenge, we've made a mistake. Please let one of the organisers know!

## Topics
- Challenge formatting
- Docker

## Hosting Instructions
This section should contain **detailed instructions** on hosting the challenge.

- Any files used for **hosting**, e.g. servers, Dockerfiles etc should go in `hosting-files/`

- Any files **which should be given to the user** should go in `user-files/`

- A **full writeup** and **working solution** should go in `solution/`

- (Optionally) you can put any files you used to create the challenge in `creation-or-misc-files/`

- E.g. "Host using Dockerfile in `hosting-files/`, listens internally on port 1337 but you can use any port externally.

### Example File Structure
Your challenge folder should look something like this:
```
.
├── creation-or-misc-files
│   └── create-hello.py
├── hosting-files
│   ├── Dockerfile
│   └── hello.py
├── README.md
├── solution
│   ├── solve.py
│   └── writeup.md
└── user-files
    └── hello.py
```
(These visualisations are sometimes quite useful, you can create them with `tree`)

## Flag
<details>
    <summary>Flag</summary>

    GooseCTF{MAKE_SURE_YOUR_FLAG_IS_HIDDEN_IN_THE_README}
</details>