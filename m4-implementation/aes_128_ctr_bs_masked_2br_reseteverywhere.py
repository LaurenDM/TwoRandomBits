#!/usr/bin/env python3

rounds = 10

rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

print(""".syntax unified
.thumb

.align 2
.type AES_Sbox,%object
AES_Sbox:
.word   0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5
.word   0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76
.word   0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0
.word   0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0
.word   0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc
.word   0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15
.word   0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a
.word   0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75
.word   0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0
.word   0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84
.word   0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b
.word   0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf
.word   0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85
.word   0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8
.word   0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5
.word   0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2
.word   0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17
.word   0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73
.word   0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88
.word   0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb
.word   0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c
.word   0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79
.word   0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9
.word   0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08
.word   0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6
.word   0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a
.word   0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e
.word   0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e
.word   0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94
.word   0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf
.word   0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68
.word   0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16

.align 2
@ void AES_128_keyschedule(const uint8_t *key,
@       uint8_t *rk) {
.global AES_128_keyschedule
.type   AES_128_keyschedule,%function
AES_128_keyschedule:

    //function prologue, preserve registers
    push {r0,r4-r12,r14}

    //first we are going to expand the full key and push it to the stack
    //then we do a reversed second pass, bitslice and store to rk
    //this ensures less context switching and less loads/stores of temporary variables

    //load key
    ldm r0, {r4-r7}

    //load S-box table address once
    adr r3, AES_Sbox
""")

for i in range(rounds):
    print("""    //round {:d}
    uxtb r8, r7, ror #8
    uxtb r9, r7, ror #16
    uxtb r10, r7, ror #24
    uxtb r11, r7

    ldr r8, [r3, r8, lsl #2]
    ldr r9, [r3, r9, lsl #2]
    ldr r10, [r3, r10, lsl #2]
    ldr r11, [r3, r11, lsl #2]

    eor r4, #0x{:02X} //rcon
    eor r4, r8
    eor r4, r4, r9, ror #24
    eor r4, r4, r10, ror #16
    eor r4, r4, r11, ror #8 //rk[{:d}]
    eor r5, r4 //rk[{:d}]
    eor r6, r5 //rk[{:d}]
    eor r7, r6 //rk[{:d}]""".format(i+1, rcon[i], (i+1)*4, (i+1)*4+1, (i+1)*4+2, (i+1)*4+3))

    if i < rounds-1:
        print("""    push.w {r4-r7}
""")
    else:
        print("""    //push {r4-r7} don't have to push in last round, keep in registers
""")

print("""    //done expanding, now start bitslicing

    //load bsconst table address once
    adr r14, AES_bsconst

    ldm r14, {r0,r2-r3}
    //r0 = 0x55555555 (but little-endian)
    //r2 = 0x33333333
    //r3 = 0x0f0f0f0f

    //set r1 to end of rk, to be filled backwards
    add r1, #352
""")

for i in range(rounds,-1,-1):
    print("""    //round {:d}""".format(i))

    if i < rounds and i > 0:
        print("""    pop.w {r4-r7}""")
    elif i < rounds:
        print("""    ldm r14, {r4-r7} //original key""")

    print("""    mov r8, r4
    mov r9, r5
    mov r10, r6
    mov r11, r7

    //bitslicekey
    //0x55555555
    eor r12, r8, r4, lsl #1
    and r12, r0
    eor r8, r12
    eor r4, r4, r12, lsr #1

    eor r12, r9, r5, lsl #1
    and r12, r0
    eor r9, r12
    eor r5, r5, r12, lsr #1

    eor r12, r10, r6, lsl #1
    and r12, r0
    eor r10, r12
    eor r6, r6, r12, lsr #1

    eor r12, r11, r7, lsl #1
    and r12, r0
    eor r11, r12
    eor r7, r7, r12, lsr #1
""")
    if i > 0:
        print("""    //0x33333333
    eor r12, r5, r4, lsl #2
    and r12, r2
    eor r5, r12
    eor r4, r4, r12, lsr #2

    eor r12, r7, r6, lsl #2
    and r12, r2
    eor r7, r12
    eor r6, r6, r12, lsr #2

    eor r12, r9, r8, lsl #2
    and r12, r2
    eor r9, r12
    eor r8, r8, r12, lsr #2

    eor r12, r11, r10, lsl #2
    and r12, r2
    eor r11, r12
    eor r10, r10, r12, lsr #2

    //0x0f0f0f0f
    eor r12, r6, r4, lsl #4
    and r12, r3
    eor r6, r12
    eor r4, r4, r12, lsr #4

    eor r12, r7, r5, lsl #4
    and r12, r3
    eor r7, r12
    eor r5, r5, r12, lsr #4

    eor r12, r10, r8, lsl #4
    and r12, r3
    eor r10, r12
    eor r8, r8, r12, lsr #4

    eor r12, r11, r9, lsl #4
    and r12, r3
    eor r11, r12
    eor r9, r9, r12, lsr #4

    //NOTs that are removed from SubBytes during encryption
    mvn r8, r8
    mvn r5, r5
    mvn r7, r7
    mvn r11, r11

    //stmdb r1!, {r4-r11} but in a different order
    //this could be fixed as we do during encryption, but then we destroy r0 and r2 and we would need to load the masks again
    str r11, [r1, #-4]
    str r7, [r1, #-8]
    str r10, [r1, #-12]
    str r6, [r1, #-16]
    str r9, [r1, #-20]
    str r5, [r1, #-24]
    str r8, [r1, #-28]""")
        if i == 1:
            print("""    pop {r14} //interleaving saves 1 cycle""")
        print("""    str r4, [r1, #-32]!
""")
    else:
        print("""    //0x33333333
    eor r12, r5, r4, lsl #2
    and r12, r2
    eor r0, r5, r12
    eor r4, r4, r12, lsr #2

    eor r12, r9, r8, lsl #2
    and r12, r2
    eor r9, r12
    eor r5, r8, r12, lsr #2

    eor r12, r7, r6, lsl #2
    and r12, r2
    eor r7, r12
    eor r8, r6, r12, lsr #2

    eor r12, r11, r10, lsl #2
    and r12, r2
    eor r11, r12
    eor r2, r10, r12, lsr #2

    //0x0f0f0f0f
    eor r12, r8, r4, lsl #4
    and r12, r3
    eor r8, r12
    eor r4, r4, r12, lsr #4

    eor r12, r7, r0, lsl #4
    and r12, r3
    eor r10, r7, r12
    eor r6, r0, r12, lsr #4

    eor r12, r11, r9, lsl #4
    and r12, r3
    eor r11, r12
    eor r7, r9, r12, lsr #4

    eor r12, r2, r5, lsl #4
    and r12, r3
    eor r9, r2, r12
    eor r5, r5, r12, lsr #4

    stmdb r1!, {r4-r11}
""")

print("""    //function epilogue, restore state
    pop {r4-r12,r14}
    bx lr

.align 2
.type AES_bsconst,%object
AES_bsconst:
.word 0xaaaaaaaa
.word 0xcccccccc
.word 0xf0f0f0f0

.align 2
@ void AES_128_encrypt_ctr(param const *p,
@       const uint8_t *in, uint8_t *out,
@       uint32_t len) {
.global AES_128_encrypt_ctr
.type   AES_128_encrypt_ctr,%function
AES_128_encrypt_ctr:

    //function prologue, preserve registers
    push {r0-r12,r14}

    adr r14, AES_bsconst
    sub.w sp, #172

    //STM32F407 specific!
    //RNG_CR = 0x50060800
    //RNG_SR = 0x50060804
    //RNG_DR = 0x50060808
    movw r12, 0x0804
    movt r12, 0x5006

.align 2
encrypt_blocks: //expect p in r0, RNG_SR in r12, AES_bsconst in r14

    //generate 1 random word
    mov r7, #1
    add r5, r12, #4 //RNG_DR
.align 2
generate_random:
    ldr r6, [r12]
    tst r6, r7
    beq generate_random //wait until RNG_SR == RNG_SR_DRDY
    mov r6, #0
    ldr.w r6, [r5]
    //extract 2 bits to use per block, change format, and store on stack
    //............................abcd to
    //cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd and
    //abababababababababababababababab
    //a and c are the masks for one block, b and d for the other
    mov r4, #0
    ubfx r4, r6, #0, #2
    orr r4, r4, r4, lsl #16
    orr r4, r4, r4, lsl #8
    orr r4, r4, r4, lsl #4
    orr r4, r4, r4, lsl #2
    mov r5, #0
    ubfx r5, r6, #2, #2
    orr r5, r5, r5, lsl #16
    orr r5, r5, r5, lsl #8
    orr r5, r5, r5, lsl #4
    orr r5, r5, r5, lsl #2
    eor r6, r4, r5
    str r4, [sp, #168] //MASK1
    str r5, [sp, #164] //MASK2
    str.w r6, [sp, #160] //MASK3 = MASK1 ^ MASK2

    //load from p two ctrnonce-blocks in r4-r7 and r8-r11
    ldmia.w r0!, {r4-r7} //increase r0 to point to p.rk for addroundkey
    mov r8, r4
    mov r9, r5
    mov r10, r6
    mov r11, r7

    //increase one ctr
    rev r11, r11
    add r11, #1 //won't overflow, only 2^32 blocks allowed
    rev r11, r11

    //transform state of two blocks into bitsliced form
    //general swapmoves moves {r4-r11} to {r4,8,5,9,6,10,7,11} so correct for this to have {r4-r11} again
    ldm r14, {r1-r3}
    //r1 = 0x55555555 (but little-endian)
    //r2 = 0x33333333
    //r3 = 0x0f0f0f0f

    //0x55555555
    eor r12, r8, r4, lsl #1
    and r12, r1
    eor r8, r12
    eor r4, r4, r12, lsr #1

    eor r12, r9, r5, lsl #1
    and r12, r1
    eor r9, r12
    eor r5, r5, r12, lsr #1

    eor r12, r10, r6, lsl #1
    and r12, r1
    eor r10, r12
    eor r6, r6, r12, lsr #1

    eor r12, r11, r7, lsl #1
    and r12, r1
    eor r11, r12
    eor r7, r7, r12, lsr #1

    //0x33333333
    eor r12, r5, r4, lsl #2
    and r12, r2
    eor r1, r5, r12
    eor r4, r4, r12, lsr #2

    eor r12, r9, r8, lsl #2
    and r12, r2
    eor r9, r12
    eor r5, r8, r12, lsr #2

    eor r12, r7, r6, lsl #2
    and r12, r2
    eor r7, r12
    eor r8, r6, r12, lsr #2

    eor r12, r11, r10, lsl #2
    and r12, r2
    eor r11, r12
    eor r2, r10, r12, lsr #2

    //0x0f0f0f0f
    eor r12, r8, r4, lsl #4
    and r12, r3
    eor r8, r12
    eor r4, r4, r12, lsr #4

    eor r12, r7, r1, lsl #4
    and r12, r3
    eor r10, r7, r12
    eor r6, r1, r12, lsr #4

    eor r12, r11, r9, lsl #4
    and r12, r3
    eor r11, r12
    eor r7, r9, r12, lsr #4

    eor r12, r2, r5, lsl #4
    and r12, r3
    eor r9, r2, r12
    eor r5, r5, r12, lsr #4

    //mask the input
    mov r12, #0
    mov r14, #0
    mov r3, #0
    ldr r12, [sp, #168] //MASK1
    ldr r14, [sp, #164] //MASK2
    ldr.w r3, [sp, #160]  //MASK3
    eor r4, r14
    eor r5, r12
    eor r6, r14
    eor r7, r12
    eor r8, r12
    eor r9, r3
    eor r10, r3
    eor r11, r14
""")

def printAddRoundKey(roundnr):
    print("    //AddRoundKey")
    if roundnr == 1:
        print("""    //mov r12, #0
    //mov r14, #0
    //mov r3, #0
    //ldr.w r0, [sp, #156] not necessary in round 1, p.rk already in r0
    //ldr r12, [sp, #168] //MASK1
    //ldr r14, [sp, #164] //MASK2
    //ldr.w r3, [sp, #160] //MASK3
""")
    elif roundnr == rounds:
        print("""    mov r12, #0
    mov r14, #0
    mov r3, #0
    ldr.w r0, [sp, #156] // p.rk
    ldr r12, [sp, #168] //MASK1
    ldr r14, [sp, #164] //MASK2
    ldr.w r3, [sp, #160] //MASK3
""")
    else:
        print("""    mov r12, #0
    mov r14, #0
    //mov r3, #0
    ldr.w r0, [sp, #156] // p.rk
    ldr r12, [sp, #168] //MASK1
    ldr r14, [sp, #164] //MASK2
    //ldr.w r3, [sp, #160] //MASK3 is already there from MixColumns
""")

    print("""    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r14         //mask k7
    mov r1, #0
    eor r1, r2, r12         //mk7
    mov r2, #0
    eor r2, r1, {:<11s} //mo7
    mov r4, #0
    eor r4, r2, r3          //o7

    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r12         //mask k6
    mov r1, #0
    eor r1, r2, r14         //mk6
    mov r2, #0
    eor r2, r1, {:<11s} //mo6
    mov r5, #0
    eor r5, r2, r3          //o6

    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r14
    mov r1, #0
    eor r1, r2, r12
    mov r2, #0
    eor r2, r1, {:<11s}
    mov r6, #0
    eor r6, r2, r3

    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r12
    mov r1, #0
    eor r1, r2, r14
    mov r2, #0
    eor r2, r1, {:<11s}
    mov r7, #0
    eor r7, r2, r3

    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r12
    mov r1, #0
    eor r1, r2, r14
    mov r2, #0
    eor r2, r1, {:<11s}
    mov r8, #0
    eor r8, r2, r3

    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r3
    mov r1, #0
    eor r1, r2, r12
    mov r2, #0
    eor r2, r1, {:<11s}
    mov r9, #0
    eor r9, r2, r14

    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r3
    mov r1, #0
    eor r1, r2, r12
    mov r2, #0
    eor r2, r1, {:<11s}
    mov r10, #0
    eor r10, r2, r14

    mov r1, #0
    ldr r1, [r0], #4
    mov r2, #0
    eor r2, r1, r14
    mov r1, #0
    eor r1, r2, r12
    mov r2, #0
    eor r2, r1, {:<11s}
    mov r11, #0
    eor r11, r2, r3
""".format( 'r4' if roundnr == 1 or roundnr == rounds else  'r4, ror #8',
            'r5' if roundnr == 1 or roundnr == rounds else  'r5, ror #8',
            'r6' if roundnr == 1 or roundnr == rounds else  'r6, ror #8',
            'r7' if roundnr == 1 or roundnr == rounds else  'r7, ror #8',
            'r8' if roundnr == 1 or roundnr == rounds else  'r8, ror #8',
            'r9' if roundnr == 1 or roundnr == rounds else  'r9, ror #8',
           'r10' if roundnr == 1 or roundnr == rounds else 'r10, ror #8',
           'r11' if roundnr == 1 or roundnr == rounds else 'r11, ror #8'))

    if roundnr < rounds:
        print("    str.w r0, [sp, #156] //must store, don't want to destroy original p.rk\n")

def printShiftRowsMixColumns():
    print("""    //ShiftRows
    //Meanwhile move to o0-o7 = r0,2,9,3,12,4,14,1 such that we're back in {r4-r11} after MixColumns
    //use r6 as tmp
    mov r12, #0
    mov r6, #0
    uxtb.w r12, r0
    ubfx r6, r0, #14, #2
    eor r12, r12, r6, lsl #8
    mov r6, #0
    ubfx r6, r0, #8, #6
    eor r12, r12, r6, lsl #10
    mov r6, #0
    ubfx r6, r0, #20, #4
    eor r12, r12, r6, lsl #16
    mov r6, #0
    ubfx r6, r0, #16, #4
    eor r12, r12, r6, lsl #20
    mov r6, #0
    ubfx r6, r0, #26, #6
    eor r12, r12, r6, lsl #24
    mov r6, #0
    ubfx r6, r0, #24, #2
    eor r12, r12, r6, lsl #30

    mov r4, #0
    mov r6, #0
    uxtb.w r4, r3
    ubfx r6, r3, #14, #2
    eor r4, r4, r6, lsl #8
    mov r6, #0
    ubfx r6, r3, #8, #6
    eor r4, r4, r6, lsl #10
    mov r6, #0
    ubfx r6, r3, #20, #4
    eor r4, r4, r6, lsl #16
    mov r6, #0
    ubfx r6, r3, #16, #4
    eor r4, r4, r6, lsl #20
    mov r6, #0
    ubfx r6, r3, #26, #6
    eor r4, r4, r6, lsl #24
    mov r6, #0
    ubfx r6, r3, #24, #2
    eor r4, r4, r6, lsl #30

    mov r14, #0
    mov r6, #0
    uxtb.w r14, r9
    ubfx r6, r9, #14, #2
    eor r14, r14, r6, lsl #8
    mov r6, #0
    ubfx r6, r9, #8, #6
    eor r14, r14, r6, lsl #10
    mov r6, #0
    ubfx r6, r9, #20, #4
    eor r14, r14, r6, lsl #16
    mov r6, #0
    ubfx r6, r9, #16, #4
    eor r14, r14, r6, lsl #20
    mov r6, #0
    ubfx r6, r9, #26, #6
    eor r14, r14, r6, lsl #24
    mov r6, #0
    ubfx r6, r9, #24, #2
    eor r14, r14, r6, lsl #30

    mov r0, #0
    mov r6, #0
    uxtb.w r0, r5
    ubfx r6, r5, #14, #2
    eor r0, r0, r6, lsl #8
    mov r6, #0
    ubfx r6, r5, #8, #6
    eor r0, r0, r6, lsl #10
    mov r6, #0
    ubfx r6, r5, #20, #4
    eor r0, r0, r6, lsl #16
    mov r6, #0
    ubfx r6, r5, #16, #4
    eor r0, r0, r6, lsl #20
    mov r6, #0
    ubfx r6, r5, #26, #6
    eor r0, r0, r6, lsl #24
    mov r6, #0
    ubfx r6, r5, #24, #2
    eor r0, r0, r6, lsl #30

    mov r9, #0
    mov r6, #0
    uxtb.w r9, r8
    ubfx r6, r8, #14, #2
    eor r9, r9, r6, lsl #8
    mov r6, #0
    ubfx r6, r8, #8, #6
    eor r9, r9, r6, lsl #10
    mov r6, #0
    ubfx r6, r8, #20, #4
    eor r9, r9, r6, lsl #16
    mov r6, #0
    ubfx r6, r8, #16, #4
    eor r9, r9, r6, lsl #20
    mov r6, #0
    ubfx r6, r8, #26, #6
    eor r9, r9, r6, lsl #24
    mov r6, #0
    ubfx r6, r8, #24, #2
    eor r9, r9, r6, lsl #30

    mov r3, #0
    mov r6, #0
    uxtb.w r3, r7
    ubfx r6, r7, #14, #2
    eor r3, r3, r6, lsl #8
    mov r6, #0
    ubfx r6, r7, #8, #6
    eor r3, r3, r6, lsl #10
    mov r6, #0
    ubfx r6, r7, #20, #4
    eor r3, r3, r6, lsl #16
    mov r6, #0
    ubfx r6, r7, #16, #4
    eor r3, r3, r6, lsl #20
    mov r6, #0
    ubfx r6, r7, #26, #6
    eor r3, r3, r6, lsl #24
    mov r6, #0
    ubfx r6, r7, #24, #2
    eor r3, r3, r6, lsl #30

    mov r10, #0
    mov r6, #0
    uxtb.w r10, r2
    ubfx r6, r2, #14, #2
    eor r10, r10, r6, lsl #8
    mov r6, #0
    ubfx r6, r2, #8, #6
    eor r10, r10, r6, lsl #10
    mov r6, #0
    ubfx r6, r2, #20, #4
    eor r10, r10, r6, lsl #16
    mov r6, #0
    ubfx r6, r2, #16, #4
    eor r10, r10, r6, lsl #20
    mov r6, #0
    ubfx r6, r2, #26, #6
    eor r10, r10, r6, lsl #24
    mov r6, #0
    ubfx r6, r2, #24, #2
    mov r2, #0
    eor r2, r10, r6, lsl #30

    mov r10, #0
    mov r6, #0
    uxtb.w r10, r1
    ubfx r6, r1, #14, #2
    eor r10, r10, r6, lsl #8
    mov r6, #0
    ubfx r6, r1, #8, #6
    eor r10, r10, r6, lsl #10
    mov r6, #0
    ubfx r6, r1, #20, #4
    eor r10, r10, r6, lsl #16
    mov r6, #0
    ubfx r6, r1, #16, #4
    eor r10, r10, r6, lsl #20
    mov r6, #0
    ubfx r6, r1, #26, #6
    eor r10, r10, r6, lsl #24
    mov r6, #0
    ubfx r6, r1, #24, #2
    mov r1, #0
    eor r1, r10, r6, lsl #30

    //MixColumns
    //based on Käsper-Schwabe, squeezed in 14 registers
    //x0-x7 = r0,2,9,3,12,4,14,1, t0-t7 = r11,10,(9),8,7,6,5,(4)
    mov r5, #0
    mov r6, #0
    ldr r5, [sp, #160] //MASK3
    ldr r6, [sp, #164] //MASK2
    mov r11, #0
    eor r11, r0, r5
    eor r11, r0, r11, ror #8

    mov r10, #0
    eor r10, r2, r6
    eor r10, r2, r10, ror #8

    mov r7, #0
    eor r7, r9, r6
    eor r7, r9, r7, ror #8
    eor r9, r9, r10, ror #24
    eor r9, r9, r7, ror #8

    mov r8, #0
    eor r8, r3, r5
    eor r8, r3, r8, ror #8
    eor r3, r3, r7, ror #24 //r7 now free, store t4 in r7

    mov r7, #0
    eor r7, r12, r5
    eor r7, r12, r7, ror #8

    mov r6, #0
    eor r6, r4, r5
    eor r6, r4, r6, ror #8
    eor r4, r4, r7, ror #24
    str   sp, [sp, #152]
    str.w r7, [sp, #152]

    eor r5, r14, r5
    eor r5, r14, r5, ror #8
    eor r14, r14, r6, ror #24
    eor r6, r4, r6, ror #8 //r4 now free, store t7 in r4

    mov r4, #0
    mov r7, #0
    ldr r4, [sp, #160] //MASK3
    ldr r7, [sp, #164] //MASK2
    eor r4, r1, r4
    eor r4, r1, r4, ror #8

    eor r0, r0, r4, ror #24
    eor r11, r11, r7
    eor r2, r2, r11, ror #24
    eor r2, r2, r4, ror #24
    eor r12, r12, r8, ror #24
    eor r3, r3, r7
    eor r3, r3, r4, ror #24
    eor r1, r1, r5, ror #24
    eor r12, r12, r4, ror #24

    eor r5, r14, r5, ror #8
    eor r4, r1, r4, ror #8
    eor r8, r3, r8, ror #8
    eor r11, r11, r7
    mov r7, #0
    mov r3, #0
    ldr r7, [sp, #152]
    ldr r3, [sp, #160] //MASK3
    eor r7, r12, r7, ror #8
    eor r11, r0, r11, ror #8
    eor r10, r2, r10, ror #8

    eor r7, r7, r3
""")

def printSubBytes():
    print("""    //SubBytes
    //Result of combining a masked version of http://www.cs.yale.edu/homes/peralta/CircuitStuff/AES_SBox.txt with my custom instruction scheduler / register allocator
    //Note that the 4 last NOTs are moved to the key schedule
    //Result: 95 loads and 66 stores
    mov    r0, #0         //RESET
    eor    r0, r12, r14   //Exec MASK3 = MASK1 ^ MASK2 into r0
    mov    r1, #0         //RESET
    and    r1, r12, r14   //Exec MASK1AND2 = MASK1 & MASK2 into r1
    mov    r2, #0         //RESET
    and    r2, r12,  r0   //Exec MASK1AND3 = MASK1 & MASK3 into r2
    mov    r3, #0         //RESET
    and    r3, r14,  r0   //Exec MASK2AND3 = MASK2 & MASK3 into r3
    str    sp, [sp, #152] //RESET
    str.w r11, [sp, #152] //Store r11/i0 on stack
    mov   r11, #0         //RESET
    eor   r11,  r1, r12   //Exec MASK1AND2XOR1 = MASK1AND2 ^ MASK1 into r11
    str    sp, [sp, #148] //RESET
    str.w r11, [sp, #148] //Store r11/MASK1AND2XOR1 on stack
    mov   r11, #0         //RESET
    eor   r11,  r1, r14   //Exec MASK1AND2XOR2 = MASK1AND2 ^ MASK2 into r11
    mov    r1, #0         //RESET
    eor    r1,  r2, r12   //Exec MASK1AND3XOR1 = MASK1AND3 ^ MASK1 into r1
    str    sp, [sp, #144] //RESET
    str.w r11, [sp, #144] //Store r11/MASK1AND2XOR2 on stack
    mov   r11, #0         //RESET
    eor   r11,  r2,  r0   //Exec MASK1AND3XOR3 = MASK1AND3 ^ MASK3 into r11
    mov    r2, #0         //RESET
    eor    r2,  r3, r14   //Exec MASK2AND3XOR2 = MASK2AND3 ^ MASK2 into r2
    str    sp, [sp, #140] //RESET
    str.w  r1, [sp, #140] //Store r1/MASK1AND3XOR1 on stack
    mov    r1, #0         //RESET
    eor    r1,  r3,  r0   //Exec MASK2AND3XOR3 = MASK2AND3 ^ MASK3 into r1
    mov    r3, #0         //RESET
    eor    r3,  r4,  r7   //Exec T1_0 = i7 ^ i4 into r3
    str    sp, [sp, #136] //RESET
    str.w  r1, [sp, #136] //Store r1/MASK2AND3XOR3 on stack
    mov    r1, #0         //RESET
    eor    r1,  r4,  r9   //Exec T2_0 = i7 ^ i2 into r1
    str    sp, [sp, #132] //RESET
    str.w  r2, [sp, #132] //Store r2/MASK2AND3XOR2 on stack
    mov    r2, #0         //RESET
    eor    r2,  r4, r10   //Exec T3_0 = i7 ^ i1 into r2
    mov    r4, #0         //RESET
    eor    r4,  r7,  r9   //Exec T4_0 = i4 ^ i2 into r4
    str    sp, [sp, #128] //RESET
    str.w r11, [sp, #128] //Store r11/MASK1AND3XOR3 on stack
    mov   r11, #0         //RESET
    eor   r11,  r8, r10   //Exec T5_0 = i3 ^ i1 into r11
    mov    r8, #0         //RESET
    eor    r8,  r3, r11   //Exec T6_0 = T1_0 ^ T5_0 into r8
    mov    r0, #0         //RESET
    eor    r0,  r5,  r6   //Exec T7_0 = i6 ^ i5 into r0
    str    sp, [sp, #124] //RESET
    str.w  r1, [sp, #124] //Store r1/T2_0 on stack
    mov    r1, #0         //RESET
    ldr.w  r1, [sp, #152] //Load i0 into r1
    str    sp, [sp, #120] //RESET
    str.w r10, [sp, #120] //Store r10/i1 on stack
    mov   r10, #0         //RESET
    eor   r10,  r1,  r8   //Exec T8_0 = i0 ^ T6_0 into r10
    str    sp, [sp, #116] //RESET
    str.w  r3, [sp, #116] //Store r3/T1_0 on stack
    mov    r3, #0         //RESET
    eor    r3, r10, r12   //Exec ht8_0 = T8_0 ^ MASK1 into r3
    str    sp, [sp, #112] //RESET
    str.w r10, [sp, #112] //Store r10/T8_0 on stack
    mov   r10, #0         //RESET
    eor   r10,  r1,  r0   //Exec T9_0 = i0 ^ T7_0 into r10
    str    sp, [sp, #108] //RESET
    str.w  r3, [sp, #108] //Store r3/ht8_0 on stack
    mov    r3, #0         //RESET
    eor    r3, r10, r14   //Exec ht9_0 = T9_0 ^ MASK2 into r3
    str    sp, [sp, #104] //RESET
    str.w  r3, [sp, #104] //Store r3/ht9_0 on stack
    mov    r3, #0         //RESET
    eor    r3,  r8,  r0   //Exec T10_0 = T6_0 ^ T7_0 into r3
    str    sp, [sp, #100] //RESET
    str.w  r3, [sp, #100] //Store r3/T10_0 on stack
    mov    r3, #0         //RESET
    eor    r3,  r5,  r9   //Exec T11_0 = i6 ^ i2 into r3
    mov    r5, #0         //RESET
    eor    r5,  r3, r12   //Exec ht11_0 = T11_0 ^ MASK1 into r5
    mov   r14, #0         //RESET
    eor   r14,  r6,  r9   //Exec T12_0 = i5 ^ i2 into r14
    mov    r6, #0         //RESET
    eor    r6,  r2,  r4   //Exec T13_0 = T3_0 ^ T4_0 into r6
    mov    r9, #0         //RESET
    eor    r9,  r6, r12   //Exec ht13_0 = T13_0 ^ MASK1 into r9
    str    sp, [sp, #96 ] //RESET
    str.w  r9, [sp, #96 ] //Store r9/ht13_0 on stack
    mov    r9, #0         //RESET
    eor    r9,  r8,  r3   //Exec T14_0 = T6_0 ^ T11_0 into r9
    mov    r3, #0         //RESET
    eor    r3, r11,  r5   //Exec T15_0 = T5_0 ^ ht11_0 into r3
    mov    r5, #0         //RESET
    eor    r5, r11, r14   //Exec T16_0 = T5_0 ^ T12_0 into r5
    mov   r11, #0         //RESET
    eor   r11, r10,  r5   //Exec T17_0 = T9_0 ^ T16_0 into r11
    str    sp, [sp, #92 ] //RESET
    str.w  r4, [sp, #92 ] //Store r4/T4_0 on stack
    mov    r4, #0         //RESET
    eor    r4, r11, r12   //Exec ht17_0 = T17_0 ^ MASK1 into r4
    str    sp, [sp, #88 ] //RESET
    str.w r11, [sp, #88 ] //Store r11/T17_0 on stack
    mov   r11, #0         //RESET
    eor   r11,  r7,  r1   //Exec T18_0 = i4 ^ i0 into r11
    mov    r7, #0         //RESET
    eor    r7, r11, r12   //Exec ht18_0 = T18_0 ^ MASK1 into r7
    mov   r11, #0         //RESET
    eor   r11,  r0,  r7   //Exec T19_0 = T7_0 ^ ht18_0 into r11
    mov    r7, #0         //RESET
    ldr.w  r7, [sp, #164] //Load MASK2 into r7
    str    sp, [sp, #84 ] //RESET
    str.w  r3, [sp, #84 ] //Store r3/T15_0 on stack
    mov    r3, #0         //RESET
    eor    r3, r11,  r7   //Exec ht19_0 = T19_0 ^ MASK2 into r3
    str    sp, [sp, #80 ] //RESET
    str.w  r3, [sp, #80 ] //Store r3/ht19_0 on stack
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #116] //Load T1_0 into r3
    str    sp, [sp, #76 ] //RESET
    str.w r10, [sp, #76 ] //Store r10/T9_0 on stack
    mov   r10, #0         //RESET
    eor   r10,  r3, r11   //Exec T20_0 = T1_0 ^ T19_0 into r10
    str    sp, [sp, #72 ] //RESET
    str.w r11, [sp, #72 ] //Store r11/T19_0 on stack
    mov   r11, #0         //RESET
    ldr.w r11, [sp, #120] //Load i1 into r11
    str    sp, [sp, #68 ] //RESET
    str.w  r9, [sp, #68 ] //Store r9/T14_0 on stack
    mov    r9, #0         //RESET
    eor    r9, r11,  r1   //Exec T21_0 = i1 ^ i0 into r9
    mov   r11, #0         //RESET
    eor   r11,  r0,  r9   //Exec T22_0 = T7_0 ^ T21_0 into r11
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #124] //Load T2_0 into r0
    mov    r9, #0         //RESET
    eor    r9,  r0, r11   //Exec T23_0 = T2_0 ^ T22_0 into r9
    str    sp, [sp, #120] //RESET
    str.w r11, [sp, #120] //Store r11/T22_0 on stack
    mov   r11, #0         //RESET
    ldr.w r11, [sp, #100] //Load T10_0 into r11
    mov    r1, #0         //RESET
    eor    r1,  r0, r11   //Exec T24_0 = T2_0 ^ T10_0 into r1
    mov    r0, #0         //RESET
    eor    r0,  r1, r12   //Exec ht24_0 = T24_0 ^ MASK1 into r0
    mov    r1, #0         //RESET
    eor    r1, r10,  r4   //Exec T25_0 = T20_0 ^ ht17_0 into r1
    str    sp, [sp, #64 ] //RESET
    str.w  r1, [sp, #64 ] //Store r1/T25_0 on stack
    mov    r1, #0         //RESET
    eor    r1,  r2,  r5   //Exec T26_0 = T3_0 ^ T16_0 into r1
    str    sp, [sp, #60 ] //RESET
    str.w  r0, [sp, #60 ] //Store r0/ht24_0 on stack
    mov    r0, #0         //RESET
    eor    r0,  r3, r14   //Exec T27_0 = T1_0 ^ T12_0 into r0
    mov   r14, #0         //RESET
    eor   r14,  r0, r12   //Exec ht27_0 = T27_0 ^ MASK1 into r14
    str    sp, [sp, #56 ] //RESET
    str.w  r0, [sp, #56 ] //Store r0/T27_0 on stack
    mov    r0, #0         //RESET
    and    r0,  r8,  r6   //Exec XM1_00 = T6_0 & T13_0 into r0
    mov   r11, #0         //RESET
    ldr.w r11, [sp, #160] //Load MASK3 into r11
    //Wait, I could have recomputed that!
    str    sp, [sp, #52 ] //RESET
    str.w r14, [sp, #52 ] //Store r14/ht27_0 on stack
    mov   r14, #0         //RESET
    and   r14,  r8, r11   //Exec XM1_01 = T6_0 & MASK3 into r14
    str    sp, [sp, #48 ] //RESET
    str.w  r8, [sp, #48 ] //Store r8/T6_0 on stack
    mov    r8, #0         //RESET
    eor    r8, r14, r11   //Exec XM1_02 = XM1_01 ^ MASK3 into r8
    mov   r14, #0         //RESET
    eor   r14,  r0,  r8   //Exec XM1_03 = XM1_00 ^ XM1_02 into r14
    mov    r0, #0         //RESET
    and    r0, r12,  r6   //Exec XM1_04 = MASK1 & T13_0 into r0
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #128] //Load MASK1AND3XOR3 into r6
    mov    r8, #0         //RESET
    eor    r8,  r0,  r6   //Exec XM1_05 = XM1_04 ^ MASK1AND3XOR3 into r8
    mov    r0, #0         //RESET
    eor    r0,  r8, r12   //Exec XM1_06 = XM1_05 ^ MASK1 into r0
    mov    r8, #0         //RESET
    eor    r8, r14,  r0   //Exec M1_0 = XM1_03 ^ XM1_06 into r8
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #108] //Load ht8_0 into r0
    mov   r14, #0         //RESET
    and   r14,  r9,  r0   //Exec XM2_00 = T23_0 & ht8_0 into r14
    mov    r6, #0         //RESET
    and    r6,  r9,  r7   //Exec XM2_01 = T23_0 & MASK2 into r6
    str    sp, [sp, #44 ] //RESET
    str.w  r9, [sp, #44 ] //Store r9/T23_0 on stack
    mov    r9, #0         //RESET
    eor    r9,  r6,  r7   //Exec XM2_02 = XM2_01 ^ MASK2 into r9
    mov    r6, #0         //RESET
    eor    r6, r14,  r9   //Exec XM2_03 = XM2_00 ^ XM2_02 into r6
    mov    r9, #0         //RESET
    and    r9, r11,  r0   //Exec XM2_04 = MASK3 & ht8_0 into r9
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #132] //Load MASK2AND3XOR2 into r0
    mov   r14, #0         //RESET
    eor   r14,  r9,  r0   //Exec XM2_05 = XM2_04 ^ MASK2AND3XOR2 into r14
    mov    r9, #0         //RESET
    eor    r9, r14, r11   //Exec XM2_06 = XM2_05 ^ MASK3 into r9
    mov   r14, #0         //RESET
    eor   r14,  r6,  r9   //Exec M2_0 = XM2_03 ^ XM2_06 into r14
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #68 ] //Load T14_0 into r6
    mov    r9, #0         //RESET
    eor    r9,  r6,  r8   //Exec M3_0 = T14_0 ^ M1_0 into r9
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #152] //Load i0 into r6
    str    sp, [sp, #108] //RESET
    str.w  r9, [sp, #108] //Store r9/M3_0 on stack
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #72 ] //Load T19_0 into r9
    str    sp, [sp, #68 ] //RESET
    str.w r14, [sp, #68 ] //Store r14/M2_0 on stack
    mov   r14, #0         //RESET
    and   r14,  r6,  r9   //Exec XM4_00 = i0 & T19_0 into r14
    mov    r0, #0         //RESET
    and    r0,  r6, r12   //Exec XM4_01 = i0 & MASK1 into r0
    mov    r6, #0         //RESET
    eor    r6,  r0, r12   //Exec XM4_02 = XM4_01 ^ MASK1 into r6
    mov    r0, #0         //RESET
    eor    r0, r14,  r6   //Exec XM4_03 = XM4_00 ^ XM4_02 into r0
    mov    r6, #0         //RESET
    and    r6,  r7,  r9   //Exec XM4_04 = MASK2 & T19_0 into r6
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #148] //Load MASK1AND2XOR1 into r9
    mov   r14, #0         //RESET
    eor   r14,  r6,  r9   //Exec XM4_05 = XM4_04 ^ MASK1AND2XOR1 into r14
    mov    r6, #0         //RESET
    eor    r6, r14,  r7   //Exec XM4_06 = XM4_05 ^ MASK2 into r6
    mov   r14, #0         //RESET
    eor   r14,  r0,  r6   //Exec M4_0 = XM4_03 ^ XM4_06 into r14
    mov    r0, #0         //RESET
    eor    r0, r14,  r8   //Exec M5_0 = M4_0 ^ M1_0 into r0
    mov    r6, #0         //RESET
    and    r6,  r5,  r2   //Exec XM6_00 = T16_0 & T3_0 into r6
    mov    r8, #0         //RESET
    and    r8,  r5, r12   //Exec XM6_01 = T16_0 & MASK1 into r8
    mov   r14, #0         //RESET
    eor   r14,  r8, r12   //Exec XM6_02 = XM6_01 ^ MASK1 into r14
    mov    r8, #0         //RESET
    eor    r8,  r6, r14   //Exec XM6_03 = XM6_00 ^ XM6_02 into r8
    mov    r6, #0         //RESET
    and    r6, r11,  r2   //Exec XM6_04 = MASK3 & T3_0 into r6
    mov   r14, #0         //RESET
    ldr.w r14, [sp, #140] //Load MASK1AND3XOR1 into r14
    str    sp, [sp, #72 ] //RESET
    str.w  r2, [sp, #72 ] //Store r2/T3_0 on stack
    mov    r2, #0         //RESET
    eor    r2,  r6, r14   //Exec XM6_05 = XM6_04 ^ MASK1AND3XOR1 into r2
    mov    r6, #0         //RESET
    eor    r6,  r2, r11   //Exec XM6_06 = XM6_05 ^ MASK3 into r6
    mov    r2, #0         //RESET
    eor    r2,  r8,  r6   //Exec M6_0 = XM6_03 ^ XM6_06 into r2
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #120] //Load T22_0 into r6
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #76 ] //Load T9_0 into r8
    str    sp, [sp, #40 ] //RESET
    str.w  r5, [sp, #40 ] //Store r5/T16_0 on stack
    mov    r5, #0         //RESET
    and    r5,  r6,  r8   //Exec XM7_00 = T22_0 & T9_0 into r5
    mov   r14, #0         //RESET
    and   r14,  r6, r12   //Exec XM7_01 = T22_0 & MASK1 into r14
    mov    r6, #0         //RESET
    eor    r6, r14, r12   //Exec XM7_02 = XM7_01 ^ MASK1 into r6
    mov   r14, #0         //RESET
    eor   r14,  r5,  r6   //Exec XM7_03 = XM7_00 ^ XM7_02 into r14
    mov    r5, #0         //RESET
    and    r5,  r7,  r8   //Exec XM7_04 = MASK2 & T9_0 into r5
    mov    r6, #0         //RESET
    eor    r6,  r5,  r9   //Exec XM7_05 = XM7_04 ^ MASK1AND2XOR1 into r6
    mov    r5, #0         //RESET
    eor    r5,  r6,  r7   //Exec XM7_06 = XM7_05 ^ MASK2 into r5
    mov    r6, #0         //RESET
    eor    r6, r14,  r5   //Exec M7_0 = XM7_03 ^ XM7_06 into r6
    mov    r5, #0         //RESET
    eor    r5,  r1,  r2   //Exec M8_0 = T26_0 ^ M6_0 into r5
    mov    r1, #0         //RESET
    and    r1, r10,  r4   //Exec XM9_00 = T20_0 & ht17_0 into r1
    mov    r8, #0         //RESET
    and    r8, r10, r11   //Exec XM9_01 = T20_0 & MASK3 into r8
    mov   r14, #0         //RESET
    eor   r14,  r8, r11   //Exec XM9_02 = XM9_01 ^ MASK3 into r14
    mov    r8, #0         //RESET
    eor    r8,  r1, r14   //Exec XM9_03 = XM9_00 ^ XM9_02 into r8
    mov    r1, #0         //RESET
    and    r1,  r7,  r4   //Exec XM9_04 = MASK2 & ht17_0 into r1
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #136] //Load MASK2AND3XOR3 into r4
    mov   r14, #0         //RESET
    eor   r14,  r1,  r4   //Exec XM9_05 = XM9_04 ^ MASK2AND3XOR3 into r14
    mov    r1, #0         //RESET
    eor    r1, r14,  r7   //Exec XM9_06 = XM9_05 ^ MASK2 into r1
    mov   r14, #0         //RESET
    eor   r14,  r8,  r1   //Exec M9_0 = XM9_03 ^ XM9_06 into r14
    mov    r1, #0         //RESET
    eor    r1, r14,  r2   //Exec M10_0 = M9_0 ^ M6_0 into r1
    mov    r2, #0         //RESET
    ldr.w  r2, [sp, #84 ] //Load T15_0 into r2
    mov    r8, #0         //RESET
    and    r8,  r2,  r3   //Exec XM11_00 = T15_0 & T1_0 into r8
    mov   r14, #0         //RESET
    and   r14,  r2, r11   //Exec XM11_01 = T15_0 & MASK3 into r14
    str    sp, [sp, #76 ] //RESET
    str.w r10, [sp, #76 ] //Store r10/T20_0 on stack
    mov   r10, #0         //RESET
    eor   r10, r14, r11   //Exec XM11_02 = XM11_01 ^ MASK3 into r10
    mov   r14, #0         //RESET
    eor   r14,  r8, r10   //Exec XM11_03 = XM11_00 ^ XM11_02 into r14
    mov    r8, #0         //RESET
    and    r8, r12,  r3   //Exec XM11_04 = MASK1 & T1_0 into r8
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #128] //Load MASK1AND3XOR3 into r10
    mov    r3, #0         //RESET
    eor    r3,  r8, r10   //Exec XM11_05 = XM11_04 ^ MASK1AND3XOR3 into r3
    mov    r8, #0         //RESET
    eor    r8,  r3, r12   //Exec XM11_06 = XM11_05 ^ MASK1 into r8
    mov    r3, #0         //RESET
    eor    r3, r14,  r8   //Exec M11_0 = XM11_03 ^ XM11_06 into r3
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #52 ] //Load ht27_0 into r8
    mov   r14, #0         //RESET
    ldr.w r14, [sp, #92 ] //Load T4_0 into r14
    mov    r2, #0         //RESET
    and    r2,  r8, r14   //Exec XM12_00 = ht27_0 & T4_0 into r2
    mov    r4, #0         //RESET
    and    r4,  r8,  r7   //Exec XM12_01 = ht27_0 & MASK2 into r4
    mov    r8, #0         //RESET
    eor    r8,  r4,  r7   //Exec XM12_02 = XM12_01 ^ MASK2 into r8
    mov    r4, #0         //RESET
    eor    r4,  r2,  r8   //Exec XM12_03 = XM12_00 ^ XM12_02 into r4
    mov    r2, #0         //RESET
    and    r2, r11, r14   //Exec XM12_04 = MASK3 & T4_0 into r2
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #132] //Load MASK2AND3XOR2 into r8
    mov   r14, #0         //RESET
    eor   r14,  r2,  r8   //Exec XM12_05 = XM12_04 ^ MASK2AND3XOR2 into r14
    mov    r2, #0         //RESET
    eor    r2, r14, r11   //Exec XM12_06 = XM12_05 ^ MASK3 into r2
    mov   r14, #0         //RESET
    eor   r14,  r4,  r2   //Exec M12_0 = XM12_03 ^ XM12_06 into r14
    mov    r2, #0         //RESET
    eor    r2, r14,  r3   //Exec M13_0 = M12_0 ^ M11_0 into r2
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #100] //Load T10_0 into r4
    mov   r14, #0         //RESET
    ldr.w r14, [sp, #124] //Load T2_0 into r14
    mov    r8, #0         //RESET
    and    r8,  r4, r14   //Exec XM14_00 = T10_0 & T2_0 into r8
    mov   r10, #0         //RESET
    and   r10,  r4, r12   //Exec XM14_01 = T10_0 & MASK1 into r10
    mov    r4, #0         //RESET
    eor    r4, r10, r12   //Exec XM14_02 = XM14_01 ^ MASK1 into r4
    mov   r10, #0         //RESET
    eor   r10,  r8,  r4   //Exec XM14_03 = XM14_00 ^ XM14_02 into r10
    mov    r4, #0         //RESET
    and    r4,  r7, r14   //Exec XM14_04 = MASK2 & T2_0 into r4
    mov    r8, #0         //RESET
    eor    r8,  r4,  r9   //Exec XM14_05 = XM14_04 ^ MASK1AND2XOR1 into r8
    mov    r4, #0         //RESET
    eor    r4,  r8,  r7   //Exec XM14_06 = XM14_05 ^ MASK2 into r4
    mov    r8, #0         //RESET
    eor    r8, r10,  r4   //Exec M14_0 = XM14_03 ^ XM14_06 into r8
    mov    r4, #0         //RESET
    eor    r4,  r8,  r3   //Exec M15_0 = M14_0 ^ M11_0 into r4
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #108] //Load M3_0 into r3
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #68 ] //Load M2_0 into r8
    mov   r10, #0         //RESET
    eor   r10,  r3,  r8   //Exec M16_0 = M3_0 ^ M2_0 into r10
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #60 ] //Load ht24_0 into r3
    mov    r8, #0         //RESET
    eor    r8,  r0,  r3   //Exec M17_0 = M5_0 ^ ht24_0 into r8
    mov    r0, #0         //RESET
    eor    r0,  r5,  r6   //Exec M18_0 = M8_0 ^ M7_0 into r0
    mov    r3, #0         //RESET
    eor    r3,  r1,  r4   //Exec M19_0 = M10_0 ^ M15_0 into r3
    mov    r1, #0         //RESET
    eor    r1, r10,  r2   //Exec M20_0 = M16_0 ^ M13_0 into r1
    mov    r5, #0         //RESET
    eor    r5,  r8,  r4   //Exec M21_0 = M17_0 ^ M15_0 into r5
    mov    r4, #0         //RESET
    eor    r4,  r0,  r2   //Exec M22_0 = M18_0 ^ M13_0 into r4
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #64 ] //Load T25_0 into r0
    mov    r2, #0         //RESET
    eor    r2,  r3,  r0   //Exec M23_0 = M19_0 ^ T25_0 into r2
    mov    r0, #0         //RESET
    eor    r0,  r2, r12   //Exec hm23_0 = M23_0 ^ MASK1 into r0
    mov    r3, #0         //RESET
    eor    r3,  r4,  r2   //Exec M24_0 = M22_0 ^ M23_0 into r3
    mov    r6, #0         //RESET
    and    r6,  r4,  r1   //Exec XM25_00 = M22_0 & M20_0 into r6
    mov    r8, #0         //RESET
    and    r8,  r4, r11   //Exec XM25_01 = M22_0 & MASK3 into r8
    mov   r10, #0         //RESET
    eor   r10,  r8, r11   //Exec XM25_02 = XM25_01 ^ MASK3 into r10
    mov    r8, #0         //RESET
    eor    r8,  r6, r10   //Exec XM25_03 = XM25_00 ^ XM25_02 into r8
    mov    r6, #0         //RESET
    and    r6, r12,  r1   //Exec XM25_04 = MASK1 & M20_0 into r6
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #128] //Load MASK1AND3XOR3 into r10
    mov   r14, #0         //RESET
    eor   r14,  r6, r10   //Exec XM25_05 = XM25_04 ^ MASK1AND3XOR3 into r14
    mov    r6, #0         //RESET
    eor    r6, r14, r12   //Exec XM25_06 = XM25_05 ^ MASK1 into r6
    mov   r14, #0         //RESET
    eor   r14,  r8,  r6   //Exec M25_0 = XM25_03 ^ XM25_06 into r14
    mov    r6, #0         //RESET
    eor    r6, r14,  r7   //Exec hm25_0 = M25_0 ^ MASK2 into r6
    mov    r8, #0         //RESET
    eor    r8,  r5, r14   //Exec M26_0 = M21_0 ^ M25_0 into r8
    mov   r10, #0         //RESET
    eor   r10,  r1,  r5   //Exec M27_0 = M20_0 ^ M21_0 into r10
    mov    r9, #0         //RESET
    eor    r9,  r2, r14   //Exec M28_0 = M23_0 ^ M25_0 into r9
    str    sp, [sp, #108] //RESET
    str.w  r2, [sp, #108] //Store r2/M23_0 on stack
    mov    r2, #0         //RESET
    and    r2, r10,  r9   //Exec XM29_00 = M27_0 & M28_0 into r2
    str    sp, [sp, #68 ] //RESET
    str.w r14, [sp, #68 ] //Store r14/M25_0 on stack
    mov   r14, #0         //RESET
    and   r14, r10,  r7   //Exec XM29_01 = M27_0 & MASK2 into r14
    str    sp, [sp, #64 ] //RESET
    str.w  r4, [sp, #64 ] //Store r4/M22_0 on stack
    mov    r4, #0         //RESET
    eor    r4, r14,  r7   //Exec XM29_02 = XM29_01 ^ MASK2 into r4
    mov   r14, #0         //RESET
    eor   r14,  r2,  r4   //Exec XM29_03 = XM29_00 ^ XM29_02 into r14
    mov    r2, #0         //RESET
    and    r2, r12,  r9   //Exec XM29_04 = MASK1 & M28_0 into r2
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #144] //Load MASK1AND2XOR2 into r4
    mov    r9, #0         //RESET
    eor    r9,  r2,  r4   //Exec XM29_05 = XM29_04 ^ MASK1AND2XOR2 into r9
    mov    r2, #0         //RESET
    eor    r2,  r9, r12   //Exec XM29_06 = XM29_05 ^ MASK1 into r2
    mov    r9, #0         //RESET
    eor    r9, r14,  r2   //Exec M29_0 = XM29_03 ^ XM29_06 into r9
    mov    r2, #0         //RESET
    and    r2,  r3,  r8   //Exec XM30_00 = M24_0 & M26_0 into r2
    mov   r14, #0         //RESET
    and   r14,  r3, r11   //Exec XM30_01 = M24_0 & MASK3 into r14
    str    sp, [sp, #60 ] //RESET
    str.w  r9, [sp, #60 ] //Store r9/M29_0 on stack
    mov    r9, #0         //RESET
    eor    r9, r14, r11   //Exec XM30_02 = XM30_01 ^ MASK3 into r9
    mov   r14, #0         //RESET
    eor   r14,  r2,  r9   //Exec XM30_03 = XM30_00 ^ XM30_02 into r14
    mov    r2, #0         //RESET
    and    r2,  r7,  r8   //Exec XM30_04 = MASK2 & M26_0 into r2
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #136] //Load MASK2AND3XOR3 into r8
    mov    r9, #0         //RESET
    eor    r9,  r2,  r8   //Exec XM30_05 = XM30_04 ^ MASK2AND3XOR3 into r9
    mov    r2, #0         //RESET
    eor    r2,  r9,  r7   //Exec XM30_06 = XM30_05 ^ MASK2 into r2
    mov    r9, #0         //RESET
    eor    r9, r14,  r2   //Exec M30_0 = XM30_03 ^ XM30_06 into r9
    mov    r2, #0         //RESET
    and    r2,  r1,  r0   //Exec XM31_00 = M20_0 & hm23_0 into r2
    mov   r14, #0         //RESET
    and   r14,  r1,  r7   //Exec XM31_01 = M20_0 & MASK2 into r14
    mov    r1, #0         //RESET
    eor    r1, r14,  r7   //Exec XM31_02 = XM31_01 ^ MASK2 into r1
    mov   r14, #0         //RESET
    eor   r14,  r2,  r1   //Exec XM31_03 = XM31_00 ^ XM31_02 into r14
    mov    r1, #0         //RESET
    and    r1, r11,  r0   //Exec XM31_04 = MASK3 & hm23_0 into r1
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #132] //Load MASK2AND3XOR2 into r0
    mov    r2, #0         //RESET
    eor    r2,  r1,  r0   //Exec XM31_05 = XM31_04 ^ MASK2AND3XOR2 into r2
    mov    r1, #0         //RESET
    eor    r1,  r2, r11   //Exec XM31_06 = XM31_05 ^ MASK3 into r1
    mov    r2, #0         //RESET
    eor    r2, r14,  r1   //Exec M31_0 = XM31_03 ^ XM31_06 into r2
    mov    r1, #0         //RESET
    and    r1,  r2, r10   //Exec XM32_00 = M31_0 & M27_0 into r1
    mov   r14, #0         //RESET
    and   r14,  r2, r12   //Exec XM32_01 = M31_0 & MASK1 into r14
    mov    r2, #0         //RESET
    eor    r2, r14, r12   //Exec XM32_02 = XM32_01 ^ MASK1 into r2
    mov   r14, #0         //RESET
    eor   r14,  r1,  r2   //Exec XM32_03 = XM32_00 ^ XM32_02 into r14
    mov    r1, #0         //RESET
    and    r1, r11, r10   //Exec XM32_04 = MASK3 & M27_0 into r1
    mov    r2, #0         //RESET
    ldr.w  r2, [sp, #140] //Load MASK1AND3XOR1 into r2
    mov    r0, #0         //RESET
    eor    r0,  r1,  r2   //Exec XM32_05 = XM32_04 ^ MASK1AND3XOR1 into r0
    mov    r1, #0         //RESET
    eor    r1,  r0, r11   //Exec XM32_06 = XM32_05 ^ MASK3 into r1
    mov    r0, #0         //RESET
    eor    r0, r14,  r1   //Exec M32_0 = XM32_03 ^ XM32_06 into r0
    mov    r1, #0         //RESET
    eor    r1, r10,  r6   //Exec M33_0 = M27_0 ^ hm25_0 into r1
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #64 ] //Load M22_0 into r6
    mov   r10, #0         //RESET
    and   r10,  r6,  r5   //Exec XM34_00 = M22_0 & M21_0 into r10
    mov   r14, #0         //RESET
    and   r14,  r6,  r7   //Exec XM34_01 = M22_0 & MASK2 into r14
    mov    r6, #0         //RESET
    eor    r6, r14,  r7   //Exec XM34_02 = XM34_01 ^ MASK2 into r6
    mov   r14, #0         //RESET
    eor   r14, r10,  r6   //Exec XM34_03 = XM34_00 ^ XM34_02 into r14
    mov    r6, #0         //RESET
    and    r6, r12,  r5   //Exec XM34_04 = MASK1 & M21_0 into r6
    mov   r10, #0         //RESET
    eor   r10,  r6,  r4   //Exec XM34_05 = XM34_04 ^ MASK1AND2XOR2 into r10
    mov    r6, #0         //RESET
    eor    r6, r10, r12   //Exec XM34_06 = XM34_05 ^ MASK1 into r6
    mov   r10, #0         //RESET
    eor   r10, r14,  r6   //Exec M34_0 = XM34_03 ^ XM34_06 into r10
    mov    r6, #0         //RESET
    and    r6, r10,  r3   //Exec XM35_00 = M34_0 & M24_0 into r6
    mov   r14, #0         //RESET
    and   r14, r10,  r7   //Exec XM35_01 = M34_0 & MASK2 into r14
    mov   r10, #0         //RESET
    eor   r10, r14,  r7   //Exec XM35_02 = XM35_01 ^ MASK2 into r10
    mov   r14, #0         //RESET
    eor   r14,  r6, r10   //Exec XM35_03 = XM35_00 ^ XM35_02 into r14
    mov    r6, #0         //RESET
    and    r6, r12,  r3   //Exec XM35_04 = MASK1 & M24_0 into r6
    mov   r10, #0         //RESET
    eor   r10,  r6,  r4   //Exec XM35_05 = XM35_04 ^ MASK1AND2XOR2 into r10
    mov    r6, #0         //RESET
    eor    r6, r10, r12   //Exec XM35_06 = XM35_05 ^ MASK1 into r6
    mov   r10, #0         //RESET
    eor   r10, r14,  r6   //Exec M35_0 = XM35_03 ^ XM35_06 into r10
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #68 ] //Load M25_0 into r6
    mov   r14, #0         //RESET
    eor   r14,  r3,  r6   //Exec M36_0 = M24_0 ^ M25_0 into r14
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #60 ] //Load M29_0 into r3
    mov    r6, #0         //RESET
    eor    r6,  r5,  r3   //Exec M37_0 = M21_0 ^ M29_0 into r6
    mov    r3, #0         //RESET
    eor    r3,  r0,  r1   //Exec M38_0 = M32_0 ^ M33_0 into r3
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #108] //Load M23_0 into r0
    mov    r1, #0         //RESET
    eor    r1,  r0,  r9   //Exec M39_0 = M23_0 ^ M30_0 into r1
    mov    r0, #0         //RESET
    eor    r0, r10, r14   //Exec M40_0 = M35_0 ^ M36_0 into r0
    mov    r5, #0         //RESET
    eor    r5,  r3,  r0   //Exec M41_0 = M38_0 ^ M40_0 into r5
    mov    r9, #0         //RESET
    eor    r9,  r6,  r1   //Exec M42_0 = M37_0 ^ M39_0 into r9
    mov   r10, #0         //RESET
    eor   r10,  r6,  r3   //Exec M43_0 = M37_0 ^ M38_0 into r10
    mov   r14, #0         //RESET
    eor   r14,  r1,  r0   //Exec M44_0 = M39_0 ^ M40_0 into r14
    str    sp, [sp, #108] //RESET
    str.w  r6, [sp, #108] //Store r6/M37_0 on stack
    mov    r6, #0         //RESET
    eor    r6,  r9,  r5   //Exec M45_0 = M42_0 ^ M41_0 into r6
    str    sp, [sp, #68 ] //RESET
    str.w  r5, [sp, #68 ] //Store r5/M41_0 on stack
    mov    r5, #0         //RESET
    ldr.w  r5, [sp, #48 ] //Load T6_0 into r5
    str    sp, [sp, #64 ] //RESET
    str.w  r6, [sp, #64 ] //Store r6/M45_0 on stack
    mov    r6, #0         //RESET
    and    r6, r14,  r5   //Exec XM46_00 = M44_0 & T6_0 into r6
    str    sp, [sp, #60 ] //RESET
    str.w  r9, [sp, #60 ] //Store r9/M42_0 on stack
    mov    r9, #0         //RESET
    and    r9, r14, r12   //Exec XM46_01 = M44_0 & MASK1 into r9
    str    sp, [sp, #52 ] //RESET
    str.w r14, [sp, #52 ] //Store r14/M44_0 on stack
    mov   r14, #0         //RESET
    eor   r14,  r9, r12   //Exec XM46_02 = XM46_01 ^ MASK1 into r14
    mov    r9, #0         //RESET
    eor    r9,  r6, r14   //Exec XM46_03 = XM46_00 ^ XM46_02 into r9
    mov    r6, #0         //RESET
    and    r6, r11,  r5   //Exec XM46_04 = MASK3 & T6_0 into r6
    mov    r5, #0         //RESET
    eor    r5,  r6,  r2   //Exec XM46_05 = XM46_04 ^ MASK1AND3XOR1 into r5
    mov    r6, #0         //RESET
    eor    r6,  r5, r11   //Exec XM46_06 = XM46_05 ^ MASK3 into r6
    mov    r5, #0         //RESET
    eor    r5,  r9,  r6   //Exec M46_0 = XM46_03 ^ XM46_06 into r5
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #112] //Load T8_0 into r6
    mov    r9, #0         //RESET
    and    r9,  r0,  r6   //Exec XM47_00 = M40_0 & T8_0 into r9
    mov   r14, #0         //RESET
    and   r14,  r0, r11   //Exec XM47_01 = M40_0 & MASK3 into r14
    str    sp, [sp, #48 ] //RESET
    str.w  r5, [sp, #48 ] //Store r5/M46_0 on stack
    mov    r5, #0         //RESET
    eor    r5, r14, r11   //Exec XM47_02 = XM47_01 ^ MASK3 into r5
    mov   r14, #0         //RESET
    eor   r14,  r9,  r5   //Exec XM47_03 = XM47_00 ^ XM47_02 into r14
    mov    r5, #0         //RESET
    and    r5,  r7,  r6   //Exec XM47_04 = MASK2 & T8_0 into r5
    mov    r6, #0         //RESET
    eor    r6,  r5,  r8   //Exec XM47_05 = XM47_04 ^ MASK2AND3XOR3 into r6
    mov    r5, #0         //RESET
    eor    r5,  r6,  r7   //Exec XM47_06 = XM47_05 ^ MASK2 into r5
    mov    r6, #0         //RESET
    eor    r6, r14,  r5   //Exec M47_0 = XM47_03 ^ XM47_06 into r6
    mov    r5, #0         //RESET
    ldr.w  r5, [sp, #152] //Load i0 into r5
    mov    r9, #0         //RESET
    and    r9,  r1,  r5   //Exec XM48_00 = M39_0 & i0 into r9
    mov   r14, #0         //RESET
    and   r14,  r1,  r7   //Exec XM48_01 = M39_0 & MASK2 into r14
    str    sp, [sp, #112] //RESET
    str.w  r6, [sp, #112] //Store r6/M47_0 on stack
    mov    r6, #0         //RESET
    eor    r6, r14,  r7   //Exec XM48_02 = XM48_01 ^ MASK2 into r6
    mov   r14, #0         //RESET
    eor   r14,  r9,  r6   //Exec XM48_03 = XM48_00 ^ XM48_02 into r14
    mov    r6, #0         //RESET
    and    r6, r12,  r5   //Exec XM48_04 = MASK1 & i0 into r6
    mov    r5, #0         //RESET
    eor    r5,  r6,  r4   //Exec XM48_05 = XM48_04 ^ MASK1AND2XOR2 into r5
    mov    r6, #0         //RESET
    eor    r6,  r5, r12   //Exec XM48_06 = XM48_05 ^ MASK1 into r6
    mov    r5, #0         //RESET
    eor    r5, r14,  r6   //Exec M48_0 = XM48_03 ^ XM48_06 into r5
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #40 ] //Load T16_0 into r6
    mov    r9, #0         //RESET
    and    r9, r10,  r6   //Exec XM49_00 = M43_0 & T16_0 into r9
    mov   r14, #0         //RESET
    and   r14, r10, r11   //Exec XM49_01 = M43_0 & MASK3 into r14
    str    sp, [sp, #152] //RESET
    str.w  r5, [sp, #152] //Store r5/M48_0 on stack
    mov    r5, #0         //RESET
    eor    r5, r14, r11   //Exec XM49_02 = XM49_01 ^ MASK3 into r5
    mov   r14, #0         //RESET
    eor   r14,  r9,  r5   //Exec XM49_03 = XM49_00 ^ XM49_02 into r14
    mov    r5, #0         //RESET
    and    r5,  r7,  r6   //Exec XM49_04 = MASK2 & T16_0 into r5
    mov    r6, #0         //RESET
    eor    r6,  r5,  r8   //Exec XM49_05 = XM49_04 ^ MASK2AND3XOR3 into r6
    mov    r5, #0         //RESET
    eor    r5,  r6,  r7   //Exec XM49_06 = XM49_05 ^ MASK2 into r5
    mov    r6, #0         //RESET
    eor    r6, r14,  r5   //Exec M49_0 = XM49_03 ^ XM49_06 into r6
    mov    r5, #0         //RESET
    ldr.w  r5, [sp, #104] //Load ht9_0 into r5
    mov    r9, #0         //RESET
    and    r9,  r5,  r3   //Exec XM50_00 = ht9_0 & M38_0 into r9
    mov   r14, #0         //RESET
    and   r14,  r5, r12   //Exec XM50_01 = ht9_0 & MASK1 into r14
    mov    r5, #0         //RESET
    eor    r5, r14, r12   //Exec XM50_02 = XM50_01 ^ MASK1 into r5
    mov   r14, #0         //RESET
    eor   r14,  r9,  r5   //Exec XM50_03 = XM50_00 ^ XM50_02 into r14
    mov    r5, #0         //RESET
    and    r5, r11,  r3   //Exec XM50_04 = MASK3 & M38_0 into r5
    mov    r9, #0         //RESET
    eor    r9,  r5,  r2   //Exec XM50_05 = XM50_04 ^ MASK1AND3XOR1 into r9
    mov    r5, #0         //RESET
    eor    r5,  r9, r11   //Exec XM50_06 = XM50_05 ^ MASK3 into r5
    mov    r9, #0         //RESET
    eor    r9, r14,  r5   //Exec M50_0 = XM50_03 ^ XM50_06 into r9
    mov    r5, #0         //RESET
    ldr.w  r5, [sp, #108] //Load M37_0 into r5
    mov   r14, #0         //RESET
    ldr.w r14, [sp, #88 ] //Load T17_0 into r14
    str    sp, [sp, #104] //RESET
    str.w  r6, [sp, #104] //Store r6/M49_0 on stack
    mov    r6, #0         //RESET
    and    r6,  r5, r14   //Exec XM51_00 = M37_0 & T17_0 into r6
    str    sp, [sp, #40 ] //RESET
    str.w  r9, [sp, #40 ] //Store r9/M50_0 on stack
    mov    r9, #0         //RESET
    and    r9,  r5,  r7   //Exec XM51_01 = M37_0 & MASK2 into r9
    mov    r5, #0         //RESET
    eor    r5,  r9,  r7   //Exec XM51_02 = XM51_01 ^ MASK2 into r5
    mov    r9, #0         //RESET
    eor    r9,  r6,  r5   //Exec XM51_03 = XM51_00 ^ XM51_02 into r9
    mov    r5, #0         //RESET
    and    r5, r11, r14   //Exec XM51_04 = MASK3 & T17_0 into r5
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #132] //Load MASK2AND3XOR2 into r6
    mov   r14, #0         //RESET
    eor   r14,  r5,  r6   //Exec XM51_05 = XM51_04 ^ MASK2AND3XOR2 into r14
    mov    r5, #0         //RESET
    eor    r5, r14, r11   //Exec XM51_06 = XM51_05 ^ MASK3 into r5
    mov   r14, #0         //RESET
    eor   r14,  r9,  r5   //Exec M51_0 = XM51_03 ^ XM51_06 into r14
    mov    r5, #0         //RESET
    ldr.w  r5, [sp, #84 ] //Load T15_0 into r5
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #60 ] //Load M42_0 into r9
    str    sp, [sp, #88 ] //RESET
    str.w r14, [sp, #88 ] //Store r14/M51_0 on stack
    mov   r14, #0         //RESET
    and   r14,  r5,  r9   //Exec XM52_00 = T15_0 & M42_0 into r14
    str    sp, [sp, #36 ] //RESET
    str.w  r3, [sp, #36 ] //Store r3/M38_0 on stack
    mov    r3, #0         //RESET
    and    r3,  r5,  r7   //Exec XM52_01 = T15_0 & MASK2 into r3
    mov    r5, #0         //RESET
    eor    r5,  r3,  r7   //Exec XM52_02 = XM52_01 ^ MASK2 into r5
    mov    r3, #0         //RESET
    eor    r3, r14,  r5   //Exec XM52_03 = XM52_00 ^ XM52_02 into r3
    mov    r5, #0         //RESET
    and    r5, r12,  r9   //Exec XM52_04 = MASK1 & M42_0 into r5
    mov   r14, #0         //RESET
    eor   r14,  r5,  r4   //Exec XM52_05 = XM52_04 ^ MASK1AND2XOR2 into r14
    mov    r5, #0         //RESET
    eor    r5, r14, r12   //Exec XM52_06 = XM52_05 ^ MASK1 into r5
    mov   r14, #0         //RESET
    eor   r14,  r3,  r5   //Exec M52_0 = XM52_03 ^ XM52_06 into r14
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #56 ] //Load T27_0 into r3
    mov    r5, #0         //RESET
    ldr.w  r5, [sp, #64 ] //Load M45_0 into r5
    str    sp, [sp, #84 ] //RESET
    str.w r14, [sp, #84 ] //Store r14/M52_0 on stack
    mov   r14, #0         //RESET
    and   r14,  r3,  r5   //Exec XM53_00 = T27_0 & M45_0 into r14
    mov    r9, #0         //RESET
    and    r9,  r3, r12   //Exec XM53_01 = T27_0 & MASK1 into r9
    mov    r3, #0         //RESET
    eor    r3,  r9, r12   //Exec XM53_02 = XM53_01 ^ MASK1 into r3
    mov    r9, #0         //RESET
    eor    r9, r14,  r3   //Exec XM53_03 = XM53_00 ^ XM53_02 into r9
    mov    r3, #0         //RESET
    and    r3,  r7,  r5   //Exec XM53_04 = MASK2 & M45_0 into r3
    mov   r14, #0         //RESET
    ldr.w r14, [sp, #148] //Load MASK1AND2XOR1 into r14
    mov    r5, #0         //RESET
    eor    r5,  r3, r14   //Exec XM53_05 = XM53_04 ^ MASK1AND2XOR1 into r5
    mov    r3, #0         //RESET
    eor    r3,  r5,  r7   //Exec XM53_06 = XM53_05 ^ MASK2 into r3
    mov    r5, #0         //RESET
    eor    r5,  r9,  r3   //Exec M53_0 = XM53_03 ^ XM53_06 into r5
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #100] //Load T10_0 into r3
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #68 ] //Load M41_0 into r9
    str    sp, [sp, #56 ] //RESET
    str.w  r5, [sp, #56 ] //Store r5/M53_0 on stack
    mov    r5, #0         //RESET
    and    r5,  r3,  r9   //Exec XM54_00 = T10_0 & M41_0 into r5
    mov   r14, #0         //RESET
    and   r14,  r3, r11   //Exec XM54_01 = T10_0 & MASK3 into r14
    mov    r3, #0         //RESET
    eor    r3, r14, r11   //Exec XM54_02 = XM54_01 ^ MASK3 into r3
    mov   r14, #0         //RESET
    eor   r14,  r5,  r3   //Exec XM54_03 = XM54_00 ^ XM54_02 into r14
    mov    r3, #0         //RESET
    and    r3,  r7,  r9   //Exec XM54_04 = MASK2 & M41_0 into r3
    mov    r5, #0         //RESET
    eor    r5,  r3,  r8   //Exec XM54_05 = XM54_04 ^ MASK2AND3XOR3 into r5
    mov    r3, #0         //RESET
    eor    r3,  r5,  r7   //Exec XM54_06 = XM54_05 ^ MASK2 into r3
    mov    r5, #0         //RESET
    eor    r5, r14,  r3   //Exec M54_0 = XM54_03 ^ XM54_06 into r5
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #52 ] //Load M44_0 into r3
    //Wait, I could have recomputed that!
    mov   r14, #0         //RESET
    ldr.w r14, [sp, #96 ] //Load ht13_0 into r14
    str    sp, [sp, #100] //RESET
    str.w  r5, [sp, #100] //Store r5/M54_0 on stack
    mov    r5, #0         //RESET
    and    r5,  r3, r14   //Exec XM55_00 = M44_0 & ht13_0 into r5
    mov    r9, #0         //RESET
    and    r9,  r3,  r7   //Exec XM55_01 = M44_0 & MASK2 into r9
    mov    r3, #0         //RESET
    eor    r3,  r9,  r7   //Exec XM55_02 = XM55_01 ^ MASK2 into r3
    mov    r9, #0         //RESET
    eor    r9,  r5,  r3   //Exec XM55_03 = XM55_00 ^ XM55_02 into r9
    mov    r3, #0         //RESET
    and    r3, r11, r14   //Exec XM55_04 = MASK3 & ht13_0 into r3
    mov    r5, #0         //RESET
    eor    r5,  r3,  r6   //Exec XM55_05 = XM55_04 ^ MASK2AND3XOR2 into r5
    mov    r3, #0         //RESET
    eor    r3,  r5, r11   //Exec XM55_06 = XM55_05 ^ MASK3 into r3
    mov    r5, #0         //RESET
    eor    r5,  r9,  r3   //Exec M55_0 = XM55_03 ^ XM55_06 into r5
    mov    r3, #0         //RESET
    ldr.w  r3, [sp, #44 ] //Load T23_0 into r3
    mov    r9, #0         //RESET
    and    r9,  r0,  r3   //Exec XM56_00 = M40_0 & T23_0 into r9
    mov   r14, #0         //RESET
    and   r14,  r0, r11   //Exec XM56_01 = M40_0 & MASK3 into r14
    mov    r0, #0         //RESET
    eor    r0, r14, r11   //Exec XM56_02 = XM56_01 ^ MASK3 into r0
    mov   r14, #0         //RESET
    eor   r14,  r9,  r0   //Exec XM56_03 = XM56_00 ^ XM56_02 into r14
    mov    r0, #0         //RESET
    and    r0,  r7,  r3   //Exec XM56_04 = MASK2 & T23_0 into r0
    mov    r3, #0         //RESET
    eor    r3,  r0,  r8   //Exec XM56_05 = XM56_04 ^ MASK2AND3XOR3 into r3
    mov    r0, #0         //RESET
    eor    r0,  r3,  r7   //Exec XM56_06 = XM56_05 ^ MASK2 into r0
    mov    r3, #0         //RESET
    eor    r3, r14,  r0   //Exec M56_0 = XM56_03 ^ XM56_06 into r3
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #80 ] //Load ht19_0 into r0
    mov    r8, #0         //RESET
    and    r8,  r0,  r1   //Exec XM57_00 = ht19_0 & M39_0 into r8
    mov    r9, #0         //RESET
    and    r9,  r0, r12   //Exec XM57_01 = ht19_0 & MASK1 into r9
    mov    r0, #0         //RESET
    eor    r0,  r9, r12   //Exec XM57_02 = XM57_01 ^ MASK1 into r0
    mov    r9, #0         //RESET
    eor    r9,  r8,  r0   //Exec XM57_03 = XM57_00 ^ XM57_02 into r9
    mov    r0, #0         //RESET
    and    r0, r11,  r1   //Exec XM57_04 = MASK3 & M39_0 into r0
    mov    r1, #0         //RESET
    eor    r1,  r0,  r2   //Exec XM57_05 = XM57_04 ^ MASK1AND3XOR1 into r1
    mov    r0, #0         //RESET
    eor    r0,  r1, r11   //Exec XM57_06 = XM57_05 ^ MASK3 into r0
    mov    r1, #0         //RESET
    eor    r1,  r9,  r0   //Exec M57_0 = XM57_03 ^ XM57_06 into r1
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #72 ] //Load T3_0 into r0
    mov    r2, #0         //RESET
    and    r2,  r0, r10   //Exec XM58_00 = T3_0 & M43_0 into r2
    mov    r8, #0         //RESET
    and    r8,  r0,  r7   //Exec XM58_01 = T3_0 & MASK2 into r8
    mov    r0, #0         //RESET
    eor    r0,  r8,  r7   //Exec XM58_02 = XM58_01 ^ MASK2 into r0
    mov    r8, #0         //RESET
    eor    r8,  r2,  r0   //Exec XM58_03 = XM58_00 ^ XM58_02 into r8
    mov    r0, #0         //RESET
    and    r0, r12, r10   //Exec XM58_04 = MASK1 & M43_0 into r0
    mov    r2, #0         //RESET
    eor    r2,  r0,  r4   //Exec XM58_05 = XM58_04 ^ MASK1AND2XOR2 into r2
    mov    r0, #0         //RESET
    eor    r0,  r2, r12   //Exec XM58_06 = XM58_05 ^ MASK1 into r0
    mov    r2, #0         //RESET
    eor    r2,  r8,  r0   //Exec M58_0 = XM58_03 ^ XM58_06 into r2
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #36 ] //Load M38_0 into r0
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #120] //Load T22_0 into r8
    mov    r9, #0         //RESET
    and    r9,  r0,  r8   //Exec XM59_00 = M38_0 & T22_0 into r9
    mov   r10, #0         //RESET
    and   r10,  r0,  r7   //Exec XM59_01 = M38_0 & MASK2 into r10
    mov    r0, #0         //RESET
    eor    r0, r10,  r7   //Exec XM59_02 = XM59_01 ^ MASK2 into r0
    mov   r10, #0         //RESET
    eor   r10,  r9,  r0   //Exec XM59_03 = XM59_00 ^ XM59_02 into r10
    mov    r0, #0         //RESET
    and    r0, r12,  r8   //Exec XM59_04 = MASK1 & T22_0 into r0
    mov    r8, #0         //RESET
    eor    r8,  r0,  r4   //Exec XM59_05 = XM59_04 ^ MASK1AND2XOR2 into r8
    mov    r0, #0         //RESET
    eor    r0,  r8, r12   //Exec XM59_06 = XM59_05 ^ MASK1 into r0
    mov    r4, #0         //RESET
    eor    r4, r10,  r0   //Exec M59_0 = XM59_03 ^ XM59_06 into r4
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #108] //Load M37_0 into r0
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #76 ] //Load T20_0 into r8
    mov    r9, #0         //RESET
    and    r9,  r0,  r8   //Exec XM60_00 = M37_0 & T20_0 into r9
    mov   r10, #0         //RESET
    and   r10,  r0,  r7   //Exec XM60_01 = M37_0 & MASK2 into r10
    mov    r0, #0         //RESET
    eor    r0, r10,  r7   //Exec XM60_02 = XM60_01 ^ MASK2 into r0
    mov   r10, #0         //RESET
    eor   r10,  r9,  r0   //Exec XM60_03 = XM60_00 ^ XM60_02 into r10
    mov    r0, #0         //RESET
    and    r0, r11,  r8   //Exec XM60_04 = MASK3 & T20_0 into r0
    mov    r8, #0         //RESET
    eor    r8,  r0,  r6   //Exec XM60_05 = XM60_04 ^ MASK2AND3XOR2 into r8
    mov    r0, #0         //RESET
    eor    r0,  r8, r11   //Exec XM60_06 = XM60_05 ^ MASK3 into r0
    mov    r8, #0         //RESET
    eor    r8, r10,  r0   //Exec M60_0 = XM60_03 ^ XM60_06 into r8
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #116] //Load T1_0 into r0
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #60 ] //Load M42_0 into r9
    mov   r10, #0         //RESET
    and   r10,  r0,  r9   //Exec XM61_00 = T1_0 & M42_0 into r10
    mov   r14, #0         //RESET
    and   r14,  r0,  r7   //Exec XM61_01 = T1_0 & MASK2 into r14
    mov    r0, #0         //RESET
    eor    r0, r14,  r7   //Exec XM61_02 = XM61_01 ^ MASK2 into r0
    mov   r14, #0         //RESET
    eor   r14, r10,  r0   //Exec XM61_03 = XM61_00 ^ XM61_02 into r14
    mov    r0, #0         //RESET
    and    r0, r11,  r9   //Exec XM61_04 = MASK3 & M42_0 into r0
    mov    r9, #0         //RESET
    eor    r9,  r0,  r6   //Exec XM61_05 = XM61_04 ^ MASK2AND3XOR2 into r9
    mov    r0, #0         //RESET
    eor    r0,  r9, r11   //Exec XM61_06 = XM61_05 ^ MASK3 into r0
    mov    r6, #0         //RESET
    eor    r6, r14,  r0   //Exec M61_0 = XM61_03 ^ XM61_06 into r6
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #92 ] //Load T4_0 into r0
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #64 ] //Load M45_0 into r9
    mov   r10, #0         //RESET
    and   r10,  r0,  r9   //Exec XM62_00 = T4_0 & M45_0 into r10
    mov   r14, #0         //RESET
    and   r14,  r0, r12   //Exec XM62_01 = T4_0 & MASK1 into r14
    mov    r0, #0         //RESET
    eor    r0, r14, r12   //Exec XM62_02 = XM62_01 ^ MASK1 into r0
    mov   r14, #0         //RESET
    eor   r14, r10,  r0   //Exec XM62_03 = XM62_00 ^ XM62_02 into r14
    mov    r0, #0         //RESET
    and    r0,  r7,  r9   //Exec XM62_04 = MASK2 & M45_0 into r0
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #148] //Load MASK1AND2XOR1 into r9
    mov   r10, #0         //RESET
    eor   r10,  r0,  r9   //Exec XM62_05 = XM62_04 ^ MASK1AND2XOR1 into r10
    mov    r0, #0         //RESET
    eor    r0, r10,  r7   //Exec XM62_06 = XM62_05 ^ MASK2 into r0
    mov    r9, #0         //RESET
    eor    r9, r14,  r0   //Exec M62_0 = XM62_03 ^ XM62_06 into r9
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #124] //Load T2_0 into r0
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #68 ] //Load M41_0 into r10
    mov   r14, #0         //RESET
    and   r14,  r0, r10   //Exec XM63_00 = T2_0 & M41_0 into r14
    str    sp, [sp, #148] //RESET
    str.w  r1, [sp, #148] //Store r1/M57_0 on stack
    mov    r1, #0         //RESET
    and    r1,  r0, r11   //Exec XM63_01 = T2_0 & MASK3 into r1
    mov    r0, #0         //RESET
    eor    r0,  r1, r11   //Exec XM63_02 = XM63_01 ^ MASK3 into r0
    mov    r1, #0         //RESET
    eor    r1, r14,  r0   //Exec XM63_03 = XM63_00 ^ XM63_02 into r1
    mov    r0, #0         //RESET
    and    r0, r12, r10   //Exec XM63_04 = MASK1 & M41_0 into r0
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #128] //Load MASK1AND3XOR3 into r10
    mov   r14, #0         //RESET
    eor   r14,  r0, r10   //Exec XM63_05 = XM63_04 ^ MASK1AND3XOR3 into r14
    mov    r0, #0         //RESET
    eor    r0, r14, r12   //Exec XM63_06 = XM63_05 ^ MASK1 into r0
    mov   r10, #0         //RESET
    eor   r10,  r1,  r0   //Exec M63_0 = XM63_03 ^ XM63_06 into r10
    mov    r0, #0         //RESET
    eor    r0,  r6,  r9   //Exec L0_0 = M61_0 ^ M62_0 into r0
    mov    r1, #0         //RESET
    ldr.w  r1, [sp, #40 ] //Load M50_0 into r1
    mov   r14, #0         //RESET
    eor   r14,  r1,  r3   //Exec L1_0 = M50_0 ^ M56_0 into r14
    mov   r11, #0         //RESET
    eor   r11, r14,  r7   //Exec ml1_0 = L1_0 ^ MASK2 into r11
    mov    r7, #0         //RESET
    ldr.w  r7, [sp, #48 ] //Load M46_0 into r7
    mov   r12, #0         //RESET
    ldr.w r12, [sp, #152] //Load M48_0 into r12
    str    sp, [sp, #144] //RESET
    str.w r11, [sp, #144] //Store r11/ml1_0 on stack
    mov   r11, #0         //RESET
    eor   r11,  r7, r12   //Exec L2_0 = M46_0 ^ M48_0 into r11
    str    sp, [sp, #140] //RESET
    str.w r10, [sp, #140] //Store r10/M63_0 on stack
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #112] //Load M47_0 into r10
    str    sp, [sp, #136] //RESET
    str.w  r3, [sp, #136] //Store r3/M56_0 on stack
    mov    r3, #0         //RESET
    eor    r3, r10,  r5   //Exec L3_0 = M47_0 ^ M55_0 into r3
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #100] //Load M54_0 into r10
    str    sp, [sp, #132] //RESET
    str.w  r5, [sp, #132] //Store r5/M55_0 on stack
    mov    r5, #0         //RESET
    eor    r5, r10,  r2   //Exec L4_0 = M54_0 ^ M58_0 into r5
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #104] //Load M49_0 into r10
    str    sp, [sp, #128] //RESET
    str.w  r2, [sp, #128] //Store r2/M58_0 on stack
    mov    r2, #0         //RESET
    eor    r2, r10,  r6   //Exec L5_0 = M49_0 ^ M61_0 into r2
    mov   r10, #0         //RESET
    eor   r10,  r9,  r2   //Exec L6_0 = M62_0 ^ L5_0 into r10
    mov    r2, #0         //RESET
    eor    r2,  r7,  r3   //Exec L7_0 = M46_0 ^ L3_0 into r2
    mov    r7, #0         //RESET
    ldr.w  r7, [sp, #88 ] //Load M51_0 into r7
    mov    r9, #0         //RESET
    eor    r9,  r7,  r4   //Exec L8_0 = M51_0 ^ M59_0 into r9
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #84 ] //Load M52_0 into r4
    str    sp, [sp, #124] //RESET
    str.w r10, [sp, #124] //Store r10/L6_0 on stack
    mov   r10, #0         //RESET
    ldr.w r10, [sp, #56 ] //Load M53_0 into r10
    str    sp, [sp, #120] //RESET
    str.w  r3, [sp, #120] //Store r3/L3_0 on stack
    mov    r3, #0         //RESET
    eor    r3,  r4, r10   //Exec L9_0 = M52_0 ^ M53_0 into r3
    str    sp, [sp, #116] //RESET
    str.w  r3, [sp, #116] //Store r3/L9_0 on stack
    mov    r3, #0         //RESET
    eor    r3, r10,  r5   //Exec L10_0 = M53_0 ^ L4_0 into r3
    mov   r10, #0         //RESET
    eor   r10,  r8, r11   //Exec L11_0 = M60_0 ^ L2_0 into r10
    mov    r8, #0         //RESET
    eor    r8, r12,  r7   //Exec L12_0 = M48_0 ^ M51_0 into r8
    mov    r7, #0         //RESET
    eor    r7,  r1,  r0   //Exec L13_0 = M50_0 ^ L0_0 into r7
    mov    r1, #0         //RESET
    eor    r1,  r4,  r6   //Exec L14_0 = M52_0 ^ M61_0 into r1
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #132] //Load M55_0 into r4
    mov    r6, #0         //RESET
    eor    r6,  r4, r14   //Exec L15_0 = M55_0 ^ L1_0 into r6
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #136] //Load M56_0 into r4
    mov   r12, #0         //RESET
    eor   r12,  r4,  r0   //Exec L16_0 = M56_0 ^ L0_0 into r12
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #148] //Load M57_0 into r4
    str    sp, [sp, #152] //RESET
    str.w  r7, [sp, #152] //Store r7/L13_0 on stack
    mov    r7, #0         //RESET
    eor    r7,  r4, r14   //Exec L17_0 = M57_0 ^ L1_0 into r7
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #128] //Load M58_0 into r4
    str    sp, [sp, #148] //RESET
    str.w r12, [sp, #148] //Store r12/L16_0 on stack
    mov   r12, #0         //RESET
    eor   r12,  r4,  r9   //Exec L18_0 = M58_0 ^ L8_0 into r12
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #140] //Load M63_0 into r4
    str    sp, [sp, #136] //RESET
    str.w  r7, [sp, #136] //Store r7/L17_0 on stack
    mov    r7, #0         //RESET
    eor    r7,  r4,  r5   //Exec L19_0 = M63_0 ^ L4_0 into r7
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #144] //Load ml1_0 into r4
    mov    r5, #0         //RESET
    eor    r5,  r0,  r4   //Exec L20_0 = L0_0 ^ ml1_0 into r5
    mov    r0, #0         //RESET
    eor    r0, r14,  r2   //Exec L21_0 = L1_0 ^ L7_0 into r0
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #168] //Load MASK1 into r4
    mov   r14, #0         //RESET
    eor   r14,  r0,  r4   //Exec hl21_0 = L21_0 ^ MASK1 into r14
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #120] //Load L3_0 into r0
    mov    r4, #0         //RESET
    eor    r4,  r0,  r8   //Exec L22_0 = L3_0 ^ L12_0 into r4
    mov    r0, #0         //RESET
    eor    r0, r12, r11   //Exec L23_0 = L18_0 ^ L2_0 into r0
    mov    r8, #0         //RESET
    ldr.w  r8, [sp, #116] //Load L9_0 into r8
    mov   r11, #0         //RESET
    eor   r11,  r6,  r8   //Exec L24_0 = L15_0 ^ L9_0 into r11
    mov    r6, #0         //RESET
    ldr.w  r6, [sp, #124] //Load L6_0 into r6
    mov   r12, #0         //RESET
    eor   r12,  r6,  r3   //Exec L25_0 = L6_0 ^ L10_0 into r12
    str    sp, [sp, #32 ] //RESET
    str.w  r0, [sp, #32 ] //Store r0/L23_0 on stack
    mov    r0, #0         //RESET
    eor    r0,  r2,  r8   //Exec L26_0 = L7_0 ^ L9_0 into r0
    mov    r2, #0         //RESET
    eor    r2,  r9,  r3   //Exec L27_0 = L8_0 ^ L10_0 into r2
    mov    r3, #0         //RESET
    eor    r3, r10,  r1   //Exec L28_0 = L11_0 ^ L14_0 into r3
    mov    r1, #0         //RESET
    ldr.w  r1, [sp, #136] //Load L17_0 into r1
    mov    r8, #0         //RESET
    eor    r8, r10,  r1   //Exec L29_0 = L11_0 ^ L17_0 into r8
    mov    r1, #0         //RESET
    eor    r1,  r6, r11   //Exec o7 = L6_0 ^ L24_0 into r1
    mov    r9, #0         //RESET
    ldr.w  r9, [sp, #148] //Load L16_0 into r9
    mov   r10, #0         //RESET
    eor   r10,  r9,  r0   //Exec Y1_0 = L16_0 ^ L26_0 ^ 1 into r10
    mov    r0, #0         //RESET
    ldr.w  r0, [sp, #160] //Load MASK3 into r0
    mov    r9, #0         //RESET
    eor    r9, r10,  r0   //Exec o6 = Y1_0 ^ MASK3 into r9
    mov   r10, #0         //RESET
    eor   r10,  r7,  r3   //Exec Y2_0 = L19_0 ^ L28_0 ^ 1 into r10
    mov    r3, #0         //RESET
    eor    r3, r10,  r0   //Exec o5 = Y2_0 ^ MASK3 into r3
    mov    r0, #0         //RESET
    eor    r0,  r6, r14   //Exec o4 = L6_0 ^ hl21_0 into r0
    mov    r7, #0         //RESET
    eor    r7,  r5,  r4   //Exec o3 = L20_0 ^ L22_0 into r7
    mov    r4, #0         //RESET
    eor    r4, r12,  r8   //Exec Y5_0 = L25_0 ^ L29_0 into r4
    mov    r5, #0         //RESET
    ldr.w  r5, [sp, #164] //Load MASK2 into r5
    mov    r8, #0         //RESET
    eor    r8,  r4,  r5   //Exec o2 = Y5_0 ^ MASK2 into r8
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #152] //Load L13_0 into r4
    mov   r10, #0         //RESET
    eor   r10,  r4,  r2   //Exec Y6_0 = L13_0 ^ L27_0 ^ 1 into r10
    mov    r2, #0         //RESET
    eor    r2, r10,  r5   //Exec o1 = Y6_0 ^ MASK2 into r2
    mov    r4, #0         //RESET
    ldr.w  r4, [sp, #32 ] //Load L23_0 into r4
    mov    r5, #0         //RESET
    eor    r5,  r6,  r4   //Exec o0 = L6_0 ^ L23_0 ^ 1 into r5
    //[('r0', 'o4'), ('r1', 'o7'), ('r2', 'o1'), ('r3', 'o5'), ('r4', 'L23_0'), ('r5', 'o0'), ('r6', 'L6_0'), ('r7', 'o3'), ('r8', 'o2'), ('r9', 'o6'), ('r10', 'Y6_0'), ('r11', 'L24_0'), ('r12', 'L25_0'), ('r14', 'hl21_0')]
""")

def printShiftRowsFinal():
    print("""    //ShiftRows
    //Meanwhile move back to r4-r11
    //use r14 as tmp
    mov r11, #0
    mov r14, #0
    uxtb.w r11, r5
    ubfx r14, r5, #14, #2
    eor r11, r11, r14, lsl #8
    mov r14, #0
    ubfx r14, r5, #8, #6
    eor r11, r11, r14, lsl #10
    mov r14, #0
    ubfx r14, r5, #20, #4
    eor r11, r11, r14, lsl #16
    mov r14, #0
    ubfx r14, r5, #16, #4
    eor r11, r11, r14, lsl #20
    mov r14, #0
    ubfx r14, r5, #26, #6
    eor r11, r11, r14, lsl #24
    mov r14, #0
    ubfx r14, r5, #24, #2
    eor r11, r11, r14, lsl #30

    mov r10, #0
    mov r14, #0
    uxtb.w r10, r2
    ubfx r14, r2, #14, #2
    eor r10, r10, r14, lsl #8
    mov r14, #0
    ubfx r14, r2, #8, #6
    eor r10, r10, r14, lsl #10
    mov r14, #0
    ubfx r14, r2, #20, #4
    eor r10, r10, r14, lsl #16
    mov r14, #0
    ubfx r14, r2, #16, #4
    eor r10, r10, r14, lsl #20
    mov r14, #0
    ubfx r14, r2, #26, #6
    eor r10, r10, r14, lsl #24
    mov r14, #0
    ubfx r14, r2, #24, #2
    eor r10, r10, r14, lsl #30

    mov r6, #0
    mov r14, #0
    uxtb.w r6, r3
    ubfx r14, r3, #14, #2
    eor r6, r6, r14, lsl #8
    mov r14, #0
    ubfx r14, r3, #8, #6
    eor r6, r6, r14, lsl #10
    mov r14, #0
    ubfx r14, r3, #20, #4
    eor r6, r6, r14, lsl #16
    mov r14, #0
    ubfx r14, r3, #16, #4
    eor r6, r6, r14, lsl #20
    mov r14, #0
    ubfx r14, r3, #26, #6
    eor r6, r6, r14, lsl #24
    mov r14, #0
    ubfx r14, r3, #24, #2
    eor r6, r6, r14, lsl #30

    mov r4, #0
    mov r14, #0
    uxtb.w r4, r1
    ubfx r14, r1, #14, #2
    eor r4, r4, r14, lsl #8
    mov r14, #0
    ubfx r14, r1, #8, #6
    eor r4, r4, r14, lsl #10
    mov r14, #0
    ubfx r14, r1, #20, #4
    eor r4, r4, r14, lsl #16
    mov r14, #0
    ubfx r14, r1, #16, #4
    eor r4, r4, r14, lsl #20
    mov r14, #0
    ubfx r14, r1, #26, #6
    eor r4, r4, r14, lsl #24
    mov r14, #0
    ubfx r14, r1, #24, #2
    eor r4, r4, r14, lsl #30

    mov r5, #0
    mov r14, #0
    uxtb.w r5, r9
    ubfx r14, r9, #14, #2
    eor r5, r5, r14, lsl #8
    mov r14, #0
    ubfx r14, r9, #8, #6
    eor r5, r5, r14, lsl #10
    mov r14, #0
    ubfx r14, r9, #20, #4
    eor r5, r5, r14, lsl #16
    mov r14, #0
    ubfx r14, r9, #16, #4
    eor r5, r5, r14, lsl #20
    mov r14, #0
    ubfx r14, r9, #26, #6
    eor r5, r5, r14, lsl #24
    mov r14, #0
    ubfx r14, r9, #24, #2
    eor r5, r5, r14, lsl #30

    mov r9, #0
    mov r14, #0
    uxtb.w r9, r8
    ubfx r14, r8, #14, #2
    eor r9, r9, r14, lsl #8
    mov r14, #0
    ubfx r14, r8, #8, #6
    eor r9, r9, r14, lsl #10
    mov r14, #0
    ubfx r14, r8, #20, #4
    eor r9, r9, r14, lsl #16
    mov r14, #0
    ubfx r14, r8, #16, #4
    eor r9, r9, r14, lsl #20
    mov r14, #0
    ubfx r14, r8, #26, #6
    eor r9, r9, r14, lsl #24
    mov r14, #0
    ubfx r14, r8, #24, #2
    eor r9, r9, r14, lsl #30

    mov r8, #0
    mov r14, #0
    uxtb.w r8, r7
    ubfx r14, r7, #14, #2
    eor r8, r8, r14, lsl #8
    mov r14, #0
    ubfx r14, r7, #8, #6
    eor r8, r8, r14, lsl #10
    mov r14, #0
    ubfx r14, r7, #20, #4
    eor r8, r8, r14, lsl #16
    mov r14, #0
    ubfx r14, r7, #16, #4
    eor r8, r8, r14, lsl #20
    mov r14, #0
    ubfx r14, r7, #26, #6
    eor r8, r8, r14, lsl #24
    mov r14, #0
    ubfx r14, r7, #24, #2
    eor r8, r8, r14, lsl #30

    mov r7, #0
    mov r14, #0
    uxtb.w r7, r0
    ubfx r14, r0, #14, #2
    eor r7, r7, r14, lsl #8
    mov r14, #0
    ubfx r14, r0, #8, #6
    eor r7, r7, r14, lsl #10
    mov r14, #0
    ubfx r14, r0, #20, #4
    eor r7, r7, r14, lsl #16
    mov r14, #0
    ubfx r14, r0, #16, #4
    eor r7, r7, r14, lsl #20
    mov r14, #0
    ubfx r14, r0, #26, #6
    eor r7, r7, r14, lsl #24
    mov r14, #0
    ubfx r14, r0, #24, #2
    eor r7, r7, r14, lsl #30
""")

for i in range(1,rounds):
    print("    //round {:d}\n".format(i))
    printAddRoundKey(i)
    printSubBytes()
    printShiftRowsMixColumns()


# The final round
print("    //round {:d}\n".format(rounds))
printAddRoundKey(rounds-1)
printSubBytes()
printShiftRowsFinal()
printAddRoundKey(rounds)

print("""    //unmask the input data
    eor r4, r14
    eor r5, r12
    eor r6, r14
    eor r7, r12
    eor r8, r12
    eor r11, r14
    eor r9, r3
    ldr r14, =AES_bsconst //in r14, as required by encrypt_blocks
    eor r10, r3

    //r0-r3 and r14 already get overwritten by constants
    mov r12, #0

    //inverse transform of two blocks into non-bitsliced state
    ldm r14, {r1-r3}
    //r1 = 0x33333333 (but little-endian)
    //r2 = 0x55555555
    //r3 = 0x0f0f0f0f

    //0x0f0f0f0f
    eor r12, r8, r4, lsl #4
    and r12, r3
    eor r8, r12
    eor r4, r4, r12, lsr #4

    eor r12, r10, r6, lsl #4
    and r12, r3
    eor r10, r12
    eor r6, r6, r12, lsr #4

    eor r12, r11, r7, lsl #4
    and r12, r3
    eor r11, r12
    eor r7, r7, r12, lsr #4

    eor r12, r9, r5, lsl #4
    and r12, r3
    eor r9, r12
    eor r3, r5, r12, lsr #4

    //0x33333333
    eor r12, r6, r4, lsl #2
    and r12, r2
    eor r5, r6, r12
    eor r4, r4, r12, lsr #2

    eor r12, r10, r8, lsl #2
    and r12, r2
    eor r10, r12
    eor r6, r8, r12, lsr #2

    eor r12, r7, r3, lsl #2
    and r12, r2
    eor r7, r12
    eor r8, r3, r12, lsr #2

    eor r12, r11, r9, lsl #2
    and r12, r2
    eor r11, r12
    eor r2, r9, r12, lsr #2

    //0x55555555
    eor r12, r8, r4, lsl #1
    and r12, r1
    eor r8, r12
    eor r4, r4, r12, lsr #1

    eor r12, r7, r5, lsl #1
    and r12, r1
    eor r9, r7, r12
    eor r5, r5, r12, lsr #1

    eor r12, r11, r10, lsl #1
    and r12, r1
    eor r11, r12
    eor r7, r10, r12, lsr #1

    eor r12, r2, r6, lsl #1
    and r12, r1
    eor r10, r2, r12
    eor r6, r6, r12, lsr #1

    //load in
    ldr.w r0, [sp, #176]

    //load input, xor keystream and write to output
    ldmia r0!, {r1-r3,r12} //load first block input
    eor r4, r1
    eor r5, r2
    eor r6, r3
    eor r7, r12
    ldr.w r1, [sp, #180] //load out
    stmia.w r1!, {r4-r7} //write first block output

    ldmia.w r0!, {r4-r7} //load second block input
    eor r8, r4
    eor r9, r5
    eor r10, r6
    eor r11, r7
    stmia r1!, {r8-r11} //write second block output
    str r0, [sp, #176] //store in
    str r1, [sp, #180] //store out

    //load p, len, ctr
    ldr r0, [sp, #172] //p in r0, as required by encrypt_blocks
    ldr r3, [sp, #184] //len
    ldr r4, [r0, #12] //ctr

    //dec and store len counter
    subs r3, #32
    ble exit //if len<=0: exit
    str r3, [sp, #184]

    //inc and store ctr
    rev r4, r4
    add r4, #2
    rev r4, r4
    str.w r4, [r0, #12]

    //RNG_SR in r12, as expected by encrypt_blocks
    movw r12, 0x0804
    movt r12, 0x5006

    b encrypt_blocks

.align 2
exit:
    //function epilogue, restore state
    add sp, #188
    pop {r4-r12,r14}
    bx lr
""")
