# backport to linux-4.8 the support for OcteonTx cn81xx/cn83xx and
# ThunderX cn88xx which is present in upstream linux-4.9 code...

inherit kernel

PROVIDES += "virtual/kernel"
COMPATIBLE_MACHINE = "cavium-octeontx-83xx|cavium-octeontx-cn81xx|cavium-thunderx-cn88xx|qemuarm64"
ARCH = "arm64"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"

# Skip processing of this recipe if it is not explicitly specified as the
# PREFERRED_PROVIDER for virtual/kernel. This avoids errors when trying
# to build multiple virtual/kernel providers
python () {
    if d.getVar("PREFERRED_PROVIDER_virtual/kernel", True) != "linux-octeontx-83xx":
        raise bb.parse.SkipPackage("Set PREFERRED_PROVIDER_virtual/kernel to linux-octeontx-83xx to enable it")
}

PV2 ?= "4.8"
PV3 ?= "${PV2}.28"
LINUX_VERSION = "${PV3}"
LINUX_VERSION_EXTENSION_append = "-cn83xx"
PV = "${LINUX_VERSION}"

KBRANCH = "standard/base"
SRCREV = "e3c2247579b1387ce62e040d215270d9c82971c8"
S = "${WORKDIR}/git"
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-${PV2}:${THISDIR}/${PN}-${PV2}/patches:"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-${PV2}.git;branch=${KBRANCH}"
SRC_URI += "file://defconfig"
include patches_4_8_cn8x.inc

addtask deploy after do_install
addtask shared_workdir after do_compile before do_install

do_populate_lic[depends] += "virtual/kernel:do_unpack"
#
do_patch[depends] += "virtual/kernel:do_unpack"

FILES_kernel-image += "/boot/Image*"
#KERNEL_EXTRA_ARGS += "LOADADDR=${UBOOT_ENTRYPOINT}"
