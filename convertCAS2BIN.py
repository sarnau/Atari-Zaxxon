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

def parseCAS(thePath):
	print("Parsing %s" % (thePath))
	f = open(thePath, "rb") # notice the b for binary mode
	buffer = f.read()
	f.close()
#	print(dump(buffer))

	fileOffset = 0
	fileLength = len(buffer)
	file_index = 0
	baseaddr = None
	data = bytes()
	while fileOffset < fileLength:

		chunk_type = buffer[fileOffset:fileOffset+4].decode('ascii')
		chunk_length,param = struct.unpack_from("<HH", buffer[fileOffset+4:fileOffset+8], 0)
		chunk_data = buffer[fileOffset+8:fileOffset+8+chunk_length]
		#print(dump(chunk_data))
		if chunk_type == 'baud':
			#print('BAUD: %d baud' % param)
			pass
		elif chunk_type == 'data':
			print('DATA: LEN=$%04x PARAM=$%04x' % (chunk_length,param))
			#print(dump(chunk_data))
			csum = 0x00
			if chunk_length > 0:
				for i in range(0,chunk_length-1):
					csum += chunk_data[i]
					if csum >= 0x100:
						csum = (csum & 0xFF) + (csum >> 8)
			if len(chunk_data) >= 4 and chunk_data[0] == 0x55 and chunk_data[1] == 0x55:
				if chunk_data[2] == 0xFC or chunk_data[2] == 0xFD or chunk_data[2] == 0xFE or chunk_data[2] == 0xFA:
					if csum != chunk_data[-1]:
						print('CHECKSUM $%02x $%02x' % (csum,chunk_data[-1]))
					else:
						if chunk_data[2] == 0xFE:
							if len(data):
								ext = 'bin'
								if file_index == 0:
									ext = 'xex'
									f = open(thePath+'_%d.%s' % (file_index,ext), "wb") # notice the b for binary mode
								else:
									f = open(thePath+'_%d_%04x.%s' % (file_index,baseaddr,ext), "wb") # notice the b for binary mode
								if file_index == 3:
									data = data[:0xc0]
								f.write(data)
								f.close()
							file_index += 1
							data = bytes()
							baseaddr = None
							print('#' * 40)
						else:
							blockData = chunk_data[3:-1]
							if file_index == 1 or file_index == 2:
								#print(dump(blockData))
								dadr = (blockData[0] << 8) + blockData[1]
								if not baseaddr:
									baseaddr = dadr + 3
								print('BDATA: ADDR=$%04x DECRYPT=$%02x' % (dadr, blockData[2]))
								dblock = bytearray(0x80)
								for ii in range(0x7f,0x02,-1):
									dblock[ii] = (((blockData[ii] ^ 0xFF) - blockData[2]) & 0xFF) ^ 0xFF
								blocklen = 0x80
								if file_index == 1 or file_index == 2:
									blocklen = 0x5F
								blockData = dblock[3:3+blocklen]
							elif file_index == 3:
								baseaddr = 0x100
							print(dump(blockData))
							data += blockData
				else:
					print('RECORD $%02x $%s' % (chunk_data[2],dump(chunk_data)))
			else:
				print('MARKER $%s' % (dump(chunk_data)))
		elif chunk_type == 'FUJI' or chunk_type == 'fsk ':
			pass
		else:
			print('%s $%04x $%04x' % (chunk_type,chunk_length,param))
		fileOffset += 8 + chunk_length

parseCAS("Zaxxon Side A.cas")
