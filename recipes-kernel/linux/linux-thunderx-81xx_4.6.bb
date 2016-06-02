inherit kernel

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"
LINUX_VERSION ?= "4.6"
PROVIDES += "virtual/kernel"
COMPATIBLE_MACHINE = "cavium-thunderx-81xx"
ARCH = "arm64"

SRCREV = "7866f54e4ad61305fedd08e49771424e2c786688"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-dev;branch=standard/base"
SRC_URI += "file://defconfig"
include ilp32_4_6_patches.inc
S = "${WORKDIR}/git"


addtask deploy after do_install
addtask shared_workdir after do_compile before do_install
FILES_kernel-image += "/boot/Image*"
KERNEL_EXTRA_ARGS += "LOADADDR=${UBOOT_ENTRYPOINT}"
LDFLAGS += "-lssl -lcrypto"
