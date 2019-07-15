#include "common/stm32wrapper.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

extern void subbytes(uint32_t, uint32_t, uint32_t, uint8_t *);

int main(void)
{
    clock_setup();
    gpio_setup();
    usart_setup(115200);
    flash_setup();

    RNG_CR |= RNG_CR_RNGEN;

    uint32_t data[8] = {0};

    while (1) {
        recv_USART_bytes((uint8_t *)data, 32);

        //prepare masks
        uint32_t rand = rng_get_random_blocking();
        uint32_t mask1 = rand & 0x3;
        mask1 ^= mask1 << 16;
        mask1 ^= mask1 << 8;
        mask1 ^= mask1 << 4;
        mask1 ^= mask1 << 2;
        uint32_t mask2 = (rand & 0xc) >> 2;
        mask2 ^= mask2 << 16;
        mask2 ^= mask2 << 8;
        mask2 ^= mask2 << 4;
        mask2 ^= mask2 << 2;
        uint32_t mask3 = mask1 ^ mask2;

        //mask data
        data[0] ^= mask2;
        data[1] ^= mask1;
        data[2] ^= mask2;
        data[3] ^= mask1;
        data[4] ^= mask1;
        data[5] ^= mask3;
        data[6] ^= mask3;
        data[7] ^= mask2;

        //trigger, subbytes
        gpio_set(GPIOC, GPIO2);
        subbytes(mask1, mask2, mask3, (uint8_t *)data);
        gpio_clear(GPIOC, GPIO2);

        //unmask data
        data[0] ^= mask2;
        data[1] ^= mask1;
        data[2] ^= mask2;
        data[3] ^= mask1;
        data[4] ^= mask1;
        data[5] ^= mask3;
        data[6] ^= mask3;
        data[7] ^= mask2;

        send_USART_bytes((uint8_t *)data, 32);
    }

    return 0;
}
