SRC_URI = "git://github.com/mjaggi-cavium/u-boot-81xx.git"
LIC_FILES_CHKSUM = "file://README;md5=0a6bf9bc0593273e7e569690ee754fb3"

# This revision corresponds to the tag "v2015.01"
# We use the revision in order to avoid having to fetch it from the repo during parse
SRCREV = "af9c54c743a07b0a9c30b57e0b18661cb9e4a357"
PV = "v2016.03+"
SRC_URI[md5sum] = "b11900e678c40f49e77d4615197db55c"
SRC_URI[sha256sum] = "da70bf58d6724bbfd5a8c19ce0497e185f2bb4b9980b230b737a49403ae065a1"

BDK_IMAGE = "${CAVIUM_UBOOT_SCRIPTS}/thunder-release-v1.23-rc1.bin"
ATFBS_IMAGE= "${CAVIUM_UBOOT_SCRIPTS}/${CAVIUM_BOARD_NAME}-bootstrap.bin"
ATFBL1_IMAGE= "${CAVIUM_UBOOT_SCRIPTS}/${CAVIUM_BOARD_NAME}-bl1.bin"
ATFFIP_IMAGE= "${CAVIUM_UBOOT_SCRIPTS}/${CAVIUM_BOARD_NAME}-fip.bin"
