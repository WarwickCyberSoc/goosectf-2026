# Mendel's Mistake
Mendel's work dealt heavily with genetics. Prototype pollution, by nature, deals with causing a child to **inherit** malicious properties from an abstract ancestor (ideally `Object.prototype`).


## Discovery

When you create an arbitrary user account, and login, your user details are logged to the developer console. That doesn't seem good!

![Screenshot](./assets/console.png)

Between the `Insufficient privileges for accessing the flag.` message and these account details, it should be clear you need to get `admin: true`.


## Vulnerability

None of the normal payloads (SQLi, SSTI, request forgery, etc.) work.
Hopefully - between these not working, and the subtle hints in the challenge name and description - or through help from another or an LLM, you can realise that this may be prototype pollution. [Reference](https://portswigger.net/web-security/prototype-pollution/server-side)

## Theory

Prototype objects are the abstract ancestors of all other objects in JavaScript. Every entity has one: a string, an object, everything. Ultimately, these all lead back to `Object.prototype`.

Now, JavaScript inherits properties from its respective prototype class - but not just the direct parent. It will traverse every ancestor gaining as many possible properties from them. 

If a malicious user can affect the state of any of these prototype objects, or even the final parent `Object.prototype`, the new properties will be inherited by all instantiated children.

So - if we can set `admin: true` on the prototype, all new user accounts should inherit that property.

## Payload

The initial register page using html form encoding, but modern websites often accept JSON in the same form...

Normal payloads for prototype pollution, using `__proto__`, don't work. This is due to basic filtering.

```
if (key === '__proto__') continue;
```

However, there is a quick and easy bypass for this primitive content filter. Instead of:

```
"__proto__": {
    "admin": true
}
```

It is possible to use:
```
"constructor": {
    "prototype": {
        "admin": true
    }
}
```

If you then register an account with the properties:
```
{
    "username": "solution",
    "password": "solution",
    "constructor": {
        "prototype": {
            "admin": true
        }
    }
}
```
Then that user account will have admin, and therefore has sufficient privileges to access the flag.

---

Peter Walker