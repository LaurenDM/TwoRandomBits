#include <stdint.h>
#include <stdio.h>
#include <assert.h>

static uint32_t ror(uint32_t a, size_t n)
{
    assert(n > 0 && n < 32);
    return (a >> n) | (uint32_t)(a << (32 - n));
}

static void check(uint32_t * masks, uint32_t z, uint32_t x, uint32_t y, uint32_t m)
{
    if (m) {
        if (masks[x] == m || !masks[x]) {
            printf("r%d = r%d ^ mask is not allowed\n", z, x);
            printf("r%d was masked with %08x, mask was %08x\n", x, masks[x], m);
        }
        masks[z] = masks[x] ^ m;
    }
    else {
        if (masks[x] == masks[y] || !masks[x] || !masks[y]) {
            printf("r%d = r%d ^ something with r%d is not allowed\n", z, x, y);
            printf("r%d was masked with %08x, r%d was masked with %08x\n", x, masks[x], y, masks[y]);
        }
        masks[z] = masks[x] ^ masks[y];
    }
}

static void mixcols(uint32_t * regs, uint32_t * masks, uint32_t mask1, uint32_t mask2, uint32_t mask12)
{
    uint32_t r0 = regs[0];
    uint32_t r1 = regs[1];
    uint32_t r2 = regs[2];
    uint32_t r3 = regs[3];
    uint32_t r4 = regs[4];
    uint32_t r5 = regs[5];
    uint32_t r6 = regs[6];
    uint32_t r7 = regs[7];
    uint32_t r8 = regs[8];
    uint32_t r9 = regs[9];
    uint32_t r10 = regs[10];
    uint32_t r11 = regs[11];
    uint32_t r12 = regs[12];
    uint32_t r14 = regs[14];
    uint32_t stacktmp;
    uint32_t stackmask;

    r5 = mask12;
    masks[5] = mask12;
    r11 = r0 ^ r5;
    check(masks, 11, 0, 5, 0);
    r11 = r0 ^ ror(r11, 8);
    check(masks, 11, 0, 11, 0);

    r6 = mask2;
    masks[6] = mask2;
    r10 = r2 ^ r6;
    check(masks, 10, 2, 6, 0);
    r10 = r2 ^ ror(r10, 8);
    check(masks, 10, 2, 10, 0);

    r7 = r9 ^ r6;
    check(masks, 7, 9, 6, 0);
    r7 = r9 ^ ror(r7, 8);
    check(masks, 7, 9, 7, 0);
    r9 = r9 ^ ror(r10, 24);
    check(masks, 9, 9, 10, 0);
    r9 = r9 ^ ror(r7, 8);
    check(masks, 9, 9, 7, 0);

    r8 = r3 ^ r5;
    check(masks, 8, 3, 5, 0);
    r8 = r3 ^ ror(r8, 8);
    check(masks, 8, 3, 8, 0);
    r3 = r3 ^ ror(r7, 24); //r7 now free, store t4 in r7
    check(masks, 3, 3, 7, 0);

    r7 = r12 ^ r5;
    check(masks, 7, 12, 5, 0);
    r7 = r12 ^ ror(r7, 8);
    check(masks, 7, 12, 7, 0);

    r6 = r4 ^ r5;
    check(masks, 6, 4, 5, 0);
    r6 = r4 ^ ror(r6, 8);
    check(masks, 6, 4, 6, 0);
    r4 = r4 ^ ror(r7, 24);
    check(masks, 4, 4, 7, 0);

    r5 = r14 ^ r5;
    check(masks, 5, 14, 5, 0);
    r5 = r14 ^ ror(r5, 8);
    check(masks, 5, 14, 5, 0);
    r14 = r14 ^ ror(r6, 24);
    check(masks, 14, 14, 6, 0);
    r6 = r4 ^ ror(r6, 8); //r4 now free, store t7 in r4
    check(masks, 6, 4, 6, 0);

    r4 = mask12;
    masks[4] = mask12;
    r4 = r1 ^ r4;
    check(masks, 4, 1, 4, 0);
    r4 = r1 ^ ror(r4, 8);
    check(masks, 4, 1, 4, 0);

    r0 = r0 ^ ror(r4, 24);
    check(masks, 0, 0, 4, 0);
    stacktmp = r0;
    stackmask = masks[0];
    r0 = mask2;
    masks[0] = mask2;
    r11 = r11 ^ r0;
    check(masks, 11, 11, 0, 0);
    r2 = r2 ^ ror(r11, 24);
    check(masks, 2, 2, 11, 0);
    r2 = r2 ^ ror(r4, 24);
    check(masks, 2, 2, 4, 0);
    r12 = r12 ^ ror(r8, 24);
    check(masks, 12, 12, 8, 0);
    r3 = r3 ^ r0;
    check(masks, 3, 3, 0, 0);
    r3 = r3 ^ ror(r4, 24);
    check(masks, 3, 3, 4, 0);
    r1 = r1 ^ ror(r5, 24);
    check(masks, 1, 1, 5, 0);
    r12 = r12 ^ ror(r4, 24);
    check(masks, 12, 12, 4, 0);

    r5 = r14 ^ ror(r5, 8);
    check(masks, 5, 14, 5, 0);
    r4 = r1 ^ ror(r4, 8);
    check(masks, 4, 1, 4, 0);
    r8 = r3 ^ ror(r8, 8);
    check(masks, 8, 3, 8, 0);
    r7 = r12 ^ ror(r7, 8);
    check(masks, 7, 12, 7, 0);
    r11 = r11 ^ r0;
    check(masks, 11, 11, 0, 0);
    r0 = stacktmp;
    masks[0] = stackmask;
    r11 = r0 ^ ror(r11, 8);
    check(masks, 11, 0, 11, 0);
    r10 = r2 ^ ror(r10, 8);
    check(masks, 10, 2, 10, 0);

    r12 = mask12;
    masks[12] = mask12;
    r7 = r7 ^ r12;
    check(masks, 7, 7, 12, 0);

    r4 = ror(r4, 8);
    r5 = ror(r5, 8);
    r6 = ror(r6, 8);
    r7 = ror(r7, 8);
    r8 = ror(r8, 8);
    r9 = ror(r9, 8);
    r10 = ror(r10, 8);
    r11 = ror(r11, 8);

    regs[0] = r0;
    regs[1] = r1;
    regs[2] = r2;
    regs[3] = r3;
    regs[4] = r4;
    regs[5] = r5;
    regs[6] = r6;
    regs[7] = r7;
    regs[8] = r8;
    regs[9] = r9;
    regs[10] = r10;
    regs[11] = r11;
    regs[12] = r12;
    regs[14] = r14;
}

int main(void)
{
    uint32_t regs[16] = {0};
    uint32_t masks[16] = {0};
    regs[0] = 0x1;  //to r11
    regs[2] = 0x2;
    regs[9] = 0x3;
    regs[3] = 0x4;
    regs[12] = 0x5;
    regs[4] = 0x6;
    regs[14] = 0x7;
    regs[1] = 0x8;  //to r4

    /*
    printf("start\n");
    for(int i = 0; i < 15; ++i)
        printf("r%d: %08lx\n", i, regs[i]);
    */

    uint32_t mask1 = 0xaaaaaaaa;
    uint32_t mask2 = 0xffffffff;
    uint32_t mask12 = mask1 ^ mask2;

    regs[1] ^= mask2;
    masks[1] = mask2;
    regs[14] ^= mask1;
    masks[14] = mask1;
    regs[4] ^= mask2;
    masks[4] = mask2;
    regs[12] ^= mask1;
    masks[12] = mask1;
    regs[3] ^= mask1;
    masks[3] = mask1;
    regs[9] ^= mask12;
    masks[9] = mask12;
    regs[2] ^= mask12;
    masks[2] = mask12;
    regs[0] ^= mask2;
    masks[0] = mask2;

    /*
    printf("after masking\n");
    for(int i = 0; i < 15; ++i)
        printf("r%d: %08lx\n", i, regs[i]);
    */

    mixcols(regs, masks, mask1, mask2, mask12);

    printf("after mixcolumns\n");
    for(int i = 0; i < 15; ++i)
        printf("r%2d: %08lx m: %08lx\n", i, regs[i], masks[i]);

    assert(masks[4] == mask2);
    regs[4] ^= mask2;
    assert(masks[5] == mask1);
    regs[5] ^= mask1;
    assert(masks[6] == mask2);
    regs[6] ^= mask2;
    assert(masks[7] == mask1);
    regs[7] ^= mask1;
    assert(masks[8] == mask1);
    regs[8] ^= mask1;
    assert(masks[9] == mask12);
    regs[9] ^= mask12;
    assert(masks[10] == mask12);
    regs[10] ^= mask12;
    assert(masks[11] == mask2);
    regs[11] ^= mask2;

    printf("after unmasking\n");
    for(int i = 4; i <= 11; ++i)
        printf("r%d: %08lx\n", i, regs[i]);

}


