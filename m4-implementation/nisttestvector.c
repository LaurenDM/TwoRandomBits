#include "common/stm32wrapper.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>

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

    const uint32_t LEN = 4*16;
    const uint32_t LEN_ROUNDED = ((LEN+31)/32)*32;

    // NIST SP 800-38A F.5.1
    uint8_t nonce[12] = {0xf0,0xf1,0xf2,0xf3,0xf4,0xf5,0xf6,0xf7,0xf8,0xf9,0xfa,0xfb};
    uint8_t key[16] = {0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c};
    uint8_t in[4*16] = {0};/*0x6b,0xc1,0xbe,0xe2,0x2e,0x40,0x9f,0x96,0xe9,0x3d,0x7e,0x11,0x73,0x93,0x17,0x2a,
                        0xae,0x2d,0x8a,0x57,0x1e,0x03,0xac,0x9c,0x9e,0xb7,0x6f,0xac,0x45,0xaf,0x8e,0x51,
                        0x30,0xc8,0x1c,0x46,0xa3,0x5c,0xe4,0x11,0xe5,0xfb,0xc1,0x19,0x1a,0x0a,0x52,0xef,
                        0xf6,0x9f,0x24,0x45,0xdf,0x4f,0x9b,0x17,0xad,0x2b,0x41,0x7b,0xe6,0x6c,0x37,0x10};*/
    uint8_t out[LEN_ROUNDED];

    unsigned int i;

    char buffer[36];
    param p;
    p.ctr = 0xfffefdfc;
    memcpy(p.nonce, nonce, 12);

    unsigned int oldcount = DWT_CYCCNT;
    AES_128_keyschedule(key, p.rk);
    unsigned int cyclecount = DWT_CYCCNT-oldcount;


    // Print all round keys
/*
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


/*
    // Perform decryption
    p.ctr = 0xfffefdfc;

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

    while (1);

    return 0;
}
