SECTION = "bootloaders"
PROVIDES = "virtual/bootloader"
DEPENDS_append += "libgcc"
LICENSE = "GPL"

S = "${WORKDIR}/git"
PACKAGE_ARCH = "${MACHINE_ARCH}"
MKBFS = "${CAVIUM_UBOOT_SCRIPTS}/make-bootfs.py"
FATFS_TOOL = "${CAVIUM_UBOOT_SCRIPTS}/fatfs-tool"
BOOTFS_IMAGE = "${S}/${CAVIUM_BOARD_NAME}-firmware-uboot.img"
DEPLOY_BOOTFS_IMAGE = "${DEPLOYDIR}/${CAVIUM_BOARD_NAME}-firmware.img"
DTB_DIR = "${CAVIUM_UBOOT_SCRIPTS}"

inherit uboot-config deploy
##include board defines
include u-boot-${CAVIUM_BOARD_NAME}.inc

do_compile () {
	unset LDFLAGS
	unset CFLAGS
	unset CPPFLAGS

	make thunderx_81xx_config
	make CROSS_COMPILE="aarch64-thunderx-linux-gnu-" \
		CFLAGS="-mlittle-endian -I${S}/csr/include -mabi=lp64" u-boot-nodtb.bin
}

do_deploy () {
	${MKBFS} --uboot u-boot-nodtb.bin -f ${BOOTFS_IMAGE}
 	${FATFS_TOOL} -i ${BDK_IMAGE} cp ${DTB_DIR}/*.dtb /      
	${MKBFS} --bs ${BDK_IMAGE} --bl0  ${ATFBS_IMAGE} -f ${BOOTFS_IMAGE} 
	${MKBFS} --fip ${ATFFIP_IMAGE} --bl1 ${ATFBL1_IMAGE} -f ${BOOTFS_IMAGE}

        cp ${BOOTFS_IMAGE} ${DEPLOY_BOOTFS_IMAGE}
}

addtask deploy after do_compile
addtask fetch before do_compile
addtask deploy after do_compile
