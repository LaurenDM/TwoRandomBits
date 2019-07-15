#include "common/stm32wrapper.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

typedef struct param {
    uint8_t nonce[12];
    uint32_t ctr;
    uint8_t rk[2*11*16];
} param;

extern void AES_128_keyschedule(const uint8_t *, uint8_t *);
extern void AES_128_encrypt_ctr(param const *, const uint8_t *, uint8_t *, uint32_t);
#define AES_128_decrypt_ctr AES_128_encrypt_ctr

int main(void)
{
    clock_setup();
    gpio_setup();
    usart_setup(115200);
    flash_setup();

    SCS_DEMCR |= SCS_DEMCR_TRCENA;
    DWT_CYCCNT = 0;
    DWT_CTRL |= DWT_CTRL_CYCCNTENA;
    RNG_CR |= RNG_CR_RNGEN;

    // NIST SP 800-38A F.5.1
    uint8_t key[16] = {0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c};
    uint8_t in[32] = {0};
    uint8_t out[32];
    unsigned int i, j;
    unsigned char buffer[40] = {0};
    param p;

    AES_128_keyschedule(key, p.rk);

    while (1) {
        recv_USART_bytes(buffer, 16);

        memcpy((void *)&p, (void *)buffer, 16);

        gpio_set(GPIOC, GPIO2);
        AES_128_encrypt_ctr(&p, in, out, 32);
        gpio_clear(GPIOC, GPIO2);

        send_USART_bytes(out, 32);
    }

    return 0;
}
