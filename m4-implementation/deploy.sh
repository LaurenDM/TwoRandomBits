#!/bin/sh

default=aes_128_ctr_bs_masked_2br.bin

if [ "$1" = "" ]; then
    echo No parameter given, trying to deploy "${default}"
    binary="${default}"
else
    binary="$1"
fi

if [ -f ${binary} ]; then
    st-flash write "${binary}" 0x8000000
else
    echo Nothing to deploy...
fi
