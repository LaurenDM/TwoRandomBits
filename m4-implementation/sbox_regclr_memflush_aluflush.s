# :%s/#] \/\/\(Load\|Store\) \(t36_0\)$/#352] \/\/\1 \2/

.syntax unified
.thumb

.align 2
// void subbytes(uint32_t mask1, uint32_t mask2, uin32_t mask3, uint8_t *data);
.global subbytes
.type subbytes,%function
subbytes:
// r0 MASK1
// r1 MASK2
// r2 MASK3
// r3 dataptr
    push {r4-r12,r14}
    sub sp, #772

    str r3, [sp, #764] //dataptr
    str sp, [sp, #768] //flush
    str r0, [sp, #720] //MASK1
    mov r0, #0
    str sp, [sp, #768] //flush
    str r1, [sp, #724] //MASK2
    mov r1, #0
    str sp, [sp, #768] //flush
    str r2, [sp, #728] //MASK3
    str sp, [sp, #768] //flush
    mov r2, #0

// r3 dataptr
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #724] //Load MASK2
orr r2, r0, r1 //Compute M1ORM2 = MASK1 | MASK2
mov r0, #0
str r2, [sp, #0] //Store M1ORM2
mov r2, #0
mov r1, #0
ldr r0, [r3, #12] //Load i4
ldr r1, [r3, #20] //Load i2
eor r2, r0, r1 //Compute y14 = i4 ^ i2
str sp, [sp, #768] //Flush store
str r2, [sp, #4] //Store y14
mov r2, #0
mov r0, #0
mov r1, #0
ldr r0, [r3, #0] //Load i7
ldr r1, [r3, #24] //Load i1
eor r2, r0, r1 //Compute y13 = i7 ^ i1
mov r0, #0
mov r1, #0
ldr r0, [sp, #724] //Load MASK2
eor r1, r2, r0 //Compute hy13 = y13 ^ MASK2
mov r0, #0
str r2, [sp, #8] //Store y13
mov r2, #0
str r1, [sp, #12] //Store hy13
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [r3, #0] //Load i7
ldr r1, [r3, #12] //Load i4
eor r2, r0, r1 //Compute y9 = i7 ^ i4
mov r0, #0
mov r1, #0
ldr r0, [sp, #724] //Load MASK2
eor r1, r2, r0 //Compute hy9 = y9 ^ MASK2
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #16] //Store y9
mov r2, #0
str r1, [sp, #20] //Store hy9
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [r3, #0] //Load i7
ldr r1, [r3, #20] //Load i2
eor r2, r0, r1 //Compute y8 = i7 ^ i2
str sp, [sp, #768] //Flush store
str r2, [sp, #24] //Store y8
mov r2, #0
mov r0, #0
mov r1, #0
ldr r0, [r3, #4] //Load i6
ldr r1, [r3, #8] //Load i5
eor r2, r0, r1 //Compute t0 = i6 ^ i5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [r3, #28] //Load i0
eor r1, r2, r0 //Compute y1 = t0 ^ i0
mov r0, #0
str r2, [sp, #28] //Store t0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
eor r2, r1, r0 //Compute hy1 = y1 ^ MASK2
str r1, [sp, #32] //Store y1
mov r1, #0
mov r0, #0
ldr r0, [r3, #12] //Load i4
eor r1, r2, r0 //Compute y4 = hy1 ^ i4
mov r0, #0
str r2, [sp, #36] //Store hy1
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
eor r2, r1, r0 //Compute hy4 = y4 ^ MASK1
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #40] //Store hy4
mov r2, #0
str r1, [sp, #44] //Store y4
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #8] //Load y13
ldr r1, [sp, #4] //Load y14
nop
nop
nop
eor r2, r0, r1 //Compute y12 = y13 ^ y14
mov r0, #0
mov r1, #0
str r2, [sp, #48] //Store y12
mov r2, #0
ldr r0, [sp, #32] //Load y1
ldr r1, [r3, #0] //Load i7
eor r2, r1, r0 //Compute y2 = i7 ^ y1
str sp, [sp, #768] //Flush store
str r2, [sp, #52] //Store y2
mov r2, #0
mov r1, #0
ldr r1, [r3, #24] //Load i1
eor r2, r0, r1 //Compute y5 = y1 ^ i1
mov r1, #0
mov r0, #0
ldr r0, [sp, #24] //Load y8
eor r1, r2, r0 //Compute y3 = y5 ^ y8
str r2, [sp, #56] //Store y5
mov r2, #0
mov r0, #0
ldr r0, [sp, #724] //Load MASK2
eor r2, r1, r0 //Compute hy3 = y3 ^ MASK2
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #60] //Store hy3
mov r2, #0
mov r0, #0
ldr r0, [r3, #16] //Load i3
ldr r1, [sp, #48] //Load y12
eor r2, r0, r1 //Compute t1 = i3 ^ y12
mov r0, #0
str r1, [sp, #48] //Store y12
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [r3, #20] //Load i2
eor r1, r0, r2 //Compute y15 = i2 ^ t1
mov r0, #0
str r2, [sp, #64] //Store t1
mov r2, #0
ldr r0, [sp, #724] //Load MASK2
eor r2, r0, r1 //Compute hy15 = MASK2 ^ y15
mov r0, #0
str r1, [sp, #68] //Store y15
mov r1, #0
str r2, [sp, #72] //Store hy15
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #64] //Load t1
ldr r1, [r3, #4] //Load i6
eor r2, r1, r0 //Compute y20 = i6 ^ t1
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #76] //Store y20
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #68] //Load y15
ldr r1, [r3, #28] //Load i0
eor r2, r1, r0 //Compute y6 = i0 ^ y15
str r0, [sp, #68] //Store y15
mov r0, #0
mov r1, #0
ldr r0, [sp, #720] //Load MASK1
eor r1, r0, r2 //Compute hy6 = MASK1 ^ y6
mov r0, #0
str r2, [sp, #80] //Store y6
mov r2, #0
str r1, [sp, #84] //Store hy6
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #68] //Load y15
ldr r1, [sp, #28] //Load t0
eor r2, r1, r0 //Compute y10 = t0 ^ y15
str r0, [sp, #68] //Store y15
mov r0, #0
str r1, [sp, #28] //Store t0
mov r1, #0
ldr r0, [sp, #720] //Load MASK1
eor r1, r0, r2 //Compute hy10 = MASK1 ^ y10
mov r0, #0
str r2, [sp, #88] //Store y10
mov r2, #0
str r1, [sp, #92] //Store hy10
mov r1, #0
ldr r0, [sp, #76] //Load y20
ldr r1, [sp, #20] //Load hy9
eor r2, r0, r1 //Compute y11 = y20 ^ hy9
mov r1, #0
str sp, [sp, #768] //Flush store
str r0, [sp, #76] //Store y20
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
eor r1, r0, r2 //Compute hy11 = MASK1 ^ y11
str r2, [sp, #96] //Store y11
mov r2, #0
mov r0, #0
ldr r0, [r3, #28] //Load i0
eor r2, r0, r1 //Compute y7 = i0 ^ hy11
mov r0, #0
str r2, [sp, #100] //Store y7
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #88] //Load y10
nop
nop
nop
eor r2, r0, r1 //Compute y17 = y10 ^ hy11
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #104] //Store y17
mov r2, #0
ldr r1, [sp, #24] //Load y8
eor r2, r0, r1 //Compute y19 = y10 ^ y8
str r0, [sp, #88] //Store y10
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #108] //Store y19
mov r2, #0
ldr r0, [sp, #28] //Load t0
ldr r1, [sp, #96] //Load y11
eor r2, r0, r1 //Compute y16 = t0 ^ y11
mov r0, #0
str r1, [sp, #96] //Store y11
mov r1, #0
ldr r0, [sp, #12] //Load hy13
eor r1, r2, r0 //Compute y21 = y16 ^ hy13
str sp, [sp, #768] //Flush store
str r1, [sp, #112] //Store y21
mov r1, #0
mov r0, #0
ldr r0, [r3, #0] //Load i7
eor r1, r0, r2 //Compute y18 = i7 ^ y16
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #116] //Store y16
mov r2, #0
str r1, [sp, #120] //Store y18
mov r1, #0
ldr r0, [sp, #48] //Load y12
ldr r1, [sp, #68] //Load y15
and r2, r1, r0 //Compute t2_0 = y15 & y12
str r1, [sp, #68] //Store y15
mov r1, #0
str r2, [sp, #124] //Store t2_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
nop
nop
nop
and r2, r0, r1 //Compute t2_1 = y12 & MASK1
str r0, [sp, #48] //Store y12
mov r0, #0
eor r0, r2, r1 //Compute t2_2 = t2_1 ^ MASK1
str r2, [sp, #128] //Store t2_1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #124] //Load t2_0
nop
nop
nop
eor r2, r1, r0 //Compute t2_3 = t2_0 ^ t2_2
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #132] //Store t2_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #68] //Load y15
nop
nop
nop
and r2, r0, r1 //Compute t2_4 = MASK3 & y15
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t2_5 = t2_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #132] //Load t2_3
nop
nop
nop
eor r2, r0, r1 //Compute t2 = t2_3 ^ t2_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #136] //Store t2
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #60] //Load hy3
ldr r1, [sp, #80] //Load y6
nop
nop
nop
and r2, r0, r1 //Compute t3_0 = hy3 & y6
str sp, [sp, #768] //Flush store
str r1, [sp, #80] //Store y6
mov r1, #0
str r2, [sp, #140] //Store t3_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
nop
nop
nop
and r2, r0, r1 //Compute t3_1 = hy3 & MASK3
str r0, [sp, #60] //Store hy3
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute t3_2 = t3_1 ^ MASK3
str r2, [sp, #144] //Store t3_1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #140] //Load t3_0
nop
nop
nop
eor r2, r1, r0 //Compute t3_3 = t3_0 ^ t3_2
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #148] //Store t3_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #80] //Load y6
nop
nop
nop
and r2, r0, r1 //Compute t3_4 = MASK1 & y6
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t3_5 = t3_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #148] //Load t3_3
nop
nop
nop
eor r2, r0, r1 //Compute t3 = t3_3 ^ t3_5
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #136] //Load t2
nop
nop
nop
eor r1, r2, r0 //Compute t4 = t3 ^ t2
mov r2, #0
str sp, [sp, #768] //Flush store
str r0, [sp, #136] //Store t2
mov r0, #0
str r1, [sp, #152] //Store t4
mov r1, #0
ldr r0, [r3, #28] //Load i0
ldr r1, [sp, #40] //Load hy4
and r2, r1, r0 //Compute t5_0 = hy4 & i0
str r1, [sp, #40] //Store hy4
mov r1, #0
str r2, [sp, #156] //Store t5_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
and r2, r0, r1 //Compute t5_1 = i0 & MASK3
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute t5_2 = t5_1 ^ MASK3
str sp, [sp, #768] //Flush store
str r2, [sp, #160] //Store t5_1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #156] //Load t5_0
eor r2, r1, r0 //Compute t5_3 = t5_0 ^ t5_2
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #164] //Store t5_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #40] //Load hy4
and r2, r0, r1 //Compute t5_4 = MASK2 & hy4
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute t5_5 = t5_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #164] //Load t5_3
eor r2, r0, r1 //Compute t5 = t5_3 ^ t5_5
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #136] //Load t2
eor r1, r2, r0 //Compute t6 = t5 ^ t2
mov r2, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #168] //Store t6
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #12] //Load hy13
ldr r1, [sp, #116] //Load y16
nop
nop
nop
and r2, r0, r1 //Compute t7_0 = hy13 & y16
str sp, [sp, #768] //Flush store
str r1, [sp, #116] //Store y16
mov r1, #0
str r2, [sp, #172] //Store t7_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
and r2, r0, r1 //Compute t7_1 = hy13 & MASK1
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute t7_2 = t7_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #172] //Load t7_0
eor r2, r1, r0 //Compute t7_3 = t7_0 ^ t7_2
mov r0, #0
mov r1, #0
str r2, [sp, #176] //Store t7_3
mov r2, #0
ldr r0, [sp, #116] //Load y16
ldr r1, [sp, #728] //Load MASK3
nop
nop
nop
and r2, r0, r1 //Compute t7_4 = y16 & MASK3
str sp, [sp, #768] //Flush store
str r0, [sp, #116] //Store y16
mov r0, #0
mov r1, #0
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t7_5 = t7_4 ^ M1ORM2
str sp, [sp, #768] //Flush store
str r2, [sp, #452] //Store t7_4
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #176] //Load t7_3
eor r2, r0, r1 //Compute t7 = t7_3 ^ t7_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #180] //Store t7
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #32] //Load y1
ldr r1, [sp, #56] //Load y5
and r2, r0, r1 //Compute t8_0 = y1 & y5
str r1, [sp, #56] //Store y5
mov r1, #0
str r2, [sp, #184] //Store t8_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #724] //Load MASK2
and r2, r0, r1 //Compute t8_1 = y1 & MASK2
mov r0, #0
eor r0, r2, r1 //Compute t8_2 = t8_1 ^ MASK2
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #184] //Load t8_0
eor r2, r1, r0 //Compute t8_3 = t8_0 ^ t8_2
mov r1, #0
mov r0, #0
str r2, [sp, #188] //Store t8_3
mov r2, #0
ldr r0, [sp, #56] //Load y5
ldr r1, [sp, #720] //Load MASK1
and r2, r0, r1 //Compute t8_4 = y5 & MASK1
str sp, [sp, #768] //Flush store
str r0, [sp, #56] //Store y5
mov r0, #0
mov r1, #0
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute t8_5 = t8_4 ^ M1ORM2
str r2, [sp, #192] //Store t8_4
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #188] //Load t8_3
eor r2, r0, r1 //Compute t8 = t8_3 ^ t8_5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #180] //Load t7
eor r1, r2, r0 //Compute t9 = t8 ^ t7
mov r2, #0
str sp, [sp, #768] //Flush store
str r0, [sp, #180] //Store t7
mov r0, #0
str r1, [sp, #196] //Store t9
mov r1, #0
ldr r0, [sp, #100] //Load y7
ldr r1, [sp, #52] //Load y2
nop
nop
nop
and r2, r0, r1 //Compute t10_0 = y7 & y2
str r1, [sp, #52] //Store y2
mov r1, #0
str r2, [sp, #200] //Store t10_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
nop
nop
nop
and r2, r0, r1 //Compute t10_1 = y7 & MASK3
str r0, [sp, #100] //Store y7
mov r0, #0
eor r0, r2, r1 //Compute t10_2 = t10_1 ^ MASK3
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #200] //Load t10_0
nop
nop
nop
eor r2, r1, r0 //Compute t10_3 = t10_0 ^ t10_2
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #204] //Store t10_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #52] //Load y2
nop
nop
nop
and r2, r0, r1 //Compute t10_4 = MASK1 & y2
str sp, [sp, #768] //Flush store
str r1, [sp, #52] //Store y2
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r0, r2 //Compute t10_5 = M1ORM2 ^ t10_4
mov r2, #0
str sp, [sp, #768] //Flush store
str r0, [sp, #0] //Store M1ORM2
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #204] //Load t10_3
eor r2, r0, r1 //Compute t10 = t10_3 ^ t10_5
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #180] //Load t7
nop
nop
nop
eor r1, r2, r0 //Compute t11 = t10 ^ t7
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #208] //Store t11
mov r1, #0
ldr r0, [sp, #96] //Load y11
ldr r1, [sp, #16] //Load y9
nop
nop
nop
and r2, r0, r1 //Compute t12_0 = y11 & y9
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #212] //Store t12_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
nop
nop
nop
and r2, r0, r1 //Compute t12_1 = y11 & MASK3
str r0, [sp, #96] //Store y11
mov r0, #0
eor r0, r2, r1 //Compute t12_2 = t12_1 ^ MASK3
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #212] //Load t12_0
nop
nop
nop
eor r2, r1, r0 //Compute t12_3 = t12_0 ^ t12_2
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #216] //Store t12_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #12] //Load y9
nop
nop
nop
and r2, r0, r1 //Compute t12_4 = MASK2 & y9
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r0, r2 //Compute t12_5 = M1ORM2 ^ t12_4
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #216] //Load t12_3
eor r2, r0, r1 //Compute t12 = t12_3 ^ t12_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #220] //Store t12
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #104] //Load y17
ldr r1, [sp, #4] //Load y14
nop
nop
nop
and r2, r0, r1 //Compute t13_0 = y17 & y14
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #224] //Store t13_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #724] //Load MASK2
and r2, r0, r1 //Compute t13_1 = y17 & MASK2
str r0, [sp, #104] //Store y17
mov r0, #0
eor r0, r2, r1 //Compute t13_2 = t13_1 ^ MASK2
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #224] //Load t13_0
eor r2, r1, r0 //Compute t13_3 = t13_0 ^ t13_2
mov r1, #0
mov r0, #0
str r2, [sp, #228] //Store t13_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #4] //Load y14
nop
nop
nop
and r2, r0, r1 //Compute t13_4 = MASK1 & y14
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t13_5 = t13_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #228] //Load t13_3
eor r2, r0, r1 //Compute t13 = t13_3 ^ t13_5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #220] //Load t12
eor r1, r2, r0 //Compute t14 = t13 ^ t12
mov r2, #0
str sp, [sp, #768] //Flush store
str r0, [sp, #220] //Store t12
mov r0, #0
str r1, [sp, #232] //Store t14
mov r1, #0
ldr r0, [sp, #24] //Load y8
ldr r1, [sp, #88] //Load y10
nop
nop
nop
and r2, r0, r1 //Compute t15_0 = y8 & y10
str r1, [sp, #88] //Store y10
mov r1, #0
str r2, [sp, #236] //Store t15_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #724] //Load MASK2
nop
nop
nop
and r2, r0, r1 //Compute t15_1 = y8 & MASK2
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute t15_2 = t15_1 ^ MASK2
str sp, [sp, #768] //Flush store
str r2, [sp, #240] //Store t15_1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #236] //Load t15_0
nop
nop
nop
eor r2, r1, r0 //Compute t15_3 = t15_0 ^ t15_2
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #244] //Store t15_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #88] //Load y10
nop
nop
nop
and r2, r0, r1 //Compute t15_4 = MASK1 & y10
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t15_5 = t15_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #244] //Load t15_3
nop
nop
nop
eor r2, r0, r1 //Compute t15 = t15_3 ^ t15_5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #220] //Load t12
nop
nop
nop
eor r1, r2, r0 //Compute t16 = t15 ^ t12
mov r2, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #248] //Store t16
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #152] //Load t4
ldr r1, [sp, #76] //Load y20
eor r2, r0, r1 //Compute t17 = t4 ^ y20
mov r0, #0
mov r1, #0
str r2, [sp, #252] //Store t17
mov r2, #0
ldr r0, [sp, #168] //Load t6
ldr r1, [sp, #248] //Load t16
eor r2, r0, r1 //Compute t18 = t6 ^ t16
mov r0, #0
str r1, [sp, #248] //Store t16
mov r1, #0
str r2, [sp, #256] //Store t18
mov r2, #0
ldr r0, [sp, #196] //Load t9
ldr r1, [sp, #232] //Load t14
eor r2, r1, r0 //Compute t19 = t14 ^ t9
mov r0, #0
str r1, [sp, #232] //Store t14
mov r1, #0
str r2, [sp, #260] //Store t19
mov r2, #0
ldr r0, [sp, #208] //Load t11
ldr r1, [sp, #248] //Load t16
nop
nop
nop
eor r2, r0, r1 //Compute t20 = t11 ^ t16
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #264] //Store t20
mov r2, #0
ldr r0, [sp, #252] //Load t17
ldr r1, [sp, #232] //Load t14
eor r2, r1, r0 //Compute t21 = t14 ^ t17
mov r1, #0
mov r0, #0
str r2, [sp, #268] //Store t21
mov r2, #0
ldr r0, [sp, #256] //Load t18
ldr r1, [sp, #108] //Load y19
eor r2, r0, r1 //Compute t22 = t18 ^ y19
mov r1, #0
mov r0, #0
str r2, [sp, #272] //Store t22
mov r2, #0
ldr r0, [sp, #260] //Load t19
ldr r1, [sp, #112] //Load y21
eor r2, r0, r1 //Compute t23 = t19 ^ y21
mov r1, #0
mov r0, #0
ldr r0, [sp, #720] //Load MASK1
eor r1, r2, r0 //Compute ht23 = t23 ^ MASK1
mov r0, #0
str r1, [sp, #276] //Store ht23
mov r1, #0
str r2, [sp, #280] //Store t23
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #264] //Load t20
ldr r1, [sp, #120] //Load y18
nop
nop
nop
eor r2, r0, r1 //Compute t24 = t20 ^ y18
mov r1, #0
mov r0, #0
ldr r0, [sp, #720] //Load MASK1
eor r1, r2, r0 //Compute ht24 = t24 ^ MASK1
str r2, [sp, #284] //Store t24
mov r2, #0
str r1, [sp, #288] //Store ht24
mov r1, #0
mov r0, #0
ldr r0, [sp, #268] //Load t21
ldr r1, [sp, #272] //Load t22
nop
nop
nop
eor r2, r0, r1 //Compute t25 = t21 ^ t22
str sp, [sp, #768] //Flush store
str r2, [sp, #292] //Store t25
mov r2, #0
str r1, [sp, #272] //Store t22
mov r1, #0
ldr r1, [sp, #280] //Load t23
and r2, r1, r0 //Compute t26_0 = t23 & t21
str r0, [sp, #268] //Store t21
mov r0, #0
str r2, [sp, #296] //Store t26_0
mov r2, #0
ldr r0, [sp, #724] //Load MASK2
nop
nop
nop
and r2, r1, r0 //Compute t26_1 = t23 & MASK2
str r1, [sp, #280] //Store t23
mov r1, #0
nop
nop
nop
eor r1, r2, r0 //Compute t26_2 = t26_1 ^ MASK2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #296] //Load t26_0
nop
nop
nop
eor r2, r0, r1 //Compute t26_3 = t26_0 ^ t26_2
mov r0, #0
mov r1, #0
str r2, [sp, #300] //Store t26_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #268] //Load t21
nop
nop
nop
and r2, r0, r1 //Compute t26_4 = MASK3 & t21
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t26_5 = t26_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #300] //Load t26_3
nop
nop
nop
eor r2, r0, r1 //Compute t26 = t26_3 ^ t26_5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #284] //Load t24
nop
nop
nop
eor r1, r0, r2 //Compute t27 = t24 ^ t26
str sp, [sp, #768] //Flush store
str r2, [sp, #304] //Store t26
mov r2, #0
str r0, [sp, #284] //Store t24
mov r0, #0
ldr r0, [sp, #292] //Load t25
and r2, r1, r0 //Compute t28_0 = t27 & t25
str r1, [sp, #308] //Store t27
mov r1, #0
str r2, [sp, #312] //Store t28_0
mov r2, #0
ldr r1, [sp, #720] //Load MASK1
nop
nop
nop
and r2, r0, r1 //Compute t28_1 = t25 & MASK1
str r0, [sp, #292] //Store t25
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute t28_2 = t28_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #312] //Load t28_0
nop
nop
nop
eor r2, r1, r0 //Compute t28_3 = t28_0 ^ t28_2
mov r0, #0
mov r1, #0
str r2, [sp, #316] //Store t28_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #308] //Load t27
nop
nop
nop
and r2, r0, r1 //Compute t28_4 = MASK3 & t27
str sp, [sp, #768] //Flush store
str r1, [sp, #308] //Store t27
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t28_5 = t28_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #316] //Load t28_3
nop
nop
nop
eor r2, r0, r1 //Compute t28 = t28_3 ^ t28_5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #272] //Load t22
nop
nop
nop
eor r1, r2, r0 //Compute t29 = t28 ^ t22
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #320] //Store t29
mov r1, #0
str r0, [sp, #272] //Store t22
mov r0, #0
ldr r0, [sp, #280] //Load t23
ldr r1, [sp, #284] //Load t24
eor r2, r0, r1 //Compute t30 = t23 ^ t24
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #324] //Store t30
mov r2, #0
str r1, [sp, #284] //Store t24
mov r1, #0
ldr r0, [sp, #272] //Load t22
ldr r1, [sp, #304] //Load t26
eor r2, r0, r1 //Compute t31 = t22 ^ t26
mov r0, #0
mov r1, #0
ldr r0, [sp, #324] //Load t30
and r1, r2, r0 //Compute t32_0 = t31 & t30
str sp, [sp, #768] //Flush store
str r2, [sp, #328] //Store t31
mov r2, #0
str r1, [sp, #332] //Store t32_0
mov r1, #0
ldr r1, [sp, #724] //Load MASK2
nop
nop
nop
and r2, r0, r1 //Compute t32_1 = t30 & MASK2
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute t32_2 = t32_1 ^ MASK2
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #332] //Load t32_0
nop
nop
nop
eor r2, r1, r0 //Compute t32_3 = t32_0 ^ t32_2
mov r0, #0
mov r1, #0
str r2, [sp, #336] //Store t32_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #328] //Load t31
nop
nop
nop
and r2, r0, r1 //Compute t32_4 = MASK1 & t31
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t32_5 = t32_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #336] //Load t32_3
nop
nop
nop
eor r2, r0, r1 //Compute t32 = t32_3 ^ t32_5
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #284] //Load t24
nop
nop
nop
eor r1, r2, r0 //Compute t33 = t32 ^ t24
mov r2, #0
mov r0, #0
ldr r0, [sp, #720] //Load MASK1
eor r2, r1, r0 //Compute ht33 = t33 ^ MASK1
str sp, [sp, #768] //Flush store
str r2, [sp, #340] //Store ht33
mov r2, #0
mov r0, #0
ldr r0, [sp, #276] //Load ht23
eor r2, r0, r1 //Compute t34 = ht23 ^ t33
mov r0, #0
str r2, [sp, #344] //Store t34
mov r2, #0
ldr r0, [sp, #308] //Load t27
eor r2, r0, r1 //Compute t35 = t27 ^ t33
str r1, [sp, #348] //Store t33
mov r1, #0
str r0, [sp, #308] //Store t27
mov r0, #0
ldr r0, [sp, #288] //Load ht24
nop
nop
nop
and r1, r2, r0 //Compute t36_0 = t35 & ht24
str r0, [sp, #288] //Store ht24
mov r0, #0
str r1, [sp, #352] //Store t36_0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
and r1, r2, r0 //Compute t36_1 = t35 & MASK3
mov r2, #0
nop
nop
nop
eor r2, r1, r0 //Compute t36_2 = t36_1 ^ MASK3
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #352] //Load t36_0
eor r1, r0, r2 //Compute t36_3 = t36_0 ^ t36_2
mov r2, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #356] //Store t36_3
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #288] //Load ht24
and r2, r0, r1 //Compute t36_4 = MASK2 & ht24
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute t36_5 = t36_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #356] //Load t36_3
eor r2, r0, r1 //Compute t36 = t36_3 ^ t36_5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #344] //Load t34
eor r1, r2, r0 //Compute t37 = t36 ^ t34
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #360] //Store t37
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #308] //Load t27
nop
nop
nop
eor r1, r0, r2 //Compute t38 = t27 ^ t36
mov r0, #0
mov r2, #0
ldr r0, [sp, #320] //Load t29
nop
nop
nop
and r2, r0, r1 //Compute t39_0 = t29 & t38
str sp, [sp, #768] //Flush store
str r1, [sp, #364] //Store t38
mov r1, #0
str r2, [sp, #368] //Store t39_0
mov r2, #0
ldr r1, [sp, #728] //Load MASK3
nop
nop
nop
and r2, r0, r1 //Compute t39_1 = t29 & MASK3
str r0, [sp, #320] //Store t29
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute t39_2 = t39_1 ^ MASK3
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #368] //Load t39_0
nop
nop
nop
eor r2, r1, r0 //Compute t39_3 = t39_0 ^ t39_2
mov r1, #0
str sp, [sp, #768] //Flush store
str r0, [sp, #372] //Store t39_2
mov r0, #0
str r2, [sp, #376] //Store t39_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #364] //Load t38
nop
nop
nop
and r2, r0, r1 //Compute t39_4 = MASK2 & t38
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute t39_5 = t39_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #376] //Load t39_3
nop
nop
nop
eor r2, r0, r1 //Compute t39 = t39_3 ^ t39_5
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #292] //Load t25
nop
nop
nop
eor r1, r0, r2 //Compute t40 = t25 ^ t39
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #360] //Load t37
eor r2, r1, r0 //Compute t41 = t40 ^ t37
str sp, [sp, #768] //Flush store
str r2, [sp, #380] //Store t41
mov r2, #0
str r0, [sp, #360] //Store t37
mov r0, #0
str r1, [sp, #384] //Store t40
mov r1, #0
ldr r0, [sp, #320] //Load t29
ldr r1, [sp, #348] //Load t33
eor r2, r1, r0 //Compute t42 = t33 ^ t29
str sp, [sp, #768] //Flush store
str r2, [sp, #388] //Store t42
mov r2, #0
str r1, [sp, #348] //Store t33
mov r1, #0
ldr r1, [sp, #384] //Load t40
eor r2, r0, r1 //Compute t43 = t29 ^ t40
str sp, [sp, #768] //Flush store
str r2, [sp, #392] //Store t43
mov r2, #0
str r1, [sp, #384] //Store t40
mov r1, #0
str r0, [sp, #320] //Store t29
mov r0, #0
ldr r0, [sp, #340] //Load ht33
ldr r1, [sp, #360] //Load t37
eor r2, r0, r1 //Compute t44 = ht33 ^ t37
mov r0, #0
str r2, [sp, #396] //Store t44
mov r2, #0
str r1, [sp, #360] //Store t37
mov r1, #0
ldr r0, [sp, #388] //Load t42
ldr r1, [sp, #380] //Load t41
eor r2, r0, r1 //Compute t45 = t42 ^ t41
str r0, [sp, #388] //Store t42
mov r0, #0
str r2, [sp, #400] //Store t45
mov r2, #0
str r1, [sp, #380] //Store t41
mov r1, #0
ldr r0, [sp, #396] //Load t44
ldr r1, [sp, #72] //Load hy15
nop
nop
nop
and r2, r0, r1 //Compute z0_0 = t44 & hy15
str r1, [sp, #72] //Store hy15
mov r1, #0
str r2, [sp, #404] //Store z0_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
nop
nop
nop
and r2, r0, r1 //Compute z0_1 = t44 & MASK3
str r0, [sp, #396] //Store t44
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z0_2 = z0_1 ^ MASK3
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #404] //Load z0_0
nop
nop
nop
eor r2, r1, r0 //Compute z0_3 = z0_0 ^ z0_2
mov r1, #0
str sp, [sp, #768] //Flush store
str r0, [sp, #408] //Store z0_2
mov r0, #0
str r2, [sp, #412] //Store z0_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #72] //Load hy15
nop
nop
nop
and r2, r0, r1 //Compute z0_4 = MASK1 & hy15
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z0_5 = z0_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #412] //Load z0_3
nop
nop
nop
eor r2, r0, r1 //Compute z0 = z0_3 ^ z0_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #416] //Store z0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #84] //Load hy6
ldr r1, [sp, #360] //Load t37
nop
nop
nop
and r2, r0, r1 //Compute z1_0 = hy6 & t37
str r1, [sp, #360] //Store t37
mov r1, #0
str r2, [sp, #420] //Store z1_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
and r2, r0, r1 //Compute z1_1 = hy6 & MASK3
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z1_2 = z1_1 ^ MASK3
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #420] //Load z1_0
eor r2, r1, r0 //Compute z1_3 = z1_0 ^ z1_2
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #424] //Store z1_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #360] //Load t37
nop
nop
nop
and r2, r0, r1 //Compute z1_4 = MASK2 & t37
str sp, [sp, #768] //Flush store
str r1, [sp, #360] //Store t37
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z1_5 = z1_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #424] //Load z1_3
eor r2, r0, r1 //Compute z1 = z1_3 ^ z1_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #428] //Store z1
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #348] //Load t33
ldr r1, [r3, #28] //Load i0
nop
nop
nop
and r2, r0, r1 //Compute z2_0 = t33 & i0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #432] //Store z2_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #724] //Load MASK2
and r2, r0, r1 //Compute z2_1 = t33 & MASK2
str r0, [sp, #348] //Store t33
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z2_2 = z2_1 ^ MASK2
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #432] //Load z2_0
eor r2, r1, r0 //Compute z2_3 = z2_0 ^ z2_2
mov r1, #0
str r0, [sp, #436] //Store z2_2
mov r0, #0
str r2, [sp, #440] //Store z2_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #160] //Load t5_1
ldr r1, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r2, r0, r1 //Compute z2_5 = t5_1 ^ M1ORM2
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #440] //Load z2_3
eor r1, r0, r2 //Compute z2 = z2_3 ^ z2_5
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #444] //Store z2
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #116] //Load y16
ldr r1, [sp, #392] //Load t43
nop
nop
nop
and r2, r0, r1 //Compute z3_0 = y16 & t43
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #392] //Store t43
mov r1, #0
str r2, [sp, #448] //Store z3_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #452] //Load t7_4
ldr r1, [sp, #728] //Load MASK3
nop
nop
nop
eor r2, r0, r1 //Compute z3_2 = t7_4 ^ MASK3
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #448] //Load z3_0
nop
nop
nop
eor r1, r0, r2 //Compute z3_3 = z3_0 ^ z3_2
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #456] //Store z3_3
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #392] //Load t43
and r2, r1, r0 //Compute z3_4 = t43 & MASK1
str sp, [sp, #768] //Flush store
str r1, [sp, #392] //Store t43
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute z3_5 = z3_4 ^ M1ORM2
str r2, [sp, #460] //Store z3_4
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #456] //Load z3_3
eor r2, r0, r1 //Compute z3 = z3_3 ^ z3_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #464] //Store z3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #36] //Load hy1
ldr r1, [sp, #384] //Load t40
nop
nop
nop
and r2, r0, r1 //Compute z4_0 = hy1 & t40
str sp, [sp, #768] //Flush store
str r1, [sp, #384] //Store t40
mov r1, #0
str r2, [sp, #468] //Store z4_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
and r2, r0, r1 //Compute z4_1 = hy1 & MASK1
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z4_2 = z4_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #468] //Load z4_0
eor r2, r1, r0 //Compute z4_3 = z4_0 ^ z4_2
mov r1, #0
mov r0, #0
str r2, [sp, #472] //Store z4_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #384] //Load t40
and r2, r0, r1 //Compute z4_4 = MASK3 & t40
str sp, [sp, #768] //Flush store
str r1, [sp, #384] //Store t40
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute z4_5 = z4_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #472] //Load z4_3
eor r2, r0, r1 //Compute z4 = z4_3 ^ z4_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #476] //Store z4
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #320] //Load t29
ldr r1, [sp, #100] //Load y7
nop
nop
nop
and r2, r0, r1 //Compute z5_0 = t29 & y7
str r1, [sp, #100] //Store y7
mov r1, #0
str r2, [sp, #480] //Store z5_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
and r2, r0, r1 //Compute z5_1 = t29 & MASK1
str r0, [sp, #320] //Store t29
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z5_2 = z5_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #480] //Load z5_0
eor r2, r1, r0 //Compute z5_3 = z5_0 ^ z5_2
mov r0, #0
mov r1, #0
str r2, [sp, #484] //Store z5_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #100] //Load y7
nop
nop
nop
and r2, r0, r1 //Compute z5_4 = MASK2 & y7
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z5_5 = z5_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #484] //Load z5_3
eor r2, r0, r1 //Compute z5 = z5_3 ^ z5_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #488] //Store z5
mov r2, #0
ldr r0, [sp, #96] //Load y11
ldr r1, [sp, #388] //Load t42
and r2, r0, r1 //Compute z6_0 = y11 & t42
str r1, [sp, #388] //Store t42
mov r1, #0
str r2, [sp, #492] //Store z6_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
and r2, r0, r1 //Compute z6_1 = y11 & MASK1
mov r0, #0
eor r0, r2, r1 //Compute z6_2 = z6_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #492] //Load z6_0
eor r2, r1, r0 //Compute z6_3 = z6_0 ^ z6_2
mov r1, #0
mov r0, #0
str r2, [sp, #496] //Store z6_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #388] //Load t42
and r2, r0, r1 //Compute z6_4 = MASK2 & t42
str sp, [sp, #768] //Flush store
str r1, [sp, #388] //Store t42
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute z6_5 = z6_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #496] //Load z6_3
eor r2, r0, r1 //Compute z6 = z6_3 ^ z6_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #500] //Store z6
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #104] //Load y17
ldr r1, [sp, #400] //Load t45
nop
nop
nop
and r2, r0, r1 //Compute z7_0 = y17 & t45
str r1, [sp, #400] //Store t45
mov r1, #0
str r2, [sp, #504] //Store z7_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
and r2, r0, r1 //Compute z7_1 = y17 & MASK3
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z7_2 = z7_1 ^ MASK3
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #504] //Load z7_0
eor r2, r1, r0 //Compute z7_3 = z7_0 ^ z7_2
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #508] //Store z7_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #720] //Load MASK1
ldr r1, [sp, #400] //Load t45
nop
nop
nop
and r2, r0, r1 //Compute z7_4 = MASK1 & t45
str sp, [sp, #768] //Flush store
str r1, [sp, #400] //Store t45
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z7_5 = z7_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #508] //Load z7_3
eor r2, r0, r1 //Compute z7 = z7_3 ^ z7_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #512] //Store z7
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #92] //Load hy10
ldr r1, [sp, #380] //Load t41
nop
nop
nop
and r2, r0, r1 //Compute z8_0 = hy10 & t41
str r1, [sp, #380] //Store t41
mov r1, #0
str r2, [sp, #516] //Store z8_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #724] //Load MASK2
and r2, r0, r1 //Compute z8_1 = hy10 & MASK2
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z8_2 = z8_1 ^ MASK2
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #516] //Load z8_0
eor r2, r1, r0 //Compute z8_3 = z8_0 ^ z8_2
mov r1, #0
mov r0, #0
str r2, [sp, #520] //Store z8_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #380] //Load t41
nop
nop
nop
and r2, r0, r1 //Compute z8_4 = MASK3 & t41
str sp, [sp, #768] //Flush store
str r1, [sp, #380] //Store t41
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z8_5 = z8_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #520] //Load z8_3
eor r2, r0, r1 //Compute z8 = z8_3 ^ z8_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #524] //Store z8
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #396] //Load t44
ldr r1, [sp, #48] //Load y12
nop
nop
nop
and r2, r0, r1 //Compute z9_0 = t44 & y12
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #408] //Load z0_2
nop
nop
nop
eor r1, r2, r0 //Compute z9_3 = z9_0 ^ z0_2
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #528] //Store z9_3
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #128] //Load t2_1
ldr r1, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r2, r0, r1 //Compute z9_5 = t2_1 ^ M1ORM2
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #528] //Load z9_3
nop
nop
nop
eor r1, r0, r2 //Compute z9 = z9_3 ^ z9_5
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #532] //Store z9
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #360] //Load t37
ldr r1, [sp, #60] //Load hy3
nop
nop
nop
and r2, r0, r1 //Compute z10_0 = t37 & hy3
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #536] //Store z10_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
nop
nop
nop
and r2, r0, r1 //Compute z10_1 = t37 & MASK1
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z10_2 = z10_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #536] //Load z10_0
nop
nop
nop
eor r2, r1, r0 //Compute z10_3 = z10_0 ^ z10_2
mov r0, #0
mov r1, #0
str r2, [sp, #540] //Store z10_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #144] //Load t3_1
ldr r1, [sp, #0] //Load M1ORM2
eor r2, r0, r1 //Compute z10_5 = t3_1 ^ M1ORM2
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #540] //Load z10_3
eor r1, r0, r2 //Compute z10 = z10_3 ^ z10_5
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #544] //Store z10
mov r1, #0
ldr r0, [sp, #348] //Load t33
ldr r1, [sp, #44] //Load y4
nop
nop
nop
and r2, r0, r1 //Compute z11_0 = t33 & y4
mov r0, #0
str r1, [sp, #44] //Store y4
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #436] //Load z2_2
eor r1, r0, r2 //Compute z11_3 = z2_2 ^ z11_0
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #548] //Store z11_3
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #44] //Load y4
nop
nop
nop
and r2, r0, r1 //Compute z11_4 = MASK3 & y4
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z11_5 = z11_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #548] //Load z11_3
eor r2, r0, r1 //Compute z11 = z11_3 ^ z11_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #552] //Store z11
mov r2, #0
ldr r0, [sp, #392] //Load t43
ldr r1, [sp, #8] //Load y13
nop
nop
nop
and r2, r0, r1 //Compute z12_0 = t43 & y13
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #556] //Store z12_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #460] //Load z3_4
ldr r1, [sp, #720] //Load MASK1
nop
nop
nop
eor r2, r0, r1 //Compute z12_2 = z3_4 ^ MASK1
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #556] //Load z12_0
nop
nop
nop
eor r1, r0, r2 //Compute z12_3 = z12_0 ^ z12_2
mov r2, #0
mov r0, #0
str r1, [sp, #560] //Store z12_3
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #8] //Load y13
nop
nop
nop
and r2, r0, r1 //Compute z12_4 = MASK3 & y13
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z12_5 = z12_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #560] //Load z12_3
nop
nop
nop
eor r2, r0, r1 //Compute z12 = z12_3 ^ z12_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #564] //Store z12
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #56] //Load y5
ldr r1, [sp, #384] //Load t40
nop
nop
nop
and r2, r0, r1 //Compute z13_0 = y5 & t40
mov r0, #0
str r1, [sp, #384] //Store t40
mov r1, #0
str r2, [sp, #568] //Store z13_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #192] //Load t8_4
ldr r1, [sp, #720] //Load MASK1
nop
nop
nop
eor r2, r0, r1 //Compute z13_2 = t8_4 ^ MASK1
mov r0, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #568] //Load z13_0
eor r1, r0, r2 //Compute z13_3 = z13_0 ^ z13_2
mov r2, #0
mov r0, #0
str r1, [sp, #572] //Store z13_3
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #384] //Load t40
and r2, r0, r1 //Compute z13_4 = MASK2 & t40
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute z13_5 = z13_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #572] //Load z13_3
eor r2, r0, r1 //Compute z13 = z13_3 ^ z13_5
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #576] //Store z13
mov r2, #0
ldr r0, [sp, #320] //Load t29
ldr r1, [sp, #52] //Load y2
nop
nop
nop
and r2, r0, r1 //Compute z14_0 = t29 & y2
mov r0, #0
str r1, [sp, #52] //Store y2
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #372] //Load t39_2
nop
nop
nop
eor r1, r2, r0 //Compute z14_3 = z14_0 ^ t39_2
mov r2, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #580] //Store z14_3
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #52] //Load y2
nop
nop
nop
and r2, r0, r1 //Compute z14_4 = MASK2 & y2
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z14_5 = z14_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #580] //Load z14_3
nop
nop
nop
eor r2, r0, r1 //Compute z14 = z14_3 ^ z14_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #584] //Store z14
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #12] //Load y9
ldr r1, [sp, #388] //Load t42
nop
nop
nop
and r2, r0, r1 //Compute z15_0 = y9 & t42
str r1, [sp, #388] //Store t42
mov r1, #0
str r2, [sp, #588] //Store z15_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
and r2, r0, r1 //Compute z15_1 = y9 & MASK1
mov r0, #0
nop
nop
nop
eor r0, r2, r1 //Compute z15_2 = z15_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #588] //Load z15_0
eor r2, r1, r0 //Compute z15_3 = z15_0 ^ z15_2
mov r1, #0
mov r0, #0
str r2, [sp, #592] //Store z15_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #728] //Load MASK3
ldr r1, [sp, #388] //Load t42
nop
nop
nop
and r2, r0, r1 //Compute z15_4 = MASK3 & t42
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
nop
nop
nop
eor r1, r2, r0 //Compute z15_5 = z15_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #592] //Load z15_3
eor r2, r0, r1 //Compute z15 = z15_3 ^ z15_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #596] //Store z15
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #4] //Load y14
ldr r1, [sp, #400] //Load t45
and r2, r0, r1 //Compute z16_0 = y14 & t45
str sp, [sp, #768] //Flush store
str r1, [sp, #400] //Store t45
mov r1, #0
str r2, [sp, #600] //Store z16_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #728] //Load MASK3
and r2, r0, r1 //Compute z16_1 = y14 & MASK3
mov r0, #0
eor r0, r2, r1 //Compute z16_2 = z16_1 ^ MASK3
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #600] //Load z16_0
eor r2, r1, r0 //Compute z16_3 = z16_0 ^ z16_2
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #604] //Store z16_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #724] //Load MASK2
ldr r1, [sp, #400] //Load t45
and r2, r0, r1 //Compute z16_4 = MASK2 & t45
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #0] //Load M1ORM2
eor r1, r2, r0 //Compute z16_5 = z16_4 ^ M1ORM2
mov r2, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #604] //Load z16_3
eor r2, r0, r1 //Compute z16 = z16_3 ^ z16_5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #608] //Store z16
mov r2, #0
ldr r0, [sp, #380] //Load t41
ldr r1, [sp, #24] //Load y8
nop
nop
nop
and r2, r0, r1 //Compute z17_0 = t41 & y8
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #612] //Store z17_0
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #720] //Load MASK1
nop
nop
nop
and r2, r0, r1 //Compute z17_1 = t41 & MASK1
mov r0, #0
eor r0, r2, r1 //Compute z17_2 = z17_1 ^ MASK1
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r1, [sp, #612] //Load z17_0
nop
nop
nop
eor r2, r1, r0 //Compute z17_3 = z17_0 ^ z17_2
mov r1, #0
mov r0, #0
str r2, [sp, #616] //Store z17_3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #240] //Load t15_1
ldr r1, [sp, #0] //Load M1ORM2
eor r2, r0, r1 //Compute z17_5 = t15_1 ^ M1ORM2
mov r1, #0
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #616] //Load z17_3
eor r1, r0, r2 //Compute z17 = z17_3 ^ z17_5
mov r2, #0
mov r0, #0
str r1, [sp, #620] //Store z17
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #596] //Load z15
ldr r1, [sp, #608] //Load z16
nop
nop
nop
eor r2, r0, r1 //Compute tc1 = z15 ^ z16
mov r1, #0
str r0, [sp, #596] //Store z15
mov r0, #0
ldr r0, [sp, #544] //Load z10
eor r1, r0, r2 //Compute tc2 = z10 ^ tc1
mov r0, #0
str r2, [sp, #624] //Store tc1
mov r2, #0
ldr r0, [sp, #532] //Load z9
eor r2, r0, r1 //Compute tc3 = z9 ^ tc2
mov r0, #0
str r2, [sp, #628] //Store tc3
mov r2, #0
str r1, [sp, #632] //Store tc2
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #416] //Load z0
ldr r1, [sp, #444] //Load z2
eor r2, r0, r1 //Compute tc4 = z0 ^ z2
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #636] //Store tc4
mov r2, #0
ldr r1, [sp, #428] //Load z1
eor r2, r1, r0 //Compute tc5 = z1 ^ z0
mov r0, #0
mov r1, #0
str r2, [sp, #640] //Store tc5
mov r2, #0
ldr r0, [sp, #464] //Load z3
ldr r1, [sp, #476] //Load z4
eor r2, r0, r1 //Compute tc6 = z3 ^ z4
mov r1, #0
str r2, [sp, #644] //Store tc6
mov r2, #0
str r0, [sp, #464] //Store z3
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #564] //Load z12
ldr r1, [sp, #636] //Load tc4
eor r2, r0, r1 //Compute tc7 = z12 ^ tc4
str r1, [sp, #636] //Store tc4
mov r1, #0
str r0, [sp, #564] //Store z12
mov r0, #0
str r2, [sp, #648] //Store tc7
mov r2, #0
ldr r0, [sp, #512] //Load z7
ldr r1, [sp, #644] //Load tc6
eor r2, r1, r0 //Compute tc8 = tc6 ^ z7
mov r0, #0
str r2, [sp, #652] //Store tc8
mov r2, #0
str r1, [sp, #644] //Store tc6
mov r1, #0
ldr r0, [sp, #524] //Load z8
ldr r1, [sp, #648] //Load tc7
eor r2, r0, r1 //Compute tc9 = z8 ^ tc7
mov r1, #0
mov r0, #0
ldr r0, [sp, #652] //Load tc8
eor r1, r0, r2 //Compute tc10 = tc8 ^ tc9
mov r2, #0
str r0, [sp, #652] //Store tc8
mov r0, #0
str r1, [sp, #656] //Store tc10
mov r1, #0
ldr r0, [sp, #644] //Load tc6
ldr r1, [sp, #640] //Load tc5
nop
nop
nop
eor r2, r0, r1 //Compute tc11 = tc6 ^ tc5
mov r0, #0
mov r1, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #660] //Store tc11
mov r2, #0
ldr r0, [sp, #464] //Load z3
ldr r1, [sp, #488] //Load z5
eor r2, r0, r1 //Compute tc12 = z3 ^ z5
mov r1, #0
mov r0, #0
str r2, [sp, #664] //Store tc12
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #576] //Load z13
ldr r1, [sp, #624] //Load tc1
eor r2, r0, r1 //Compute tc13 = z13 ^ tc1
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #668] //Store tc13
mov r2, #0
ldr r0, [sp, #636] //Load tc4
ldr r1, [sp, #664] //Load tc12
eor r2, r1, r0 //Compute tc14 = tc12 ^ tc4
mov r0, #0
mov r1, #0
str r2, [sp, #672] //Store tc14
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #628] //Load tc3
ldr r1, [sp, #660] //Load tc11
eor r2, r1, r0 //Compute S3 = tc11 ^ tc3
mov r1, #0
str r0, [sp, #628] //Store tc3
mov r0, #0
str r2, [sp, #696] //Store S3
mov r2, #0
ldr r0, [sp, #500] //Load z6
ldr r1, [sp, #652] //Load tc8
eor r2, r1, r0 //Compute tc16 = tc8 ^ z6
mov r1, #0
mov r0, #0
str r2, [sp, #676] //Store tc16
mov r2, #0
ldr r0, [sp, #584] //Load z14
ldr r1, [sp, #656] //Load tc10
eor r2, r0, r1 //Compute tc17 = z14 ^ tc10
mov r0, #0
str r2, [sp, #680] //Store tc17
mov r2, #0
str r1, [sp, #656] //Store tc10
mov r1, #0
ldr r0, [sp, #668] //Load tc13
ldr r1, [sp, #672] //Load tc14
eor r2, r1, r0 //Compute tc18 = tc14 ^ tc13
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #672] //Store tc14
mov r1, #0
ldr r0, [sp, #564] //Load z12
eor r1, r0, r2 //Compute S7 = z12 ^ tc18 ^ 1 (moved to key schedule)
mov r0, #0
str r2, [sp, #684] //Store tc18
mov r2, #0
str r1, [sp, #700] //Store S7
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #596] //Load z15
ldr r1, [sp, #676] //Load tc16
eor r2, r1, r0 //Compute tc20 = tc16 ^ z15
mov r0, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #676] //Store tc16
mov r1, #0
str r2, [sp, #688] //Store tc20
mov r2, #0
ldr r0, [sp, #632] //Load tc2
ldr r1, [sp, #552] //Load z11
eor r2, r0, r1 //Compute tc21 = tc2 ^ z11
mov r1, #0
mov r0, #0
str r2, [sp, #692] //Store tc21
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #628] //Load tc3
ldr r1, [sp, #676] //Load tc16
eor r2, r0, r1 //Compute o7 = tc3 ^ tc16
str r2, [sp, #760] //Store o7
mov r2, #0
mov r0, #0
str r1, [sp, #676] //Store tc16
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #656] //Load tc10
ldr r1, [sp, #684] //Load tc18
eor r2, r0, r1 //Compute o1 = tc10 ^ tc18 ^ 1 (moved to key schedule)
mov r1, #0
mov r0, #0
str r2, [sp, #736] //Store o1
mov r2, #0
ldr r0, [sp, #672] //Load tc14
ldr r1, [sp, #696] //Load S3
eor r2, r1, r0 //Compute S4 = S3 ^ tc14
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #704] //Store S4
mov r2, #0
ldr r0, [sp, #676] //Load tc16
nop
nop
nop
eor r2, r1, r0 //Compute S1 = S3 ^ tc16 ^ 1 (moved to key schedule)
mov r0, #0
str sp, [sp, #768] //Flush store
str r2, [sp, #708] //Store S1
mov r2, #0
str r1, [sp, #696] //Store S3
mov r1, #0
ldr r0, [sp, #680] //Load tc17
ldr r1, [sp, #688] //Load tc20
eor r2, r0, r1 //Compute tc26 = tc17 ^ tc20
mov r1, #0
str r0, [sp, #680] //Store tc17
mov r0, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #620] //Load z17
eor r1, r2, r0 //Compute S2 = tc26 ^ z17 ^ 1 (moved to key schedule)
mov r0, #0
mov r2, #0
str sp, [sp, #768] //Flush store
str r1, [sp, #712] //Store S2
mov r1, #0
ldr r0, [sp, #692] //Load tc21
ldr r1, [sp, #680] //Load tc17
eor r2, r1, r0 //Compute S5 = tc17 ^ tc21
mov r1, #0
mov r0, #0
str r2, [sp, #716] //Store S5
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #708] //Load S1
ldr r1, [sp, #724] //Load MASK2
eor r2, r1, r0 //Compute o6 = MASK2 ^ S1
mov r0, #0
str r2, [sp, #756] //Store o6
mov r2, #0
mov r1, #0
ldr r0, [sp, #712] //Load S2
ldr r1, [sp, #720] //Load MASK1
eor r2, r0, r1 //Compute o5 = S2 ^ MASK1
mov r0, #0
str r2, [sp, #752] //Store o5
mov r2, #0
mov r1, #0
ldr r0, [sp, #696] //Load S3
ldr r1, [sp, #728] //Load MASK3
eor r2, r0, r1 //Compute o4 = S3 ^ MASK3
mov r0, #0
str r2, [sp, #748] //Store o4
mov r2, #0
mov r1, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #704] //Load S4
ldr r1, [sp, #724] //Load MASK2
nop
nop
nop
eor r2, r0, r1 //Compute o3 = S4 ^ MASK2
mov r1, #0
mov r0, #0
str sp, [sp, #768] //Store load
str r2, [sp, #744] //Store o3
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #716] //Load S5
ldr r1, [sp, #720] //Load MASK1
eor r2, r0, r1 //Compute o2 = S5 ^ MASK1
mov r0, #0
mov r1, #0
str r2, [sp, #740] //Store o2
mov r2, #0
ldr sp, [sp, #768] //Flush load
ldr r0, [sp, #700] //Load S7
ldr r1, [sp, #728] //Load MASK3
eor r2, r0, r1 //Compute o0 = S7 ^ MASK3
str r2, [sp, #732] //Store o0
mov r2, #0
mov r0, #0
mov r1, #0

    //store output
    ldr sp, [sp, #768]
    ldr r0, [sp, #760]
    str sp, [sp, #768]
    str r0, [r3,  #0]
    mov r0, #0
    ldr sp, [sp, #768]
    ldr r0, [sp, #756]
    str sp, [sp, #768]
    str r0, [r3,  #4]
    mov r0, #0
    ldr sp, [sp, #768]
    ldr r0, [sp, #752]
    str sp, [sp, #768]
    str r0, [r3,  #8]
    mov r0, #0
    ldr sp, [sp, #768]
    ldr r0, [sp, #748]
    str sp, [sp, #768]
    str r0, [r3, #12]
    mov r0, #0
    ldr sp, [sp, #768]
    ldr r0, [sp, #744]
    str sp, [sp, #768]
    str r0, [r3, #16]
    mov r0, #0
    ldr sp, [sp, #768]
    ldr r0, [sp, #740]
    str sp, [sp, #768]
    str r0, [r3, #20]
    mov r0, #0
    ldr sp, [sp, #768]
    ldr r0, [sp, #736]
    str sp, [sp, #768]
    str r0, [r3, #24]
    mov r0, #0
    ldr sp, [sp, #768]
    ldr r0, [sp, #732]
    str sp, [sp, #768]
    str r0, [r3, #28]
    mov r0, #0

    add sp, #772
    pop {r4-r12,r14}
    bx lr
