DESCRIPTION = "simple Hello World program"
PR = "r0"
LICENSE = "GPLv2"

S = "${WORKDIR}"

LIC_FILES_CHKSUM = "file://hello_world.c;md5=c37afcc3bdfe9a92615a5a4fb2bd7465"
SRC_URI = "file://hello_world.c"

do_compile() {
             ${CC} ${CFLAGS} ${LDFLAGS} -o hello_world hello_world.c -mabi=ilp32
}

do_install() {
             install -d ${D}${bindir}/
             install -m 0755 ${S}/hello_world ${D}${bindir}/
}

FILES_${PN} = "${bindir}/hello_world"
