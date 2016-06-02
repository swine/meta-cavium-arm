include recipes-core/images/core-image-minimal.bb


IMAGE_INSTALL += " \
	helloworld \
"

export IMAGE_BASENAME = "dai-image-hello"
