# Python Module ciphersuite
import os
import sys
from pwn import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from binascii import hexlify, unhexlify

LOCAL = False

if LOCAL:
    pause()
else:
    p = remote("ctf-fsi.fe.up.pt", 4002)

FLAG_FILE = '/flags/flag.txt'

# Use crypto random generation to get a key with length n
def gen(): 
	rkey = bytearray(os.urandom(16))
	for i in range(16): rkey[i] = rkey[i] & 1
	return bytes(rkey)

# Bitwise XOR operation.
def enc(k, m):
	cipher = Cipher(algorithms.AES(k), modes.ECB())
	encryptor = cipher.encryptor()
	cph = b""
	for ch in m:
		cph += encryptor.update((ch*16).encode())
	cph += encryptor.finalize()
	return cph

# Reverse operation
def dec(k, c):
	assert len(c) % 16 == 0
	cipher = Cipher(algorithms.AES(k), modes.ECB())
	decryptor = cipher.decryptor()
	blocks = len(c)//16
	msg = b""
	for i in range(0,(blocks)):
		msg+=decryptor.update(c[i*16:(i+1)*16])
		msg=msg[:-15]
	msg += decryptor.finalize()
	return msg

# with open(FLAG_FILE, 'r') as fd:
# 	un_flag = fd.read()


c_shell = b"9f208341e00ea7bb1b19fbc7240fd445da2e68cecc877824679888b1872836209c4b0a015af346dfa46dca8f7fa72517fee59312ee688d5846da9f1c75c325e1f68aa253a12993f840dcb66762930cf3c96f13784536877bf98708d5fb2325557fcac0e67af63ceeb63ae8243f145465728144685ab4263ace17c691d7475af2c96f13784536877bf98708d5fb23255545316b5d2676ef4c14256f8bbfa98b58728144685ab4263ace17c691d7475af29f208341e00ea7bb1b19fbc7240fd44545316b5d2676ef4c14256f8bbfa98b58860ef0942ade59861a4aa838b37a50ba680e91ff79b09fe7994760e93e1e7281728144685ab4263ace17c691d7475af27fcac0e67af63ceeb63ae8243f145465728144685ab4263ace17c691d7475af245316b5d2676ef4c14256f8bbfa98b5845316b5d2676ef4c14256f8bbfa98b58728144685ab4263ace17c691d7475af281fcb2e7b16cab51802ae1f0707a6e429f208341e00ea7bb1b19fbc7240fd445b0b7e69172edf6124fb4d6e12f282265fc75eabaec16ed9ffb7ec0d2c3e195ee860ef0942ade59861a4aa838b37a50bafc75eabaec16ed9ffb7ec0d2c3e195ee728144685ab4263ace17c691d7475af248a0dae708aaa46e72ce74f37dc4c0d3fc75eabaec16ed9ffb7ec0d2c3e195ee686a3d8e108be6a805d15f90d2d59e1b7fcac0e67af63ceeb63ae8243f14546548a0dae708aaa46e72ce74f37dc4c0d39c4b0a015af346dfa46dca8f7fa7251745316b5d2676ef4c14256f8bbfa98b5845316b5d2676ef4c14256f8bbfa98b58686a3d8e108be6a805d15f90d2d59e1b7d463801142a469dee07a55f54bbf2a0ae1f03b85619528dde5a5883e653b940"

for i in range(2**16):
    print(i)
    k2 = gen()
    if (dec(k2, unhexlify(c_shell)).decode('latin-1')[0:4] == "flag"):
        print(dec(k2, unhexlify(c_shell)).decode('latin-1'))
        break
