from pwn import *

r = remote("140.110.112.77", 9003)

def cal():
    f1 = r.recvline()
    f2 = r.recvline()

    print("Function 1: ", f1)
    print("Function 2: ", f2)

    a1 = int(f1[:f1.find(b'x')-3])
    b1 = int(f1[f1.find(b'+')+1:f1.find(b'y')-3])
    c1 = int(f1[f1.find(b'=')+1:])

    a2 = int(f2[:f2.find(b'x')-3])
    b2 = int(f2[f2.find(b'+')+1:f2.find(b'y')-3])
    c2 = int(f2[f2.find(b'=')+1:])

    delta = a1*b2-a2*b1

    if delta == 0:
        x = 0
        y = int(c1/b1)
    else:
        x = int((c1*b2-b1*c2)/delta)
        y = int((a1*c2-c1*a2)/delta)

    r.recvuntil('= ')
    r.sendline(str(x))
    r.recvuntil('= ')
    r.sendline(str(y))

for i in range(0, 100):
    cal()
    print('=========================',i,'=========================')

print(r.recvline().decode())