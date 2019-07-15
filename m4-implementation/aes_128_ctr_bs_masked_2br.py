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
    sub.w sp, #132

    //STM32F407 specific!
    //RNG_CR = 0x50060800
    //RNG_SR = 0x50060804
    //RNG_DR = 0x50060808
    movw r12, 0x0804
    movt r12, 0x5006

.align 2
encrypt_blocks: //expect p in r0, RNG_SR in r12, AES_bsconst in r14

    //generate 1 random word
    mov.w r7, #1
    add r5, r12, #4 //RNG_DR
.align 2
generate_random:
    ldr r6, [r12]
    tst r6, r7
    beq generate_random //wait until RNG_SR == RNG_SR_DRDY
    ldr.w r6, [r5]
    //extract 2 bits to use per block, change format, and store on stack
    //............................abcd to
    //cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd and
    //abababababababababababababababab
    //a and c are the masks for one block, b and d for the other
    ubfx r4, r6, #0, #2
    orr r4, r4, r4, lsl #16
    orr r4, r4, r4, lsl #8
    orr r4, r4, r4, lsl #4
    orr r4, r4, r4, lsl #2
    ubfx r5, r6, #2, #2
    orr r5, r5, r5, lsl #16
    orr r5, r5, r5, lsl #8
    orr r5, r5, r5, lsl #4
    orr r5, r5, r5, lsl #2
    eor r6, r4, r5
    str r4, [sp, #128] //MASK1
    str r5, [sp, #124] //MASK2
    str.w r6, [sp, #120] //MASK3 = MASK1 ^ MASK2

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
    ldr r12, [sp, #128] //MASK1
    ldr r14, [sp, #124] //MASK2
    ldr.w r3, [sp, #120]  //MASK3
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
        print("""    //ldr.w r0, [sp, #116] not necessary in round 1, p.rk already in r0
    //ldr r12, [sp, #128] //MASK1
    //ldr r14, [sp, #124] //MASK2
    //ldr.w r3, [sp, #120] //MASK3
""")
    elif roundnr == rounds:
        print("""    ldr.w r0, [sp, #116] // p.rk
    ldr r12, [sp, #128] //MASK1
    ldr r14, [sp, #124] //MASK2
    ldr.w r3, [sp, #120] //MASK3
""")
    else:
        print("""    ldr.w r0, [sp, #116] // p.rk
    ldr r12, [sp, #128] //MASK1
    ldr r14, [sp, #124] //MASK2
    //ldr.w r3, [sp, #120] //MASK3 is already there from MixColumns
""")

    print("""    ldr r1, [r0], #4
    ldr r2, [r0], #4
    eor r1, r14      //mask k7
    eor r2, r12      //mask k6
    eor r1, r12      //mk7
    eor r2, r14      //mk6
""")
    if roundnr == 1 or roundnr == rounds:
        print("    eor r4, r1       //mo7")
        print("    eor r5, r2       //mo6")
    else:
        print("    eor r4, r1, r4, ror #8 //mo7")
        print("    eor r5, r2, r5, ror #8 //mo6")

    print("""    eor r4, r3       //o7
    eor r5, r3       //o6

    ldr r1, [r0], #4
    ldr r2, [r0], #4
    eor r1, r14
    eor r2, r12
    eor r1, r12
    eor r2, r14
""")

    if roundnr == 1 or roundnr == rounds:
        print("    eor r6, r1")
        print("    eor r7, r2")
    else:
        print("    eor r6, r1, r6, ror #8")
        print("    eor r7, r2, r7, ror #8")

    print("""    eor r6, r3
    eor r7, r3

    ldr r1, [r0], #4
    ldr r2, [r0], #4
    eor r1, r12
    eor r2, r3
    eor r1, r14
    eor r2, r12
""")

    if roundnr == 1 or roundnr == rounds:
        print("    eor r8, r1")
        print("    eor r9, r2")
    else:
        print("    eor r8, r1, r8, ror #8")
        print("    eor r9, r2, r9, ror #8")

    print("""    eor r8, r3
    eor r9, r14

    ldr r1, [r0], #4
    ldr r2, [r0], #4
    eor r1, r3
    eor r2, r14
    eor r1, r12
    eor r2, r12
""")

    if roundnr == 1 or roundnr == rounds:
        print("    eor r10, r1")
        print("    eor r11, r2")
    else:
        print("    eor r10, r1, r10, ror #8")
        print("    eor r11, r2, r11, ror #8")

    print("    eor r10, r14")
    print("    eor r11, r3\n")

    if roundnr < rounds:
        print("    str.w r0, [sp, #116] //must store, don't want to destroy original p.rk\n")

def printShiftRowsMixColumns():
    print("""    //ShiftRows
    //Meanwhile move to o0-o7 = r0,2,9,3,12,4,14,1 such that we're back in {r4-r11} after MixColumns
    //use r7 as tmp
    uxtb.w r2, r3
    ubfx r7, r3, #14, #2
    eor r2, r2, r7, lsl #8
    ubfx r7, r3, #8, #6
    eor r2, r2, r7, lsl #10
    ubfx r7, r3, #20, #4
    eor r2, r2, r7, lsl #16
    ubfx r7, r3, #16, #4
    eor r2, r2, r7, lsl #20
    ubfx r7, r3, #26, #6
    eor r2, r2, r7, lsl #24
    ubfx r7, r3, #24, #2
    eor r2, r2, r7, lsl #30

    uxtb.w r9, r0
    ubfx r7, r0, #14, #2
    eor r9, r9, r7, lsl #8
    ubfx r7, r0, #8, #6
    eor r9, r9, r7, lsl #10
    ubfx r7, r0, #20, #4
    eor r9, r9, r7, lsl #16
    ubfx r7, r0, #16, #4
    eor r9, r9, r7, lsl #20
    ubfx r7, r0, #26, #6
    eor r9, r9, r7, lsl #24
    ubfx r7, r0, #24, #2
    eor r9, r9, r7, lsl #30

    uxtb.w r14, r6
    ubfx r7, r6, #14, #2
    eor r14, r14, r7, lsl #8
    ubfx r7, r6, #8, #6
    eor r14, r14, r7, lsl #10
    ubfx r7, r6, #20, #4
    eor r14, r14, r7, lsl #16
    ubfx r7, r6, #16, #4
    eor r14, r14, r7, lsl #20
    ubfx r7, r6, #26, #6
    eor r14, r14, r7, lsl #24
    ubfx r7, r6, #24, #2
    eor r14, r14, r7, lsl #30

    uxtb.w r0, r5
    ubfx r7, r5, #14, #2
    eor r0, r0, r7, lsl #8
    ubfx r7, r5, #8, #6
    eor r0, r0, r7, lsl #10
    ubfx r7, r5, #20, #4
    eor r0, r0, r7, lsl #16
    ubfx r7, r5, #16, #4
    eor r0, r0, r7, lsl #20
    ubfx r7, r5, #26, #6
    eor r0, r0, r7, lsl #24
    ubfx r7, r5, #24, #2
    eor r0, r0, r7, lsl #30

    uxtb.w r3, r12
    ubfx r7, r12, #14, #2
    eor r3, r3, r7, lsl #8
    ubfx r7, r12, #8, #6
    eor r3, r3, r7, lsl #10
    ubfx r7, r12, #20, #4
    eor r3, r3, r7, lsl #16
    ubfx r7, r12, #16, #4
    eor r3, r3, r7, lsl #20
    ubfx r7, r12, #26, #6
    eor r3, r3, r7, lsl #24
    ubfx r7, r12, #24, #2
    eor r3, r3, r7, lsl #30

    uxtb.w r12, r4
    ubfx r7, r4, #14, #2
    eor r12, r12, r7, lsl #8
    ubfx r7, r4, #8, #6
    eor r12, r12, r7, lsl #10
    ubfx r7, r4, #20, #4
    eor r12, r12, r7, lsl #16
    ubfx r7, r4, #16, #4
    eor r12, r12, r7, lsl #20
    ubfx r7, r4, #26, #6
    eor r12, r12, r7, lsl #24
    ubfx r7, r4, #24, #2
    eor r12, r12, r7, lsl #30

    uxtb.w r4, r8
    ubfx r7, r8, #14, #2
    eor r4, r4, r7, lsl #8
    ubfx r7, r8, #8, #6
    eor r4, r4, r7, lsl #10
    ubfx r7, r8, #20, #4
    eor r4, r4, r7, lsl #16
    ubfx r7, r8, #16, #4
    eor r4, r4, r7, lsl #20
    ubfx r7, r8, #26, #6
    eor r4, r4, r7, lsl #24
    ubfx r7, r8, #24, #2
    eor r4, r4, r7, lsl #30

    uxtb.w r6, r1
    ubfx r7, r1, #14, #2
    eor r6, r6, r7, lsl #8
    ubfx r7, r1, #8, #6
    eor r6, r6, r7, lsl #10
    ubfx r7, r1, #20, #4
    eor r6, r6, r7, lsl #16
    ubfx r7, r1, #16, #4
    eor r6, r6, r7, lsl #20
    ubfx r7, r1, #26, #6
    eor r6, r6, r7, lsl #24
    ubfx r7, r1, #24, #2
    eor r1, r6, r7, lsl #30

    //MixColumns
    //based on Käsper-Schwabe, squeezed in 14 registers
    //x0-x7 = r0,2,9,3,12,4,14,1, t0-t7 = r11,10,(9),8,7,6,5,(4)
    ldr r5, [sp, #120] //MASK3
    ldr r6, [sp, #124] //MASK2
    eor r11, r0, r5
    eor r11, r0, r11, ror #8

    eor r10, r2, r6
    eor r10, r2, r10, ror #8

    eor r7, r9, r6
    eor r7, r9, r7, ror #8
    eor r9, r9, r10, ror #24
    eor r9, r9, r7, ror #8

    eor r8, r3, r5
    eor r8, r3, r8, ror #8
    eor r3, r3, r7, ror #24 //r7 now free, store t4 in r7

    eor r7, r12, r5
    eor r7, r12, r7, ror #8

    eor r6, r4, r5
    eor r6, r4, r6, ror #8
    eor r4, r4, r7, ror #24
    str.w r7, [sp, #112]

    eor r5, r14, r5
    eor r5, r14, r5, ror #8
    eor r14, r14, r6, ror #24
    eor r6, r4, r6, ror #8 //r4 now free, store t7 in r4

    ldr r4, [sp, #120] //MASK3
    ldr r7, [sp, #124] //MASK2
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
    ldr r7, [sp, #112]
    ldr r3, [sp, #120] //MASK3
    eor r7, r12, r7, ror #8
    eor r11, r0, r11, ror #8
    eor r10, r2, r10, ror #8

    eor r7, r7, r3
""")

def printSubBytes():
    print("""    //SubBytes
    //Result of combining a masked version of http://www.cs.yale.edu/homes/peralta/CircuitStuff/AES_SBox.txt with my custom instruction scheduler / register allocator
    //Note that the 4 last NOTs are moved to the key schedule
    //Result before manual finetuning: 61 loads and 51 stores
    orr   r0, r12, r14   //Exec M1ORM2 = MASK1 | MASK2 into r0
    eor   r2,  r7,  r9   //Exec y14 = i4 ^ i2 into r2
    str.w r0, [sp, #112] //Store r0/M1ORM2 on stack
    eor   r0,  r4, r10   //Exec y13 = i7 ^ i1 into r0
    eor   r1,  r0, r14   //Exec hy13 = y13 ^ MASK2 into r1
    eor   r3,  r4,  r7   //Exec y9 = i7 ^ i4 into r3
    str.w r3, [sp, #108] //Store r3/y9 on stack
    eor   r3,  r3, r14   //Exec hy9 = y9 ^ MASK2 into r3
    str.w r1, [sp, #104] //Store r1/hy13 on stack
    eor   r1,  r4,  r9   //Exec y8 = i7 ^ i2 into r1
    eor   r6,  r5,  r6   //Exec t0 = i6 ^ i5 into r6
    str.w r3, [sp, #100] //Store r3/hy9 on stack
    eor   r3,  r6, r11   //Exec y1 = t0 ^ i0 into r3
    str.w r6, [sp, #96 ] //Store r6/t0 on stack
    eor   r6,  r3, r14   //Exec hy1 = y1 ^ MASK2 into r6
    eor   r7,  r6,  r7   //Exec y4 = hy1 ^ i4 into r7
    str.w r7, [sp, #92 ] //Store r7/y4 on stack
    eor   r7,  r7, r12   //Exec hy4 = y4 ^ MASK1 into r7
    str.w r0, [sp, #88 ] //Store r0/y13 on stack
    eor   r0,  r0,  r2   //Exec y12 = y13 ^ y14 into r0
    str.w r6, [sp, #84 ] //Store r6/hy1 on stack
    eor   r6,  r3,  r4   //Exec y2 = y1 ^ i7 into r6
    eor  r10,  r3, r10   //Exec y5 = y1 ^ i1 into r10
    str.w r2, [sp, #80 ] //Store r2/y14 on stack
    eor   r2, r10,  r1   //Exec y3 = y5 ^ y8 into r2
    str  r10, [sp, #60 ] //Store r10/y5 on stack
    eor   r2,  r2, r14   //Exec hy3 = y3 ^ MASK2 into r2
    eor   r8,  r8,  r0   //Exec t1 = i3 ^ y12 into r8
    eor   r9,  r8,  r9   //Exec y15 = t1 ^ i2 into r9
    str.w r6, [sp, #76 ] //Store r6/y2 on stack
    eor   r6,  r9, r14   //Exec hy15 = y15 ^ MASK2 into r6
    eor   r5,  r8,  r5   //Exec y20 = t1 ^ i6 into r5
    eor   r8,  r9, r11   //Exec y6 = y15 ^ i0 into r8
    str.w r6, [sp, #72 ] //Store r6/hy15 on stack
    eor   r6,  r8, r12   //Exec hy6 = y6 ^ MASK1 into r6
    str.w r6, [sp, #68 ] //Store r6/hy6 on stack
    ldr.w r6, [sp, #96 ] //Load t0 into r6
    str.w r3, [sp, #64 ] //Store r3/y1 on stack
    eor   r3,  r9,  r6   //Exec y10 = y15 ^ t0 into r3
    eor  r10,  r3, r12   //Exec hy10 = y10 ^ MASK1 into r10
    str  r10, [sp, #56 ] //Store r10/hy10 on stack
    ldr  r10, [sp, #100] //Load hy9 into r10
    str.w r5, [sp, #100] //Store r5/y20 on stack
    eor  r10,  r5, r10   //Exec y11 = y20 ^ hy9 into r10
    eor   r5, r10, r12   //Exec hy11 = y11 ^ MASK1 into r5
    eor  r14, r11,  r5   //Exec y7 = i0 ^ hy11 into r14
    eor   r5,  r3,  r5   //Exec y17 = y10 ^ hy11 into r5
    str.w r1, [sp, #52 ] //Store r1/y8 on stack
    eor   r1,  r3,  r1   //Exec y19 = y10 ^ y8 into r1
    str.w r1, [sp, #96 ] //Store r1/y19 on stack
    eor   r6,  r6, r10   //Exec y16 = t0 ^ y11 into r6
    ldr.w r1, [sp, #104] //Load hy13 into r1
    str.w r3, [sp, #48 ] //Store r3/y10 on stack
    eor   r3,  r1,  r6   //Exec y21 = hy13 ^ y16 into r3
    str.w r3, [sp, #32 ] //Store r3/y21 on stack
    eor   r4,  r4,  r6   //Exec y18 = i7 ^ y16 into r4
    str.w r4, [sp, #44 ] //Store r4/y18 on stack
    and   r4,  r0,  r9   //Exec t2_0 = y12 & y15 into r4
    str.w r0, [sp, #40 ] //Store r0/y12 on stack
    and   r0,  r0, r12   //Exec t2_1 = y12 & MASK1 into r0
    str.w r0, [sp, #36 ] //Store r0/t2_1 on stack
    eor   r0,  r0, r12   //Exec t2_2 = t2_1 ^ MASK1 into r0
    eor   r0,  r4,  r0   //Exec t2_3 = t2_0 ^ t2_2 into r0
    ldr.w r4, [sp, #120] //Load MASK3 into r4
    ldr.w r3, [sp, #112] //Load M1ORM2 into r3
    and   r9,  r4,  r9   //Exec t2_4 = MASK3 & y15 into r9
    eor   r9,  r9,  r3   //Exec t2_5 = t2_4 ^ M1ORM2 into r9
    eor   r0,  r0,  r9   //Exec t2 = t2_3 ^ t2_5 into r0
    and   r9,  r2,  r8   //Exec t3_0 = hy3 & y6 into r9
    str.w r2, [sp, #28 ] //Store r2/hy3 on stack
    and   r2,  r2,  r4   //Exec t3_1 = hy3 & MASK3 into r2
    str.w r2, [sp, #24 ] //Store r2/t3_1 on stack
    eor   r2,  r2,  r4   //Exec t3_2 = t3_1 ^ MASK3 into r2
    eor   r2,  r9,  r2   //Exec t3_3 = t3_0 ^ t3_2 into r2
    and   r8, r12,  r8   //Exec t3_4 = MASK1 & y6 into r8
    eor   r8,  r8,  r3   //Exec t3_5 = t3_4 ^ M1ORM2 into r8
    eor   r2,  r2,  r8   //Exec t3 = t3_3 ^ t3_5 into r2
    eor   r2,  r2,  r0   //Exec t4 = t3 ^ t2 into r2
    and   r8, r11,  r7   //Exec t5_0 = i0 & hy4 into r8
    and   r9, r11,  r4   //Exec t5_1 = i0 & MASK3 into r9
    str   r9, [sp, #20 ] //Store r9/t5_1 on stack
    eor   r9,  r9,  r4   //Exec t5_2 = t5_1 ^ MASK3 into r9
    eor   r8,  r8,  r9   //Exec t5_3 = t5_0 ^ t5_2 into r8
    ldr   r9, [sp, #124] //Load MASK2 into r9
    and   r7,  r9,  r7   //Exec t5_4 = MASK2 & hy4 into r7
    eor   r7,  r7,  r3   //Exec t5_5 = t5_4 ^ M1ORM2 into r7
    eor   r7,  r8,  r7   //Exec t5 = t5_3 ^ t5_5 into r7
    eor   r0,  r7,  r0   //Exec t6 = t5 ^ t2 into r0
    and   r7,  r1,  r6   //Exec t7_0 = hy13 & y16 into r7
    and   r1,  r1, r12   //Exec t7_1 = hy13 & MASK1 into r1
    eor   r1,  r1, r12   //Exec t7_2 = t7_1 ^ MASK1 into r1
    eor   r1,  r7,  r1   //Exec t7_3 = t7_0 ^ t7_2 into r1
    and   r7,  r6,  r4   //Exec t7_4 = y16 & MASK3 into r7
    eor   r8,  r7,  r3   //Exec t7_5 = t7_4 ^ M1ORM2 into r8
    str.w r7, [sp, #104] //Store r7/t7_4 on stack
    eor   r1,  r1,  r8   //Exec t7 = t7_3 ^ t7_5 into r1
    ldr   r8, [sp, #64 ] //Load y1 into r8
    ldr.w r7, [sp, #60 ] //Load y5 into r7
    str.w r6, [sp, #16 ] //Store r6/y16 on stack
    and   r6,  r8,  r7   //Exec t8_0 = y1 & y5 into r6
    and   r8,  r8,  r9   //Exec t8_1 = y1 & MASK2 into r8
    eor   r8,  r8,  r9   //Exec t8_2 = t8_1 ^ MASK2 into r8
    eor   r6,  r6,  r8   //Exec t8_3 = t8_0 ^ t8_2 into r6
    and   r8,  r7, r12   //Exec t8_4 = y5 & MASK1 into r8
    str   r8, [sp, #64 ] //Store r8/t8_4 on stack
    eor   r8,  r8,  r3   //Exec t8_5 = t8_4 ^ M1ORM2 into r8
    eor   r6,  r6,  r8   //Exec t8 = t8_3 ^ t8_5 into r6
    ldr   r8, [sp, #76 ] //Load y2 into r8
    str  r14, [sp, #12 ] //Store r14/y7 on stack
    eor   r6,  r6,  r1   //Exec t9 = t8 ^ t7 into r6
    and   r7, r14,  r8   //Exec t10_0 = y7 & y2 into r7
    and  r14, r14,  r4   //Exec t10_1 = y7 & MASK3 into r14
    eor  r14, r14,  r4   //Exec t10_2 = t10_1 ^ MASK3 into r14
    eor   r7,  r7, r14   //Exec t10_3 = t10_0 ^ t10_2 into r7
    and  r14, r12,  r8   //Exec t10_4 = MASK1 & y2 into r14
    eor  r14, r14,  r3   //Exec t10_5 = t10_4 ^ M1ORM2 into r14
    eor   r7,  r7, r14   //Exec t10 = t10_3 ^ t10_5 into r7
    eor   r1,  r7,  r1   //Exec t11 = t10 ^ t7 into r1
    ldr.w r7, [sp, #108] //Load y9 into r7
    and  r14, r10,  r7   //Exec t12_0 = y11 & y9 into r14
    and   r8, r10,  r4   //Exec t12_1 = y11 & MASK3 into r8
    eor   r8,  r8,  r4   //Exec t12_2 = t12_1 ^ MASK3 into r8
    eor   r8, r14,  r8   //Exec t12_3 = t12_0 ^ t12_2 into r8
    and  r14,  r9,  r7   //Exec t12_4 = MASK2 & y9 into r14
    eor  r14, r14,  r3   //Exec t12_5 = t12_4 ^ M1ORM2 into r14
    eor   r8,  r8, r14   //Exec t12 = t12_3 ^ t12_5 into r8
    ldr  r14, [sp, #80 ] //Load y14 into r14
    str.w r5, [sp, #8  ] //Store r5/y17 on stack
    and   r7,  r5, r14   //Exec t13_0 = y17 & y14 into r7
    and   r5,  r5,  r9   //Exec t13_1 = y17 & MASK2 into r5
    eor   r5,  r5,  r9   //Exec t13_2 = t13_1 ^ MASK2 into r5
    eor   r5,  r7,  r5   //Exec t13_3 = t13_0 ^ t13_2 into r5
    and   r7, r12, r14   //Exec t13_4 = MASK1 & y14 into r7
    eor   r7,  r7,  r3   //Exec t13_5 = t13_4 ^ M1ORM2 into r7
    eor   r5,  r5,  r7   //Exec t13 = t13_3 ^ t13_5 into r5
    eor   r5,  r5,  r8   //Exec t14 = t13 ^ t12 into r5
    ldr.w r7, [sp, #52 ] //Load y8 into r7
    ldr  r14, [sp, #48 ] //Load y10 into r14
    str  r10, [sp, #4  ] //Store r10/y11 on stack
    and  r10,  r7, r14   //Exec t15_0 = y8 & y10 into r10
    and   r7,  r7,  r9   //Exec t15_1 = y8 & MASK2 into r7
    str.w r7, [sp, #0  ] //Store r7/t15_1 on stack
    eor   r7,  r7,  r9   //Exec t15_2 = t15_1 ^ MASK2 into r7
    eor   r7, r10,  r7   //Exec t15_3 = t15_0 ^ t15_2 into r7
    and  r10, r12, r14   //Exec t15_4 = MASK1 & y10 into r10
    eor  r10, r10,  r3   //Exec t15_5 = t15_4 ^ M1ORM2 into r10
    eor   r7,  r7, r10   //Exec t15 = t15_3 ^ t15_5 into r7
    eor   r7,  r7,  r8   //Exec t16 = t15 ^ t12 into r7
    ldr   r8, [sp, #100] //Load y20 into r8
    eor   r2,  r2,  r8   //Exec t17 = t4 ^ y20 into r2
    eor   r0,  r0,  r7   //Exec t18 = t6 ^ t16 into r0
    eor   r6,  r6,  r5   //Exec t19 = t9 ^ t14 into r6
    eor   r1,  r1,  r7   //Exec t20 = t11 ^ t16 into r1
    eor   r2,  r2,  r5   //Exec t21 = t17 ^ t14 into r2
    ldr.w r5, [sp, #96 ] //Load y19 into r5
    eor   r0,  r0,  r5   //Exec t22 = t18 ^ y19 into r0
    ldr.w r5, [sp, #32 ] //Load y21 into r5
    ldr.w r7, [sp, #44 ] //Load y18 into r7
    str  r11, [sp, #100] //Store r11/i0 on stack
    eor   r5,  r6,  r5   //Exec t23 = t19 ^ y21 into r5
    eor   r6,  r5, r12   //Exec ht23 = t23 ^ MASK1 into r6
    eor   r1,  r1,  r7   //Exec t24 = t20 ^ y18 into r1
    eor   r7,  r1, r12   //Exec ht24 = t24 ^ MASK1 into r7
    eor   r8,  r2,  r0   //Exec t25 = t21 ^ t22 into r8
    and  r10,  r5,  r2   //Exec t26_0 = t23 & t21 into r10
    and  r14,  r5,  r9   //Exec t26_1 = t23 & MASK2 into r14
    eor  r14, r14,  r9   //Exec t26_2 = t26_1 ^ MASK2 into r14
    eor  r10, r10, r14   //Exec t26_3 = t26_0 ^ t26_2 into r10
    and   r2,  r4,  r2   //Exec t26_4 = MASK3 & t21 into r2
    eor   r2,  r2,  r3   //Exec t26_5 = t26_4 ^ M1ORM2 into r2
    eor   r2, r10,  r2   //Exec t26 = t26_3 ^ t26_5 into r2
    eor  r10,  r1,  r2   //Exec t27 = t24 ^ t26 into r10
    and  r14,  r8, r10   //Exec t28_0 = t25 & t27 into r14
    and  r11,  r8, r12   //Exec t28_1 = t25 & MASK1 into r11
    eor  r11, r11, r12   //Exec t28_2 = t28_1 ^ MASK1 into r11
    eor  r11, r14, r11   //Exec t28_3 = t28_0 ^ t28_2 into r11
    and  r14,  r4, r10   //Exec t28_4 = MASK3 & t27 into r14
    eor  r14, r14,  r3   //Exec t28_5 = t28_4 ^ M1ORM2 into r14
    eor  r11, r11, r14   //Exec t28 = t28_3 ^ t28_5 into r11
    eor  r11, r11,  r0   //Exec t29 = t28 ^ t22 into r11
    eor   r5,  r5,  r1   //Exec t30 = t23 ^ t24 into r5
    eor   r0,  r0,  r2   //Exec t31 = t22 ^ t26 into r0
    and   r2,  r5,  r0   //Exec t32_0 = t30 & t31 into r2
    and   r5,  r5,  r9   //Exec t32_1 = t30 & MASK2 into r5
    eor   r5,  r5,  r9   //Exec t32_2 = t32_1 ^ MASK2 into r5
    eor   r2,  r2,  r5   //Exec t32_3 = t32_0 ^ t32_2 into r2
    and   r0, r12,  r0   //Exec t32_4 = MASK1 & t31 into r0
    eor   r0,  r0,  r3   //Exec t32_5 = t32_4 ^ M1ORM2 into r0
    eor   r0,  r2,  r0   //Exec t32 = t32_3 ^ t32_5 into r0
    eor   r0,  r0,  r1   //Exec t33 = t32 ^ t24 into r0
    eor   r1,  r0, r12   //Exec ht33 = t33 ^ MASK1 into r1
    eor   r2,  r6,  r0   //Exec t34 = ht23 ^ t33 into r2
    eor   r5, r10,  r0   //Exec t35 = t27 ^ t33 into r5
    and   r6,  r5,  r7   //Exec t36_0 = t35 & ht24 into r6
    and   r5,  r5,  r4   //Exec t36_1 = t35 & MASK3 into r5
    eor   r5,  r5,  r4   //Exec t36_2 = t36_1 ^ MASK3 into r5
    eor   r5,  r6,  r5   //Exec t36_3 = t36_0 ^ t36_2 into r5
    and   r6,  r9,  r7   //Exec t36_4 = MASK2 & ht24 into r6
    eor   r6,  r6,  r3   //Exec t36_5 = t36_4 ^ M1ORM2 into r6
    eor   r5,  r5,  r6   //Exec t36 = t36_3 ^ t36_5 into r5
    eor   r2,  r5,  r2   //Exec t37 = t36 ^ t34 into r2
    eor   r5, r10,  r5   //Exec t38 = t27 ^ t36 into r5
    and   r6, r11,  r5   //Exec t39_0 = t29 & t38 into r6
    and   r7, r11,  r4   //Exec t39_1 = t29 & MASK3 into r7
    eor   r7,  r7,  r4   //Exec t39_2 = t39_1 ^ MASK3 into r7
    eor   r6,  r6,  r7   //Exec t39_3 = t39_0 ^ t39_2 into r6
    str.w r7, [sp, #96 ] //Store r7/t39_2 on stack
    and   r5,  r9,  r5   //Exec t39_4 = MASK2 & t38 into r5
    eor   r5,  r5,  r3   //Exec t39_5 = t39_4 ^ M1ORM2 into r5
    eor   r5,  r6,  r5   //Exec t39 = t39_3 ^ t39_5 into r5
    eor   r5,  r8,  r5   //Exec t40 = t25 ^ t39 into r5
    eor   r6,  r5,  r2   //Exec t41 = t40 ^ t37 into r6
    eor   r8, r11,  r0   //Exec t42 = t29 ^ t33 into r8
    eor  r10, r11,  r5   //Exec t43 = t29 ^ t40 into r10
    eor   r1,  r1,  r2   //Exec t44 = ht33 ^ t37 into r1
    eor  r14,  r8,  r6   //Exec t45 = t42 ^ t41 into r14
    ldr.w r7, [sp, #72 ] //Load hy15 into r7
    str.w r6, [sp, #48 ] //Store r6/t41 on stack
    and   r6,  r1,  r7   //Exec z0_0 = t44 & hy15 into r6
    str.w r1, [sp, #44 ] //Store r1/t44 on stack
    and   r1,  r1,  r4   //Exec z0_1 = t44 & MASK3 into r1
    eor   r1,  r1,  r4   //Exec z0_2 = z0_1 ^ MASK3 into r1
    eor   r6,  r6,  r1   //Exec z0_3 = z0_0 ^ z0_2 into r6
    and   r7, r12,  r7   //Exec z0_4 = MASK1 & hy15 into r7
    eor   r7,  r7,  r3   //Exec z0_5 = z0_4 ^ M1ORM2 into r7
    eor   r6,  r6,  r7   //Exec z0 = z0_3 ^ z0_5 into r6
    ldr.w r7, [sp, #68 ] //Load hy6 into r7
    str.w r6, [sp, #72 ] //Store r6/z0 on stack
    and   r6,  r7,  r2   //Exec z1_0 = hy6 & t37 into r6
    and   r7,  r7,  r4   //Exec z1_1 = hy6 & MASK3 into r7
    eor   r7,  r7,  r4   //Exec z1_2 = z1_1 ^ MASK3 into r7
    eor   r6,  r6,  r7   //Exec z1_3 = z1_0 ^ z1_2 into r6
    and   r7,  r9,  r2   //Exec z1_4 = MASK2 & t37 into r7
    eor   r7,  r7,  r3   //Exec z1_5 = z1_4 ^ M1ORM2 into r7
    eor   r6,  r6,  r7   //Exec z1 = z1_3 ^ z1_5 into r6
    ldr.w r7, [sp, #100] //Load i0 into r7
    str.w r6, [sp, #100] //Store r6/z1 on stack
    and   r7,  r0,  r7   //Exec z2_0 = t33 & i0 into r7
    and   r6,  r0,  r9   //Exec z2_1 = t33 & MASK2 into r6
    eor   r6,  r6,  r9   //Exec z2_2 = z2_1 ^ MASK2 into r6
    str.w r6, [sp, #68 ] //Store r6/z2_2 on stack
    eor   r7,  r7,  r6   //Exec z2_3 = z2_0 ^ z2_2 into r7
    ldr.w r6, [sp, #20 ] //Load t5_1 into r6
    eor   r6,  r6,  r3   //Exec z2_5 = t5_1 ^ M1ORM2 into r6
    eor   r6,  r7,  r6   //Exec z2 = z2_3 ^ z2_5 into r6
    str.w r6, [sp, #32 ] //Store r6/z2 on stack
    ldr.w r7, [sp, #16 ] //Load y16 into r7
    ldr.w r6, [sp, #104] //Load t7_4 into r6
    and   r7,  r7, r10   //Exec z3_0 = y16 & t43 into r7
    eor   r6,  r6,  r4   //Exec z3_2 = t7_4 ^ MASK3 into r6
    eor   r6,  r7,  r6   //Exec z3_3 = z3_0 ^ z3_2 into r6
    and   r7, r12, r10   //Exec z3_4 = MASK1 & t43 into r7
    str.w r7, [sp, #104] //Store r7/z3_4 on stack
    eor   r7,  r7,  r3   //Exec z3_5 = z3_4 ^ M1ORM2 into r7
    eor   r6,  r6,  r7   //Exec z3 = z3_3 ^ z3_5 into r6
    ldr.w r7, [sp, #84 ] //Load hy1 into r7
    str.w r6, [sp, #20 ] //Store r6/z3 on stack
    and   r6,  r7,  r5   //Exec z4_0 = hy1 & t40 into r6
    and   r7,  r7, r12   //Exec z4_1 = hy1 & MASK1 into r7
    eor   r7,  r7, r12   //Exec z4_2 = z4_1 ^ MASK1 into r7
    eor   r6,  r6,  r7   //Exec z4_3 = z4_0 ^ z4_2 into r6
    and   r7,  r4,  r5   //Exec z4_4 = MASK3 & t40 into r7
    eor   r7,  r7,  r3   //Exec z4_5 = z4_4 ^ M1ORM2 into r7
    eor   r6,  r6,  r7   //Exec z4 = z4_3 ^ z4_5 into r6
    ldr.w r7, [sp, #12 ] //Load y7 into r7
    str.w r6, [sp, #84 ] //Store r6/z4 on stack
    and   r6, r11,  r7   //Exec z5_0 = t29 & y7 into r6
    str  r11, [sp, #16 ] //Store r11/t29 on stack
    and  r11, r11, r12   //Exec z5_1 = t29 & MASK1 into r11
    eor  r11, r11, r12   //Exec z5_2 = z5_1 ^ MASK1 into r11
    eor   r6,  r6, r11   //Exec z5_3 = z5_0 ^ z5_2 into r6
    and   r7,  r9,  r7   //Exec z5_4 = MASK2 & y7 into r7
    eor   r7,  r7,  r3   //Exec z5_5 = z5_4 ^ M1ORM2 into r7
    eor   r6,  r6,  r7   //Exec z5 = z5_3 ^ z5_5 into r6
    ldr.w r7, [sp, #4  ] //Load y11 into r7
    and  r11,  r7,  r8   //Exec z6_0 = y11 & t42 into r11
    and   r7,  r7, r12   //Exec z6_1 = y11 & MASK1 into r7
    eor   r7,  r7, r12   //Exec z6_2 = z6_1 ^ MASK1 into r7
    eor   r7, r11,  r7   //Exec z6_3 = z6_0 ^ z6_2 into r7
    and  r11,  r9,  r8   //Exec z6_4 = MASK2 & t42 into r11
    eor  r11, r11,  r3   //Exec z6_5 = z6_4 ^ M1ORM2 into r11
    eor   r7,  r7, r11   //Exec z6 = z6_3 ^ z6_5 into r7
    ldr  r11, [sp, #8  ] //Load y17 into r11
    str.w r7, [sp, #12 ] //Store r7/z6 on stack
    and   r7, r11, r14   //Exec z7_0 = y17 & t45 into r7
    and  r11, r11,  r4   //Exec z7_1 = y17 & MASK3 into r11
    eor  r11, r11,  r4   //Exec z7_2 = z7_1 ^ MASK3 into r11
    eor   r7,  r7, r11   //Exec z7_3 = z7_0 ^ z7_2 into r7
    and  r11, r12, r14   //Exec z7_4 = MASK1 & t45 into r11
    eor  r11, r11,  r3   //Exec z7_5 = z7_4 ^ M1ORM2 into r11
    eor   r7,  r7, r11   //Exec z7 = z7_3 ^ z7_5 into r7
    ldr  r11, [sp, #56 ] //Load hy10 into r11
    str.w r6, [sp, #8  ] //Store r6/z5 on stack
    eor   r6,  r5,  r2   //Recompute t41 = t40 ^ t37 into r6
    str.w r7, [sp, #4  ] //Store r7/z7 on stack
    and   r7, r11,  r6   //Exec z8_0 = hy10 & t41 into r7
    and  r11, r11,  r9   //Exec z8_1 = hy10 & MASK2 into r11
    eor  r11, r11,  r9   //Exec z8_2 = z8_1 ^ MASK2 into r11
    eor   r7,  r7, r11   //Exec z8_3 = z8_0 ^ z8_2 into r7
    and  r11,  r4,  r6   //Exec z8_4 = MASK3 & t41 into r11
    eor  r11, r11,  r3   //Exec z8_5 = z8_4 ^ M1ORM2 into r11
    eor   r7,  r7, r11   //Exec z8 = z8_3 ^ z8_5 into r7
    str.w r7, [sp, #56 ] //Store r7/z8 on stack
    ldr  r11, [sp, #44 ] //Load t44 into r11
    ldr.w r7, [sp, #40 ] //Load y12 into r7
    and   r7, r11,  r7   //Exec z9_0 = t44 & y12 into r7
    eor   r1,  r7,  r1   //Exec z9_3 = z9_0 ^ z0_2 into r1
    ldr.w r7, [sp, #36 ] //Load t2_1 into r7
    eor   r7,  r7,  r3   //Exec z9_5 = t2_1 ^ M1ORM2 into r7
    eor   r1,  r1,  r7   //Exec z9 = z9_3 ^ z9_5 into r1
    ldr.w r7, [sp, #28 ] //Load hy3 into r7
    and   r7,  r2,  r7   //Exec z10_0 = t37 & hy3 into r7
    and   r2,  r2, r12   //Exec z10_1 = t37 & MASK1 into r2
    eor   r2,  r2, r12   //Exec z10_2 = z10_1 ^ MASK1 into r2
    eor   r2,  r7,  r2   //Exec z10_3 = z10_0 ^ z10_2 into r2
    ldr.w r7, [sp, #24 ] //Load t3_1 into r7
    eor   r7,  r7,  r3   //Exec z10_5 = t3_1 ^ M1ORM2 into r7
    eor   r2,  r2,  r7   //Exec z10 = z10_3 ^ z10_5 into r2
    ldr.w r7, [sp, #92 ] //Load y4 into r7
    ldr  r11, [sp, #68 ] //Load z2_2 into r11
    and   r0,  r0,  r7   //Exec z11_0 = t33 & y4 into r0
    eor   r0,  r0, r11   //Exec z11_3 = z11_0 ^ z2_2 into r0
    and   r7,  r4,  r7   //Exec z11_4 = MASK3 & y4 into r7
    eor   r7,  r7,  r3   //Exec z11_5 = z11_4 ^ M1ORM2 into r7
    eor   r0,  r0,  r7   //Exec z11 = z11_3 ^ z11_5 into r0
    ldr.w r7, [sp, #88 ] //Load y13 into r7
    ldr  r11, [sp, #104] //Load z3_4 into r11
    and  r10, r10,  r7   //Exec z12_0 = t43 & y13 into r10
    eor  r11, r11, r12   //Exec z12_2 = z3_4 ^ MASK1 into r11
    eor  r10, r10, r11   //Exec z12_3 = z12_0 ^ z12_2 into r10
    and   r7,  r4,  r7   //Exec z12_4 = MASK3 & y13 into r7
    eor   r7,  r7,  r3   //Exec z12_5 = z12_4 ^ M1ORM2 into r7
    eor   r7, r10,  r7   //Exec z12 = z12_3 ^ z12_5 into r7
    ldr  r10, [sp, #60 ] //Load y5 into r10
    ldr  r11, [sp, #64 ] //Load t8_4 into r11
    str.w r0, [sp, #104] //Store r0/z11 on stack
    and  r10, r10,  r5   //Exec z13_0 = y5 & t40 into r10
    eor  r11, r11, r12   //Exec z13_2 = t8_4 ^ MASK1 into r11
    eor  r10, r10, r11   //Exec z13_3 = z13_0 ^ z13_2 into r10
    and   r5,  r9,  r5   //Exec z13_4 = MASK2 & t40 into r5
    eor   r5,  r5,  r3   //Exec z13_5 = z13_4 ^ M1ORM2 into r5
    eor   r5, r10,  r5   //Exec z13 = z13_3 ^ z13_5 into r5
    ldr  r10, [sp, #16 ] //Load t29 into r10
    ldr  r11, [sp, #76 ] //Load y2 into r11
    ldr.w r0, [sp, #96 ] //Load t39_2 into r0
    and  r10, r10, r11   //Exec z14_0 = t29 & y2 into r10
    eor   r0, r10,  r0   //Exec z14_3 = z14_0 ^ t39_2 into r0
    and  r10,  r9, r11   //Exec z14_4 = MASK2 & y2 into r10
    eor  r10, r10,  r3   //Exec z14_5 = z14_4 ^ M1ORM2 into r10
    eor   r0,  r0, r10   //Exec z14 = z14_3 ^ z14_5 into r0
    ldr  r10, [sp, #108] //Load y9 into r10
    and  r11, r10,  r8   //Exec z15_0 = y9 & t42 into r11
    and  r10, r10, r12   //Exec z15_1 = y9 & MASK1 into r10
    eor  r10, r10, r12   //Exec z15_2 = z15_1 ^ MASK1 into r10
    eor  r10, r11, r10   //Exec z15_3 = z15_0 ^ z15_2 into r10
    and   r8,  r4,  r8   //Exec z15_4 = MASK3 & t42 into r8
    eor   r8,  r8,  r3   //Exec z15_5 = z15_4 ^ M1ORM2 into r8
    eor   r8, r10,  r8   //Exec z15 = z15_3 ^ z15_5 into r8
    ldr  r10, [sp, #80 ] //Load y14 into r10
    and  r11, r10, r14   //Exec z16_0 = y14 & t45 into r11
    and  r10, r10,  r4   //Exec z16_1 = y14 & MASK3 into r10
    eor  r10, r10,  r4   //Exec z16_2 = z16_1 ^ MASK3 into r10
    eor  r10, r11, r10   //Exec z16_3 = z16_0 ^ z16_2 into r10
    and  r11,  r9, r14   //Exec z16_4 = MASK2 & t45 into r11
    eor  r11, r11,  r3   //Exec z16_5 = z16_4 ^ M1ORM2 into r11
    eor  r10, r10, r11   //Exec z16 = z16_3 ^ z16_5 into r10
    ldr  r11, [sp, #52 ] //Load y8 into r11
    and  r11,  r6, r11   //Exec z17_0 = t41 & y8 into r11
    and   r6,  r6, r12   //Exec z17_1 = t41 & MASK1 into r6
    eor   r6,  r6, r12   //Exec z17_2 = z17_1 ^ MASK1 into r6
    eor   r6, r11,  r6   //Exec z17_3 = z17_0 ^ z17_2 into r6
    ldr  r11, [sp, #0  ] //Load t15_1 into r11
    eor   r3, r11,  r3   //Exec z17_5 = t15_1 ^ M1ORM2 into r3
    eor   r3,  r6,  r3   //Exec z17 = z17_3 ^ z17_5 into r3
    eor   r6,  r8, r10   //Exec tc1 = z15 ^ z16 into r6
    eor   r2,  r2,  r6   //Exec tc2 = z10 ^ tc1 into r2
    eor   r1,  r1,  r2   //Exec tc3 = z9 ^ tc2 into r1
    ldr  r10, [sp, #72 ] //Load z0 into r10
    ldr  r11, [sp, #32 ] //Load z2 into r11
    ldr  r14, [sp, #100] //Load z1 into r14
    str.w r3, [sp, #112] //Store r3/z17 on stack
    eor  r11, r10, r11   //Exec tc4 = z0 ^ z2 into r11
    eor  r10, r14, r10   //Exec tc5 = z1 ^ z0 into r10
    ldr  r14, [sp, #20 ] //Load z3 into r14
    ldr.w r4, [sp, #84 ] //Load z4 into r4
    ldr   r9, [sp, #4  ] //Load z7 into r9
    ldr.w r3, [sp, #56 ] //Load z8 into r3
    eor   r4, r14,  r4   //Exec tc6 = z3 ^ z4 into r4
    eor  r12,  r7, r11   //Exec tc7 = z12 ^ tc4 into r12
    eor   r9,  r9,  r4   //Exec tc8 = z7 ^ tc6 into r9
    eor   r3,  r3, r12   //Exec tc9 = z8 ^ tc7 into r3
    eor   r3,  r9,  r3   //Exec tc10 = tc8 ^ tc9 into r3
    eor   r4,  r4, r10   //Exec tc11 = tc6 ^ tc5 into r4
    ldr  r10, [sp, #8  ] //Load z5 into r10
    eor  r10, r14, r10   //Exec tc12 = z3 ^ z5 into r10
    eor   r5,  r5,  r6   //Exec tc13 = z13 ^ tc1 into r5
    eor   r6, r11, r10   //Exec tc14 = tc4 ^ tc12 into r6
    eor   r4,  r1,  r4   //Exec S3 = tc3 ^ tc11 into r4
    ldr  r10, [sp, #12 ] //Load z6 into r10
    eor   r9, r10,  r9   //Exec tc16 = z6 ^ tc8 into r9
    eor   r0,  r0,  r3   //Exec tc17 = z14 ^ tc10 into r0
    eor   r5,  r5,  r6   //Exec tc18 = tc13 ^ tc14 into r5
    eor   r7,  r7,  r5   //Exec S7 = z12 ^ tc18 ^ 1 into r7
    eor   r8,  r8,  r9   //Exec tc20 = z15 ^ tc16 into r8
    ldr  r10, [sp, #104] //Load z11 into r10
    eor   r2,  r2, r10   //Exec tc21 = tc2 ^ z11 into r2
    eor   r1,  r1,  r9   //Exec o7 = tc3 ^ tc16 into r1
    eor   r3,  r3,  r5   //Exec o1 = tc10 ^ tc18 ^ 1 into r3
    eor   r5,  r6,  r4   //Exec S4 = tc14 ^ S3 into r5
    eor   r6,  r4,  r9   //Exec S1 = S3 ^ tc16 ^ 1 into r6
    ldr   r9, [sp, #112] //Load z17 into r9
    eor   r8,  r0,  r8   //Exec tc26 = tc17 ^ tc20 into r8
    eor   r8,  r8,  r9   //Exec S2 = tc26 ^ z17 ^ 1 into r8
    eor   r0,  r2,  r0   //Exec S5 = tc21 ^ tc17 into r0
    ldr.w r2, [sp, #124] //Load MASK2 into r2
    ldr   r9, [sp, #128] //Load MASK1 into r9
    ldr  r10, [sp, #120] //Load MASK3 into r10
    eor   r6,  r6,  r2   //Exec o6 = S1 ^ MASK2 into r6
    eor   r8,  r8,  r9   //Exec o5 = S2 ^ MASK1 into r8
    eor   r4,  r4, r10   //Exec o4 = S3 ^ MASK3 into r4
    eor  r12,  r5,  r2   //Exec o3 = S4 ^ MASK2 into r12
    eor   r0,  r0,  r9   //Exec o2 = S5 ^ MASK1 into r0
    eor   r5,  r7, r10   //Exec o0 = S7 ^ MASK3 into r5
    //[('r0', 'o2'), ('r1', 'o7'), ('r2', 'MASK2'), ('r3', 'o1'), ('r4', 'o4'), ('r5', 'o0'), ('r6', 'o6'), ('r7', 'S7'), ('r8', 'o5'), ('r9', 'MASK1'), ('r10', 'MASK3'), ('r11', 'tc4'), ('r12', 'o3'), ('r14', 'z3')]
""")

def printShiftRowsFinal():
    print("""    //ShiftRows
    //Meanwhile move back to r4-r11
    //use r14 as tmp
    uxtb.w r7, r4
    ubfx r14, r4, #14, #2
    eor r7, r7, r14, lsl #8
    ubfx r14, r4, #8, #6
    eor r7, r7, r14, lsl #10
    ubfx r14, r4, #20, #4
    eor r7, r7, r14, lsl #16
    ubfx r14, r4, #16, #4
    eor r7, r7, r14, lsl #20
    ubfx r14, r4, #26, #6
    eor r7, r7, r14, lsl #24
    ubfx r14, r4, #24, #2
    eor r7, r7, r14, lsl #30

    uxtb.w r9, r0
    ubfx r14, r0, #14, #2
    eor r9, r9, r14, lsl #8
    ubfx r14, r0, #8, #6
    eor r9, r9, r14, lsl #10
    ubfx r14, r0, #20, #4
    eor r9, r9, r14, lsl #16
    ubfx r14, r0, #16, #4
    eor r9, r9, r14, lsl #20
    ubfx r14, r0, #26, #6
    eor r9, r9, r14, lsl #24
    ubfx r14, r0, #24, #2
    eor r9, r9, r14, lsl #30

    uxtb.w r10, r3
    ubfx r14, r3, #14, #2
    eor r10, r10, r14, lsl #8
    ubfx r14, r3, #8, #6
    eor r10, r10, r14, lsl #10
    ubfx r14, r3, #20, #4
    eor r10, r10, r14, lsl #16
    ubfx r14, r3, #16, #4
    eor r10, r10, r14, lsl #20
    ubfx r14, r3, #26, #6
    eor r10, r10, r14, lsl #24
    ubfx r14, r3, #24, #2
    eor r10, r10, r14, lsl #30

    uxtb.w r11, r5
    ubfx r14, r5, #14, #2
    eor r11, r11, r14, lsl #8
    ubfx r14, r5, #8, #6
    eor r11, r11, r14, lsl #10
    ubfx r14, r5, #20, #4
    eor r11, r11, r14, lsl #16
    ubfx r14, r5, #16, #4
    eor r11, r11, r14, lsl #20
    ubfx r14, r5, #26, #6
    eor r11, r11, r14, lsl #24
    ubfx r14, r5, #24, #2
    eor r11, r11, r14, lsl #30

    uxtb.w r4, r1
    ubfx r14, r1, #14, #2
    eor r4, r4, r14, lsl #8
    ubfx r14, r1, #8, #6
    eor r4, r4, r14, lsl #10
    ubfx r14, r1, #20, #4
    eor r4, r4, r14, lsl #16
    ubfx r14, r1, #16, #4
    eor r4, r4, r14, lsl #20
    ubfx r14, r1, #26, #6
    eor r4, r4, r14, lsl #24
    ubfx r14, r1, #24, #2
    eor r4, r4, r14, lsl #30

    uxtb.w r5, r6
    ubfx r14, r6, #14, #2
    eor r5, r5, r14, lsl #8
    ubfx r14, r6, #8, #6
    eor r5, r5, r14, lsl #10
    ubfx r14, r6, #20, #4
    eor r5, r5, r14, lsl #16
    ubfx r14, r6, #16, #4
    eor r5, r5, r14, lsl #20
    ubfx r14, r6, #26, #6
    eor r5, r5, r14, lsl #24
    ubfx r14, r6, #24, #2
    eor r5, r5, r14, lsl #30

    uxtb.w r6, r8
    ubfx r14, r8, #14, #2
    eor r6, r6, r14, lsl #8
    ubfx r14, r8, #8, #6
    eor r6, r6, r14, lsl #10
    ubfx r14, r8, #20, #4
    eor r6, r6, r14, lsl #16
    ubfx r14, r8, #16, #4
    eor r6, r6, r14, lsl #20
    ubfx r14, r8, #26, #6
    eor r6, r6, r14, lsl #24
    ubfx r14, r8, #24, #2
    eor r6, r6, r14, lsl #30

    uxtb.w r8, r12
    ubfx r14, r12, #14, #2
    eor r8, r8, r14, lsl #8
    ubfx r14, r12, #8, #6
    eor r8, r8, r14, lsl #10
    ubfx r14, r12, #20, #4
    eor r8, r8, r14, lsl #16
    ubfx r14, r12, #16, #4
    eor r8, r8, r14, lsl #20
    ubfx r14, r12, #26, #6
    eor r8, r8, r14, lsl #24
    ubfx r14, r12, #24, #2
    eor r8, r8, r14, lsl #30
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
    eor r11, r14
    eor r7, r12
    eor r8, r12
    eor r9, r3
    ldr r14, =AES_bsconst //in r14, as required by encrypt_blocks
    eor r10, r3

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
    ldr.w r0, [sp, #136]

    //load input, xor keystream and write to output
    ldmia r0!, {r1-r3,r12} //load first block input
    eor r4, r1
    eor r5, r2
    eor r6, r3
    eor r7, r12
    ldr.w r1, [sp, #140] //load out
    stmia.w r1!, {r4-r7} //write first block output

    ldmia.w r0!, {r4-r7} //load second block input
    eor r8, r4
    eor r9, r5
    eor r10, r6
    eor r11, r7
    stmia r1!, {r8-r11} //write second block output
    str r0, [sp, #136] //store in
    str r1, [sp, #140] //store out

    //load p, len, ctr
    ldr r0, [sp, #132] //p in r0, as required by encrypt_blocks
    ldr r3, [sp, #144] //len
    ldr r4, [r0, #12] //ctr

    //dec and store len counter
    subs r3, #32
    ble exit //if len<=0: exit
    str r3, [sp, #144]

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
    add sp, #148
    pop {r4-r12,r14}
    bx lr
""")
