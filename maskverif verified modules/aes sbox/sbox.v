module verification_wrapper(
input   i0_0, i1_0, i2_0, i3_0, i4_0, i5_0, i6_0, i7_0,
input   i0_1, i1_1, i2_1, i3_1, i4_1, i5_1, i6_1, i7_1,
input   m1, m2,
output  o0, o1, o2, o3, o4, o5, o6, o7,
);

      // Ensure mask encoding and relation as we assume
      assign i0 = (i0_0 ^ m2)      ^ i0_1; // 2 
      assign i1 = (i1_0 ^ m1 ^ m2) ^ i1_1; // 3
      assign i2 = (i2_0 ^ m1 ^ m2) ^ i2_1; // 3
      assign i3 = (i3_0 ^ m1)      ^ i3_1; // 1
      assign i4 = (i4_0 ^ m1)      ^ i4_1; // 1
      assign i5 = (i5_0 ^ m2)      ^ i5_1; // 2
      assign i6 = (i6_0 ^ m1)      ^ i6_1; // 1
      assign i7 = (i7_0 ^ m2)      ^ i7_1; // 2

      // DUV
      aes_sbox aes_sbox_inst(
        .i0(i0),
		.i1(i1),
        .i2(i2),                 
        .i3(i3),
        .i4(i4),
        .i5(i5),
        .i6(i6),
        .i7(i7),
        .MASK1(m1), 
        .MASK2(m2), 
		.o0(o0),
		.o1(o1),
        .o2(o2),
        .o3(o3),
        .o4(o4),
        .o5(o5),
        .o6(o6),
        .o7(o7));
        
endmodule

module aes_sbox(
   input i0, i1, i2, i3, i4, i5, i6, i7, MASK1, MASK2, 
   output o0, o1, o2, o3, o4, o5, o6, o7 
) ;

/* i0 -> 2, i1 -> 3, i2 -> 3, i3 -> 1, i4 -> 1, i5 -> 2, i6 -> 1, i7 -> 2, */
// Replace next line with 'assign M1ORM2 = MASK1 | MASK2;' for final code 
assign M1ORM2 = ~(~MASK1 & ~MASK2); 
  
// Manually inserted code
assign i0_m = MASK2;  
  
assign MASK3 = MASK1 ^ MASK2; 
assign MASK3_m = MASK3;
assign y14 = i4 ^ i2; 
assign y14_m = MASK2;
assign y13 = i7 ^ i1; 
assign y13_m = MASK1;
assign hy13 = y13 ^ MASK2; 
assign hy13_m = MASK3;
assign y9 = i7 ^ i4; 
assign y9_m = MASK3;
assign hy9 = y9 ^ MASK2; 
assign hy9_m = MASK1;
assign y8 = i7 ^ i2; 
assign y8_m = MASK1;
assign t0 = i6 ^ i5; 
assign t0_m = MASK3;
assign y1 = t0 ^ i0; 
assign y1_m = MASK1;
assign hy1 = y1 ^ MASK2; 
assign hy1_m = MASK3;
assign y4 = hy1 ^ i4; 
assign y4_m = MASK2;
assign hy4 = y4 ^ MASK1; 
assign hy4_m = MASK3;
assign y12 = y13 ^ y14; 
assign y12_m = MASK3;
assign y2 = y1 ^ i7; 
assign y2_m = MASK3;
assign y5 = y1 ^ i1; 
assign y5_m = MASK2;
assign y3 = y5 ^ y8; 
assign y3_m = MASK3;
assign hy3 = y3 ^ MASK2; 
assign hy3_m = MASK1;
assign t1 = i3 ^ y12; 
assign t1_m = MASK2;
assign y15 = t1 ^ i2; 
assign y15_m = MASK1;
assign hy15 = y15 ^ MASK2; 
assign hy15_m = MASK3;
assign y20 = t1 ^ i6; 
assign y20_m = MASK3;
assign y6 = y15 ^ i0; 
assign y6_m = MASK3;
assign hy6 = y6 ^ MASK1; 
assign hy6_m = MASK2;
assign y10 = y15 ^ t0; 
assign y10_m = MASK2;
assign hy10 = y10 ^ MASK1; 
assign hy10_m = MASK3;
assign y11 = y20 ^ hy9; 
assign y11_m = MASK2;
assign hy11 = y11 ^ MASK1; 
assign hy11_m = MASK3;
assign y7 = i0 ^ hy11; 
assign y7_m = MASK1;
assign y17 = y10 ^ hy11; 
assign y17_m = MASK1;
assign y19 = y10 ^ y8; 
assign y19_m = MASK3;
assign y16 = t0 ^ y11; 
assign y16_m = MASK1;
assign y21 = hy13 ^ y16; 
assign y21_m = MASK2;
assign y18 = i7 ^ y16; 
assign y18_m = MASK3;
assign t2 = ((y12 & y15) ^ ((y12 & y15_m) ^ y15_m)) ^ ((y12_m & y15) ^ M1ORM2);
assign t2_m = y12_m;
assign t3 = ((hy3 & y6) ^ ((hy3 & y6_m) ^ y6_m)) ^ ((hy3_m & y6) ^ M1ORM2);
assign t3_m = hy3_m;
assign t4 = t3 ^ t2; 
assign t4_m = MASK2;
assign t5 = ((i0 & hy4) ^ ((i0 & hy4_m) ^ hy4_m)) ^ ((i0_m & hy4) ^ M1ORM2);
assign t5_m = i0_m;
assign t6 = t5 ^ t2; 
assign t6_m = MASK1;
assign t7 = ((hy13 & y16) ^ ((hy13 & y16_m) ^ y16_m)) ^ ((hy13_m & y16) ^ M1ORM2);
assign t7_m = hy13_m;
assign t8 = ((y1 & y5) ^ ((y1 & y5_m) ^ y5_m)) ^ ((y1_m & y5) ^ M1ORM2);
assign t8_m = y1_m;
assign t9 = t8 ^ t7; 
assign t9_m = MASK2;
assign t10 = ((y7 & y2) ^ ((y7 & y2_m) ^ y2_m)) ^ ((y7_m & y2) ^ M1ORM2);
assign t10_m = y7_m;
assign t11 = t10 ^ t7; 
assign t11_m = MASK2;
assign t12 = ((y11 & y9) ^ ((y11 & y9_m) ^ y9_m)) ^ ((y11_m & y9) ^ M1ORM2);
assign t12_m = y11_m;
assign t13 = ((y17 & y14) ^ ((y17 & y14_m) ^ y14_m)) ^ ((y17_m & y14) ^ M1ORM2);
assign t13_m = y17_m;
assign t14 = t13 ^ t12; 
assign t14_m = MASK3;
assign t15 = ((y8 & y10) ^ ((y8 & y10_m) ^ y10_m)) ^ ((y8_m & y10) ^ M1ORM2);
assign t15_m = y8_m;
assign t16 = t15 ^ t12; 
assign t16_m = MASK3;
assign t17 = t4 ^ y20; 
assign t17_m = MASK1;
assign t18 = t6 ^ t16; 
assign t18_m = MASK2;
assign t19 = t9 ^ t14; 
assign t19_m = MASK1;
assign t20 = t11 ^ t16; 
assign t20_m = MASK1;
assign t21 = t17 ^ t14; 
assign t21_m = MASK2;
assign t22 = t18 ^ y19; 
assign t22_m = MASK1;
assign t23 = t19 ^ y21; 
assign t23_m = MASK3;
assign ht23 = t23 ^ MASK1; 
assign ht23_m = MASK2;
assign t24 = t20 ^ y18; 
assign t24_m = MASK2;
assign ht24 = t24 ^ MASK1; 
assign ht24_m = MASK3;
assign t25 = t21 ^ t22; 
assign t25_m = MASK3;
assign t26 = ((t23 & t21) ^ ((t23 & t21_m) ^ t21_m)) ^ ((t23_m & t21) ^ M1ORM2);
assign t26_m = t23_m;
assign t27 = t24 ^ t26; 
assign t27_m = MASK1;
assign t28 = ((t25 & t27) ^ ((t25 & t27_m) ^ t27_m)) ^ ((t25_m & t27) ^ M1ORM2);
assign t28_m = t25_m;
assign t29 = t28 ^ t22; 
assign t29_m = MASK2;
assign t30 = t23 ^ t24; 
assign t30_m = MASK1;
assign t31 = t22 ^ t26; 
assign t31_m = MASK2;
assign t32 = ((t30 & t31) ^ ((t30 & t31_m) ^ t31_m)) ^ ((t30_m & t31) ^ M1ORM2);
assign t32_m = t30_m;
assign t33 = t32 ^ t24; 
assign t33_m = MASK3;
assign ht33 = t33 ^ MASK1; 
assign ht33_m = MASK2;
assign t34 = ht23 ^ t33; 
assign t34_m = MASK1;
assign t35 = t27 ^ t33; 
assign t35_m = MASK2;
assign t36 = ((t35 & ht24) ^ ((t35 & ht24_m) ^ ht24_m)) ^ ((t35_m & ht24) ^ M1ORM2);
assign t36_m = t35_m;
assign t37 = t36 ^ t34; 
assign t37_m = MASK3;
assign t38 = t27 ^ t36; 
assign t38_m = MASK3;
assign t39 = ((t29 & t38) ^ ((t29 & t38_m) ^ t38_m)) ^ ((t29_m & t38) ^ M1ORM2);
assign t39_m = t29_m;
assign t40 = t25 ^ t39; 
assign t40_m = MASK1;
assign t41 = t40 ^ t37; 
assign t41_m = MASK2;
assign t42 = t29 ^ t33; 
assign t42_m = MASK1;
assign t43 = t29 ^ t40; 
assign t43_m = MASK3;
assign t44 = ht33 ^ t37; 
assign t44_m = MASK1;
assign t45 = t42 ^ t41; 
assign t45_m = MASK3;
assign z0 = ((t44 & hy15) ^ ((t44 & hy15_m) ^ hy15_m)) ^ ((t44_m & hy15) ^ M1ORM2);
assign z0_m = t44_m;
assign z1 = ((hy6 & t37) ^ ((hy6 & t37_m) ^ t37_m)) ^ ((hy6_m & t37) ^ M1ORM2);
assign z1_m = hy6_m;
assign z2 = ((t33 & i0) ^ ((t33 & i0_m) ^ i0_m)) ^ ((t33_m & i0) ^ M1ORM2);
assign z2_m = t33_m;
assign z3 = ((y16 & t43) ^ ((y16 & t43_m) ^ t43_m)) ^ ((y16_m & t43) ^ M1ORM2);
assign z3_m = y16_m;
assign z4 = ((hy1 & t40) ^ ((hy1 & t40_m) ^ t40_m)) ^ ((hy1_m & t40) ^ M1ORM2);
assign z4_m = hy1_m;
assign z5 = ((t29 & y7) ^ ((t29 & y7_m) ^ y7_m)) ^ ((t29_m & y7) ^ M1ORM2);
assign z5_m = t29_m;
assign z6 = ((y11 & t42) ^ ((y11 & t42_m) ^ t42_m)) ^ ((y11_m & t42) ^ M1ORM2);
assign z6_m = y11_m;
assign z7 = ((y17 & t45) ^ ((y17 & t45_m) ^ t45_m)) ^ ((y17_m & t45) ^ M1ORM2);
assign z7_m = y17_m;
assign z8 = ((hy10 & t41) ^ ((hy10 & t41_m) ^ t41_m)) ^ ((hy10_m & t41) ^ M1ORM2);
assign z8_m = hy10_m;
assign z9 = ((t44 & y12) ^ ((t44 & y12_m) ^ y12_m)) ^ ((t44_m & y12) ^ M1ORM2);
assign z9_m = t44_m;
assign z10 = ((t37 & hy3) ^ ((t37 & hy3_m) ^ hy3_m)) ^ ((t37_m & hy3) ^ M1ORM2);
assign z10_m = t37_m;
assign z11 = ((t33 & y4) ^ ((t33 & y4_m) ^ y4_m)) ^ ((t33_m & y4) ^ M1ORM2);
assign z11_m = t33_m;
assign z12 = ((t43 & y13) ^ ((t43 & y13_m) ^ y13_m)) ^ ((t43_m & y13) ^ M1ORM2);
assign z12_m = t43_m;
assign z13 = ((y5 & t40) ^ ((y5 & t40_m) ^ t40_m)) ^ ((y5_m & t40) ^ M1ORM2);
assign z13_m = y5_m;
assign z14 = ((t29 & y2) ^ ((t29 & y2_m) ^ y2_m)) ^ ((t29_m & y2) ^ M1ORM2);
assign z14_m = t29_m;
assign z15 = ((y9 & t42) ^ ((y9 & t42_m) ^ t42_m)) ^ ((y9_m & t42) ^ M1ORM2);
assign z15_m = y9_m;
assign z16 = ((y14 & t45) ^ ((y14 & t45_m) ^ t45_m)) ^ ((y14_m & t45) ^ M1ORM2);
assign z16_m = y14_m;
assign z17 = ((t41 & y8) ^ ((t41 & y8_m) ^ y8_m)) ^ ((t41_m & y8) ^ M1ORM2);
assign z17_m = t41_m;
assign tc1 = z15 ^ z16; 
assign tc1_m = MASK1;
assign tc2 = z10 ^ tc1; 
assign tc2_m = MASK2;
assign tc3 = z9 ^ tc2; 
assign tc3_m = MASK3;
assign tc4 = z0 ^ z2; 
assign tc4_m = MASK2;
assign tc5 = z1 ^ z0; 
assign tc5_m = MASK3;
assign tc6 = z3 ^ z4; 
assign tc6_m = MASK2;
assign tc7 = z12 ^ tc4; 
assign tc7_m = MASK1;
assign tc8 = z7 ^ tc6; 
assign tc8_m = MASK3;
assign tc9 = z8 ^ tc7; 
assign tc9_m = MASK2;
assign tc10 = tc8 ^ tc9; 
assign tc10_m = MASK1;
assign tc11 = tc6 ^ tc5; 
assign tc11_m = MASK1;
assign tc12 = z3 ^ z5; 
assign tc12_m = MASK3;
assign tc13 = z13 ^ tc1; 
assign tc13_m = MASK3;
assign tc14 = tc4 ^ tc12; 
assign tc14_m = MASK1;
assign S3 = tc3 ^ tc11; 
assign S3_m = MASK2;
assign tc16 = z6 ^ tc8; 
assign tc16_m = MASK1;
assign tc17 = z14 ^ tc10; 
assign tc17_m = MASK3;
assign tc18 = tc13 ^ tc14; 
assign tc18_m = MASK2;
assign S7 = ~(z12 ^ tc18); 
assign S7_m = MASK1;
assign tc20 = z15 ^ tc16; 
assign tc20_m = MASK2;
assign tc21 = tc2 ^ z11; 
assign tc21_m = MASK1;
assign S0 = tc3 ^ tc16; 
assign S0_m = MASK2;
assign S6 = ~(tc10 ^ tc18); 
assign S6_m = MASK3;
assign S4 = tc14 ^ S3; 
assign S4_m = MASK3;
assign S1 = ~(S3 ^ tc16); 
assign S1_m = MASK3;
assign tc26 = tc17 ^ tc20; 
assign tc26_m = MASK1;
assign S2 = ~(tc26 ^ z17); 
assign S2_m = MASK3;
assign S5 = tc21 ^ tc17; 
assign S5_m = MASK2;
assign o7 = S0; 
assign o7_m = MASK2;
assign o6 = S1 ^ MASK2; 
assign o6_m = MASK1;
assign o5 = S2 ^ MASK1; 
assign o5_m = MASK2;
assign o4 = S3 ^ MASK3; 
assign o4_m = MASK1;
assign o3 = S4 ^ MASK2; 
assign o3_m = MASK1;
assign o2 = S5 ^ MASK1; 
assign o2_m = MASK3;
assign o1 = S6; 
assign o1_m = MASK3;
assign o0 = S7 ^ MASK3; 
assign o0_m = MASK2;

 endmodule // aes_sbox
