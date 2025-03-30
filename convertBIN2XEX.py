#!/usr/bin/python

import struct,os,sys

# Return an ASCII hex dump
def dump(src, length=16):
    result = []
    digits = 2
    for i in range(0, len(src), length):
       s = src[i:i+length]
       hexa = ' '.join(["%02X" % (x) for x in s])
       text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.'  for x in s])
       result.append("%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return '\n'.join(result)

startupFile = bytearray(open('Zaxxon Side A.cas_1_33ff.bin', "rb").read())
mainFile = open('Zaxxon Side A.cas_2_0600.bin', "rb").read()
stackFile = open('Zaxxon Side A.cas_3_0100.bin', "rb").read()

#print(dump(mainFile))
#print(dump(stackFile))

def writeChunk(baseaddr,mem):
	endAdr = baseaddr + len(mem) - 1
	f.write(bytearray([0xFF,0xFF,baseaddr & 0xFF,baseaddr >> 8,endAdr & 0xFF,endAdr >> 8]))
	f.write(mem)

startupFile[0x3438-0x33ff] = 0x60 # open cassette
startupFile[0x34AE-0x33ff] = 0x60 # load block 0x80
startupFile[0x34CF-0x33ff] = 0x60 # decrypt block
startupFile[0x341E-0x33ff] = 0xEA # load loop
startupFile[0x341F-0x33ff] = 0xEA # load loop
startupFile[0x348F-0x33ff] = 0x60 # load block 0xC0
startupFile[0x342E-0x33ff] = 0x67 # load file and copy data => jump directly into copy
#startupFile[0x3435-0x33ff] = 0x00 # BRK

f = open('Zaxxon.xex', "wb")
writeChunk(0x33ff, startupFile)
writeChunk(0x0600, mainFile)  # final adr: 0x0400
writeChunk(0x3AA0, stackFile) # final adr: 0x100

# launch the application after loading
STARTADR = 0x3400
RUNAD = 0x02E0
f.write(bytearray([0xFF,0xFF,RUNAD & 0xFF,RUNAD >> 8,(RUNAD + 1) & 0xFF,(RUNAD + 1) >> 8, STARTADR & 0xFF, STARTADR >> 8]))

f.close()
