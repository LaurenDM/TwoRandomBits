// Code your design here
// Description     : Calculates the AES Sbox function Boyar Matthews Peralta

/* The top-level module */
module aes_sbox (
       /* Ports */
       input   i0, i1, i2, i3, i4, i5, i6, i7,
       output o0, o1, o2, o3, o4, o5, o6, o7
       ) ;
   
   assign MASK3 = MASK1 ^ MASK2;
    
   assign y14 = i4 ^ i2;
   assign y13 = i7 ^ i1;
   assign hy13 = y13 ^ MASK2;
   assign y9 = i7 ^ i4;
   assign hy9 = y9 ^ MASK2;
   assign y8 = i7 ^ i2;
   assign t0 = i6 ^ i5;
   assign y1 = t0 ^ i0;
   assign hy1 = y1 ^ MASK2;
   assign y4 = hy1 ^ i4;
   assign hy4 = y4 ^ MASK1;
   assign y12 = y13 ^ y14;
   assign y2 = y1 ^ i7;
   assign y5 = y1 ^ i1;
   assign y3 = y5 ^ y8;
   assign hy3 = y3 ^ MASK2;
   assign t1 = i3 ^ y12;
   assign y15 = t1 ^ i2;
   assign hy15 = y15 ^ MASK2;
   assign y20 = t1 ^ i6;
   assign y6 = y15 ^ i0;
   assign hy6 = y6 ^ MASK1;
   assign y10 = y15 ^ t0;
   assign hy10 = y10 ^ MASK1;
   assign y11 = y20 ^ hy9;
   assign hy11 = y11 ^ MASK1;
   assign y7 = i0 ^ hy11;
   assign y17 = y10 ^ hy11;
   assign y19 = y10 ^ y8;
   assign y16 = t0 ^ y11;
   assign y21 = hy13 ^ y16;
   assign y18 = i7 ^ y16;
   assign t2 = y12 & y15;
   assign t3 = hy3 & y6;
   assign t4 = t3 ^ t2;
   assign t5 = hy4 & i0;
   assign t6 = t5 ^ t2;
   assign t7 = hy13 & y16;
   assign t8 = y5 & y1;
   assign t9 = t8 ^ t7;
   assign t10 = y2 & y7;
   assign t11 = t10 ^ t7;
   assign t12 = y9 & y11;
   assign t13 = y14 & y17;
   assign t14 = t13 ^ t12;
   assign t15 = y8 & y10;
   assign t16 = t15 ^ t12;
   assign t17 = t4 ^ y20;
   assign t18 = t6 ^ t16;
   assign t19 = t9 ^ t14;
   assign t20 = t11 ^ t16;
   assign t21 = t17 ^ t14;
   assign t22 = t18 ^ y19;
   assign t23 = t19 ^ y21;
   assign ht23 = t23 ^ MASK1;
   assign t24 = t20 ^ y18;
   assign ht24 = t24 ^ MASK1;
   assign t25 = t21 ^ t22;
   assign t26 = t21 & t23;
   assign t27 = t24 ^ t26;
   assign t28 = t25 & t27;
   assign t29 = t28 ^ t22;
   assign t30 = t23 ^ t24;
   assign t31 = t22 ^ t26;
   assign t32 = t31 & t30;
   assign t33 = t32 ^ t24;
   assign ht33 = t33 ^ MASK1;
   assign t34 = ht23 ^ t33;
   assign t35 = t27 ^ t33;
   assign t36 = ht24 & t35;
   assign t37 = t36 ^ t34;
   assign t38 = t27 ^ t36;
   assign t39 = t29 & t38;
   assign t40 = t25 ^ t39;
   assign t41 = t40 ^ t37;
   assign t42 = t29 ^ t33;
   assign t43 = t29 ^ t40;
   assign t44 = ht33 ^ t37;
   assign t45 = t42 ^ t41;
   assign z0 = t44 & hy15;
   assign z1 = t37 & hy6;
   assign z2 = t33 & i0;
   assign z3 = t43 & y16;
   assign z4 = t40 & hy1;
   assign z5 = t29 & y7;
   assign z6 = t42 & y11;
   assign z7 = t45 & y17;
   assign z8 = t41 & hy10;
   assign z9 = t44 & y12;
   assign z10 = t37 & hy3;
   assign z11 = t33 & y4;
   assign z12 = t43 & y13;
   assign z13 = t40 & y5;
   assign z14 = t29 & y2;
   assign z15 = t42 & y9;
   assign z16 = t45 & y14;
   assign z17 = t41 & y8;
   assign tc1 = z15 ^ z16;
   assign tc2 = z10 ^ tc1;
   assign tc3 = z9 ^ tc2;
   assign tc4 = z0 ^ z2;
   assign tc5 = z1 ^ z0;
   assign tc6 = z3 ^ z4;
   assign tc7 = z12 ^ tc4;
   assign tc8 = z7 ^ tc6;
   assign tc9 = z8 ^ tc7;
   assign tc10 = tc8 ^ tc9;
   assign tc11 = tc6 ^ tc5;
   assign tc12 = z3 ^ z5;
   assign tc13 = z13 ^ tc1;
   assign tc14 = tc4 ^ tc12;
   assign S3 = tc3 ^ tc11;
   assign tc16 = z6 ^ tc8;
   assign tc17 = z14 ^ tc10;
   assign tc18 = tc13 ^ tc14;
   assign S7 = ~(z12 ^ tc18);
   assign tc20 = z15 ^ tc16;
   assign tc21 = tc2 ^ z11;
   assign S0 = tc3 ^ tc16;
   assign S6 = ~(tc10 ^ tc18);
   assign S4 = tc14 ^ S3;
   assign S1 = ~(S3 ^ tc16);
   assign tc26 = tc17 ^ tc20;
   assign S2 = ~(tc26 ^ z17);
   assign S5 = tc21 ^ tc17;
   
   //Output mapping
   assign o7 = S0;
   assign o6 = S1 ^ MASK2;
   assign o5 = S2 ^ MASK1;
   assign o4 = S3 ^ MASK3;
   assign o3 = S4 ^ MASK2;
   assign o2 = S5 ^ MASK1;
   assign o1 = S6;
   assign o0 = S7 ^ MASK3;

endmodule // aes_sbox
