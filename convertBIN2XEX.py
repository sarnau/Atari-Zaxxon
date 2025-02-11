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

mainFile = open('Zaxxon Side A.cas_2_0600.bin', "rb").read()
stackFile = open('Zaxxon Side A.cas_3_0100.bin', "rb").read()

#print(dump(mainFile))
#print(dump(stackFile))

def writeChunk(baseaddr,mem):
	endAdr = baseaddr + len(mem) - 1
	f.write(bytearray([0xFF,0xFF,baseaddr & 0xFF,baseaddr >> 8,endAdr & 0xFF,endAdr >> 8]))
	f.write(mem)
	
f = open('Zaxxon.xex', "wb")
writeChunk(0x0400, mainFile)
writeChunk(0x0100, stackFile)

# launch the application after loading
STARTADR = 0x0400
RUNAD = 0x02E0
f.write(bytearray([0xFF,0xFF,RUNAD & 0xFF,RUNAD >> 8,(RUNAD + 1) & 0xFF,(RUNAD + 1) >> 8, STARTADR & 0xFF, STARTADR >> 8]))

f.close()
