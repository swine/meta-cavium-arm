#! /usr/bin/python

import os
import sys
import binascii
import struct
import time
import argparse

# BDK image heade for Thunder is
#   Offset  Size    Description
#   0x00    4       Raw instruction for skipping header
#   0x04    4       Length of the image, includes header
#   0x08    8       Magic string "THUNDERX"
#   0x10    4       CRC32 of image + header. These bytes are zero when calculating the CRC
#   0x14    4       Zero, reserved for future use
#   0x18    64      ASCII Image name. Must always end in zero
#   0x58    32      ASCII Version. Must always end in zero
#   0x78    136     Zero, reserved for future use
#   0x100   -       Beginning of image. Header is always 256 bytes.
# UPDATE THIS FILE WHEN EVEN BDK HEADER FORMAT CHANGES.



#ATF image header for ThunderX is
#  offset       size    Description
#   0x00         4       lenght of the image
#   0x04         8       Reserved
#   0x0c         4       CRC32 image   
#   0x10         64      Image name
#   0x50         80    Reserved


BDK_HEADER_MAGIC = "THUNDERX"
BDK_HEADER_SIZE = 0x100

ATF_HEADER_SIZE = 0x100
ATF_BL0_OFFSET = 0x400000
ATF_BL1_OFFSET = 0x500000
ATF_BL2_OFFSET = 0x580000
ATF_BL32_OFFSET = 0x600000
ATF_LINUX_OFFSET = 0x800000
ATF_DTC_OFFSET = 0x700000
ATF_TBL_OFFSET = 0x480000


def load_file(filename):
    inf = open(filename, "rb")
    file = inf.read()
    inf.close()
    return file
  
def print_common_atf(data, offset):
    atflen = struct.unpack_from('<I',data, (offset + 0x0))
    if(atflen[0]):
        print ' Image Len:'+str(atflen[0])
        print ' Image Name: ' +data[(offset+0x10) : (offset +0x10 +64)]

def print_common_bdk(data, offset):
    bdklen = struct.unpack_from('<I',data, (offset + 0x4))
    if(bdklen[0]):
        print ' Image Len:'+str(bdklen[0])
        print ' Magic String: ' + data[offset+0x8:offset+0x10]
        print ' Image Name: ' +data[(offset+0x18) : (offset +0x18 +64)]
        print ' Version: ' + data[(offset + 0x58) : (offset + 0x58 + 32)]


def print_bdk_headers(bootfs_data):
    print '***********************************************'
    print ' BDK BOOT STUB(Non trusted)'
    print_common_bdk(bootfs_data,0x20000)
    print '***********************************************'
        
    print '***********************************************'
    print ' BDK BOOT STUB(Trusted)'
    print_common_bdk(bootfs_data,0x50000)
    print '***********************************************'

    print '***********************************************'
    print ' BDK Diagnostics'
    print_common_bdk(bootfs_data,0x80000)
    print '***********************************************'

    print '***********************************************'
    print ' ATF BOOT STUB'
    print_common_bdk(bootfs_data,0x400000)
    print '***********************************************'


def print_atf_headers(bootfs_data):
    print '***********************************************'
    print ' ATF BL1'
    print_common_atf(bootfs_data,0x480000)
    print '***********************************************'
    
    print '***********************************************'
    print ' ATF BL2'
    print_common_atf(bootfs_data,0x480000+(1*0x100))
    print '***********************************************'

    print '***********************************************'
    print 'BOOT LOADER'
    print_common_atf(bootfs_data,0x480000+(2*0x100))
    print '***********************************************'

    print '***********************************************'
    print ' LINUX'
    print_common_atf(bootfs_data,0x480000+(3*0x100))
    print '***********************************************'



def print_bootfs(filename):
    bootfs_data = load_file(filename)
    print_bdk_headers(bootfs_data)
    print_atf_headers(bootfs_data)


def pack(width, data):
    if width == 1:
        return struct.pack("<B", data)
    elif width == 2:
        return struct.pack("<H", data)
    elif width == 4:
        return struct.pack("<I", data)
    elif width == 8:
        return struct.pack("<Q", data)
    else:
        raise Exception("Invalid width")



def write_file(filename, data, offset):
    fhandle = open(filename, 'r+b')
    fhandle.seek(offset, 0)
    fhandle.write(data)
    fhandle.close()


def update_atf_header(filename,imagename, data, offset,tbl_idx):
    tbl_offset = ATF_TBL_OFFSET + (tbl_idx * 0x100)
    #build a atf header
    header = pack(4,len(data))
    header += pack(8,0)
    crc32 = 0xffffffffL & binascii.crc32(data)
    header += pack(4, crc32)
    name = imagename[0:63]
    header += name
    header += "\0" * (64 - len(name))
    header += "\0" * (ATF_HEADER_SIZE - len(header))
    fhandle = open(filename, 'r+b')
    fhandle.seek(tbl_offset, 0)
    fhandle.write(header)
    fhandle.close()
    write_file(filename, data, offset)


def update_bdk_header(filename, image_name, image_version, data, offset):
    # Save the 4 bytes at the front for the new header
    raw_instruction = data[0:4]
    # Remove the existing header
    data = data[BDK_HEADER_SIZE:]
    # Header begins with one raw instruction for 4 bytes
    header = raw_instruction
    # Total length
    header += pack(4, BDK_HEADER_SIZE + len(data))
    # Eight bytes of magic number
    header += BDK_HEADER_MAGIC
    # CRC - filled later
    header += pack(4, 0)
    # Reserved 4 bytes
    header += pack(4, 0)
    # 32 bytes of Name
    name = image_name[0:63] # Truncate to 63 bytes, room for \0
    header += name
    header += "\0" * (64 - len(name))
    # 16 bytes of Version
    v = image_version[0:31] # Truncate to 31 bytes, room for \0
    header += v
    header += "\0" * (32 - len(v))
    # Pad to header length
    header += "\0" * (BDK_HEADER_SIZE - len(header))
    # Make sure we're the right length
    assert(len(header) == BDK_HEADER_SIZE)

    # Combine the header and the data
    data = header + data
    # Fix the CRC
    crc32 = 0xffffffffL & binascii.crc32(data)
    data = data[0:16] + pack(4,crc32) + data[20:]
    write_file(filename, data, offset)


parser = argparse.ArgumentParser(description='argumnets for THUNDERX BOOTFS creationg.')
parser.add_argument( '--bs', '--bdk-image', help='bdk boot strap image') 
parser.add_argument('--bl0', '--aft-bs', help=' atf boot strap')
parser.add_argument('--bl1', '--atf-bl1', help='atf boot stage 1')
parser.add_argument('--fip', '--atf-fip', help='atf boot stage 2 and 3.1')
parser.add_argument('-u', '--uboot', help='use u-boot as a bootloader')
parser.add_argument('-e', '--uefi', help='use uefi as a bootloader')
parser.add_argument('-f', '--bootfs', required=True, help='file to be used for bootfs')
parser.add_argument('-l','--linux', help='include linux image also in the bootfs')
parser.add_argument('-d','--dtc', help='include linux device tree in the bootfs')
parser.add_argument('-p','--printfs', help='print headers included in a given ThundeX bootfs', action='store_true')
args = parser.parse_args()


if(args.uefi and args.uboot):
    print "Please supply only one bootloader(--uefi/--uboot)"
    exit()

if(args.printfs):
    print_bootfs(args.bootfs)
    exit()

if not os.path.isfile(args.bootfs):
    open(args.bootfs, "w").close()

if(args.bs):
    bs_data = load_file(args.bs)
    write_file(args.bootfs, bs_data, 0)

if(args.bl0):
    bl0_data = load_file(args.bl0)
    update_bdk_header(args.bootfs, 'ATF boot strap','1.0' ,bl0_data, ATF_BL0_OFFSET)

if(args.bl1):
    bl1_data = load_file(args.bl1)
    update_atf_header(args.bootfs, 'ATF stage 1',  bl1_data, ATF_BL1_OFFSET,0)

if(args.fip):
    bl2_data = load_file(args.fip)
    update_atf_header(args.bootfs, 'ATF stage 2',  bl2_data, ATF_BL2_OFFSET,1)

if(args.uboot):
    uboot_data = load_file(args.uboot)
    update_atf_header(args.bootfs, "U-BOOT",  uboot_data, ATF_BL32_OFFSET,2)

if(args.uefi):
    uefi_data = load_file(args.uefi)
    update_atf_header(args.bootfs, "UEFI", uefi_data, ATF_BL32_OFFSET,2)

if(args.linux):
    linux_data = load_file(args.linux)
    update_atf_header(args.bootfs, "LINUX", linux_data, ATF_LINUX_OFFSET,3)

if(args.dtc):
    dtc_data = load_file(args.dtc)
    update_atf_header(args.bootfs, "Device Tree", dtc_data, ATF_DTC_OFFSET,4)
	
