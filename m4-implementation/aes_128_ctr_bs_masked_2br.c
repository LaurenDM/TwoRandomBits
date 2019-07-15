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
    srand(42);

    SCS_DEMCR |= SCS_DEMCR_TRCENA;
    DWT_CYCCNT = 0;
    DWT_CTRL |= DWT_CTRL_CYCCNTENA;
    RNG_CR |= RNG_CR_RNGEN;

    const uint32_t LEN = 256*16;
    const uint32_t LEN_ROUNDED = ((LEN+31)/32)*32;

    // NIST SP 800-38A F.5.1
    uint8_t key[16];
    uint8_t in[LEN];
    uint8_t out[LEN_ROUNDED];

    unsigned int i, j;
    char buffer[36];
    param p;

    for (i=0;i<10000;++i) {
        p.ctr = 0;
        for (j = 0; j < 12; ++j) {
            p.nonce[j] = rand();
        }
        for (j = 0; j < 16; ++j) {
            key[j] = rand();
        }
        for (j = 0; j < LEN; ++j) {
            in[j] = rand();
        }
        //memcpy(p.rk, key, 16);

        unsigned int oldcount = DWT_CYCCNT;
        AES_128_keyschedule(key, p.rk);
        unsigned int cyclecount = DWT_CYCCNT-oldcount;

/*
        // Print all round keys
        unsigned int j;
        for(i=0;i<2*11*4;++i) {
            sprintf(buffer, "rk[%2d]: ", i);
            for(j=0;j<4;++j)
                sprintf(buffer+2*j+8, "%02x", p.rk[i*4+j]);
            send_USART_str(buffer);
        }
*/

        sprintf(buffer, "cyc: %d", cyclecount);
        send_USART_str(buffer);

        oldcount = DWT_CYCCNT;
        AES_128_encrypt_ctr(&p, in, out, LEN);
        cyclecount = DWT_CYCCNT-oldcount;

        sprintf(buffer, "cyc: %d", cyclecount);
        send_USART_str(buffer);

/*
        // Print ciphertext
        sprintf(buffer, "out: ");
        send_USART_str(buffer);
        for(i=0;i<LEN;++i) {
            sprintf(buffer+((2*i)%32), "%02x", out[i]);
            if(i%16 == 15)
                send_USART_str(buffer);
        }
        if(LEN%16 > 0)
            send_USART_str(buffer);
*/

/*
        // Perform decryption
        p.ctr = 0;

        AES_128_decrypt_ctr(&p, out, in, LEN);

        // Print plaintext
        sprintf(buffer, "in: ");
        send_USART_str(buffer);
        for(i=0;i<LEN;++i) {
            sprintf(buffer+((2*i)%32), "%02x", in[i]);
            if(i%16 == 15)
                send_USART_str(buffer);
        }
        if(LEN%16 > 0)
            send_USART_str(buffer);
*/
    }

    while (1);

    return 0;
}
