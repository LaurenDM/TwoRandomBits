module mixcolumns (
		   // a0x1 => a0 &  x1 => bit 1 
		   input  a0x0, a1x0, a2x0, a3x0, a0x1, a1x1, a2x1, a3x1, a0x2, a1x2, a2x2, a3x2, a0x3, a1x3, a2x3, a3x3, a0x4, a1x4, a2x4, a3x4, a0x5, a1x5, a2x5, a3x5, a0x6, a1x6, a2x6, a3x6, a0x7, a1x7, a2x7, a3x7,
		   output b0x0, b1x0, b2x0, b3x0, b0x1, b1x1, b2x1, b3x1, b0x2, b1x2, b2x2, b3x2, b0x3, b1x3, b2x3, b3x3, b0x4, b1x4, b2x4, b3x4, b0x5, b1x5, b2x5, b3x5, b0x6, b1x6, b2x6, b3x6, b0x7, b1x7, b2x7, b3x7
           );
  /* i0 -> 2, i1 -> 3, i2 -> 3, i3 -> 1, i4 -> 1, i5 -> 2, i6 -> 1, i7 -> 2, */
   
   assign ha0x0 = a0x0 ^ MASK1;
   assign a0_mul_2x0 = a0x7;
   assign a0_mul_2x1 = ha0x0 ^ a0x7;
   assign a0_mul_2x2 = a0x1;
   assign a0_mul_2x3 = a0x2 ^ a0x7;
   assign a0_mul_2x4 = a0x3 ^ a0x7;
   assign a0_mul_2x5 = a0x4;
   assign a0_mul_2x6 = a0x5;
   assign a0_mul_2x7 = a0x6;
   
   // 2*a1
   assign ha1x0 = a1x0 ^ MASK1;
   assign a1_mul_2x0 = a1x7;
   assign a1_mul_2x1 = ha1x0 ^ a1x7;
   assign a1_mul_2x2 = a1x1;
   assign a1_mul_2x3 = a1x2 ^ a1x7;
   assign a1_mul_2x4 = a1x3 ^ a1x7;
   assign a1_mul_2x5 = a1x4;
   assign a1_mul_2x6 = a1x5;
   assign a1_mul_2x7 = a1x6;

   // 2*a2
   assign ha2x0 = a2x0 ^ MASK1;
   assign a2_mul_2x0 = a2x7;
   assign a2_mul_2x1 = ha2x0 ^ a2x7;
   assign a2_mul_2x2 = a2x1;
   assign a2_mul_2x3 = a2x2 ^ a2x7;
   assign a2_mul_2x4 = a2x3 ^ a2x7;
   assign a2_mul_2x5 = a2x4;
   assign a2_mul_2x6 = a2x5;
   assign a2_mul_2x7 = a2x6;

   // 2*a3
   assign ha3x0 = a3x0 ^ MASK1;
   assign a3_mul_2x0 = a3x7;
   assign a3_mul_2x1 = ha3x0 ^ a3x7;
   assign a3_mul_2x2 = a3x1;
   assign a3_mul_2x3 = a3x2 ^ a3x7;
   assign a3_mul_2x4 = a3x3 ^ a3x7;
   assign a3_mul_2x5 = a3x4;
   assign a3_mul_2x6 = a3x5;
   assign a3_mul_2x7 = a3x6;
   
    // 3*a0= 2 * a0+ a0
   assign ha0_mul_2x0 =  a0_mul_2x0 ^ MASK1;
   assign ha0_mul_2x2 =  a0_mul_2x2 ^ MASK1;
   assign ha0_mul_2x3 =  a0_mul_2x3 ^ MASK2;
   assign a0_mul_3x0 = ha0_mul_2x0 ^ a0x0;
   assign a0_mul_3x1 = a0_mul_2x1 ^ a0x1;
   assign a0_mul_3x2 = ha0_mul_2x2 ^ a0x2;
   assign a0_mul_3x3 = ha0_mul_2x3 ^ a0x3;
   assign a0_mul_3x4 = a0_mul_2x4 ^ a0x4;
   assign a0_mul_3x5 = a0_mul_2x5 ^ a0x5;
   assign a0_mul_3x6 = a0_mul_2x6 ^ a0x6;
   assign a0_mul_3x7 = a0_mul_2x7 ^ a0x7;
   
   // 3*a1= 2 * a1+ a1
   assign ha1_mul_2x0 =  a1_mul_2x0 ^ MASK1;
   assign ha1_mul_2x2 =  a1_mul_2x2 ^ MASK1;
   assign ha1_mul_2x3 =  a1_mul_2x3 ^ MASK2;
   assign a1_mul_3x0 = ha1_mul_2x0 ^ a1x0;
   assign a1_mul_3x1 = a1_mul_2x1 ^ a1x1;
   assign a1_mul_3x2 = ha1_mul_2x2 ^ a1x2;
   assign a1_mul_3x3 = ha1_mul_2x3 ^ a1x3;
   assign a1_mul_3x4 = a1_mul_2x4 ^ a1x4;
   assign a1_mul_3x5 = a1_mul_2x5 ^ a1x5;
   assign a1_mul_3x6 = a1_mul_2x6 ^ a1x6;
   assign a1_mul_3x7 = a1_mul_2x7 ^ a1x7;

   // 3*a2= 2 * a2+ a2
   assign ha2_mul_2x0 =  a2_mul_2x0 ^ MASK1;
   assign ha2_mul_2x2 =  a2_mul_2x2 ^ MASK1;
   assign ha2_mul_2x3 =  a2_mul_2x3 ^ MASK2;
   assign a2_mul_3x0 = ha2_mul_2x0 ^ a2x0;
   assign a2_mul_3x1 = a2_mul_2x1 ^ a2x1;
   assign a2_mul_3x2 = ha2_mul_2x2 ^ a2x2;
   assign a2_mul_3x3 = ha2_mul_2x3 ^ a2x3;
   assign a2_mul_3x4 = a2_mul_2x4 ^ a2x4;
   assign a2_mul_3x5 = a2_mul_2x5 ^ a2x5;
   assign a2_mul_3x6 = a2_mul_2x6 ^ a2x6;
   assign a2_mul_3x7 = a2_mul_2x7 ^ a2x7;

   // 3*a3= 2 * a3+ a3
   assign ha3_mul_2x0 =  a3_mul_2x0 ^ MASK1;
   assign ha3_mul_2x2 =  a3_mul_2x2 ^ MASK1;
   assign ha3_mul_2x3 =  a3_mul_2x3 ^ MASK2;
   assign a3_mul_3x0 = ha3_mul_2x0 ^ a3x0;
   assign a3_mul_3x1 = a3_mul_2x1 ^ a3x1;
   assign a3_mul_3x2 = ha3_mul_2x2 ^ a3x2;
   assign a3_mul_3x3 = ha3_mul_2x3 ^ a3x3;
   assign a3_mul_3x4 = a3_mul_2x4 ^ a3x4;
   assign a3_mul_3x5 = a3_mul_2x5 ^ a3x5;
   assign a3_mul_3x6 = a3_mul_2x6 ^ a3x6;
   assign a3_mul_3x7 = a3_mul_2x7 ^ a3x7;

   // b0 = 2*a0 + 3*a1 + 1*a2 + 1*a3
   assign Ab0x0 = a0_mul_2x0 ^ a1_mul_3x0;
   assign Ab0x1 = a0_mul_2x1 ^ a1_mul_3x1;
   assign Ab0x2 = a0_mul_2x2 ^ a1_mul_3x2;
   assign Ab0x3 = a0_mul_2x3 ^ a1_mul_3x3;
   assign Ab0x4 = a0_mul_2x4 ^ a1_mul_3x4;
   assign Ab0x5 = a0_mul_2x5 ^ a1_mul_3x5;
   assign Ab0x6 = a0_mul_2x6 ^ a1_mul_3x6;
   assign Ab0x7 = a0_mul_2x7 ^ a1_mul_3x7;
   assign ha3x1 = a3x1 ^ MASK1;
   assign ha3x2 = a3x2 ^ MASK1;
   assign ha3x3 = a3x3 ^ MASK2;
   assign ha3x4 = a3x4 ^ MASK2;
   assign ha3x5 = a3x5 ^ MASK1;
   assign ha3x6 = a3x6 ^ MASK2;
   assign ha3x7 = a3x7 ^ MASK1;
   assign Bb0x0 = ha2x0    ^ a3x0;
   assign Bb0x1 = a2x1    ^ ha3x1;
   assign Bb0x2 = a2x2    ^ ha3x2;
   assign Bb0x3 = a2x3    ^ ha3x3;
   assign Bb0x4 = a2x4    ^ ha3x4;
   assign Bb0x5 = a2x5    ^ ha3x5;
   assign Bb0x6 = a2x6    ^ ha3x6;
   assign Bb0x7 = a2x7    ^ ha3x7;
   assign b0x0 = Ab0x0 ^ Bb0x0;
   assign hb0x1 = Ab0x1 ^ Bb0x1;
   assign b0x1 = hb0x1 ^ MASK1;
   assign hb0x2 = Ab0x2 ^ Bb0x2;
   assign b0x2 = hb0x2;
   assign b0x3 = Ab0x3 ^ Bb0x3;
   assign hb0x4 = Ab0x4 ^ Bb0x4;
   assign b0x4 = hb0x4 ^ MASK2;
   assign hb0x5 = Ab0x5 ^ Bb0x5;
   assign b0x5 = hb0x5 ^ MASK1;
   assign hb0x6 = Ab0x6 ^ Bb0x6;
   assign b0x6 = hb0x6 ^ MASK2;
   assign hb0x7 = Ab0x7 ^ Bb0x7;
   assign b0x7 = hb0x7 ^ MASK1;
   
   // b1 = 1*a0 + 2*a1 + 3*a2 + 1*a3
   assign Ab1x0 = ha0x0    ^ a1_mul_2x0;
   assign Ab1x1 = a0x1    ^ a1_mul_2x1;
   assign Ab1x2 = a0x2    ^ ha1_mul_2x2;
   assign Ab1x3 = a0x3    ^ ha1_mul_2x3;
   assign Ab1x4 = a0x4    ^ a1_mul_2x4;
   assign Ab1x5 = a0x5    ^ a1_mul_2x5;
   assign Ab1x6 = a0x6    ^ a1_mul_2x6;
   assign Ab1x7 = a0x7    ^ a1_mul_2x7;
   assign Bb1x0 = a2_mul_3x0 ^ a3x0;
   assign Bb1x1 = a2_mul_3x1 ^ a3x1;
   assign Bb1x2 = a2_mul_3x2 ^ a3x2;
   assign Bb1x3 = a2_mul_3x3 ^ a3x3;
   assign Bb1x4 = a2_mul_3x4 ^ a3x4;
   assign Bb1x5 = a2_mul_3x5 ^ a3x5;
   assign Bb1x6 = a2_mul_3x6 ^ a3x6;
   assign Bb1x7 = a2_mul_3x7 ^ a3x7;
   assign b1x0 = Ab1x0 ^ Bb1x0;
   assign b1x1 = Ab1x1 ^ Bb1x1;
   assign b1x2 = Ab1x2 ^ Bb1x2;
   assign b1x3 = Ab1x3 ^ Bb1x3;
   assign b1x4 = Ab1x4 ^ Bb1x4;
   assign b1x5 = Ab1x5 ^ Bb1x5;
   assign b1x6 = Ab1x6 ^ Bb1x6;
   assign b1x7 = Ab1x7 ^ Bb1x7;
   
   // b2 = 1*a0 + 1*a1 + 2*a2 + 3*a3
   assign ha0x1 = a0x1 ^ MASK1;
   assign ha0x2 = a0x2 ^ MASK1;
   assign ha0x3 = a0x3 ^ MASK2;
   assign ha0x4 = a0x4 ^ MASK2;
   assign ha0x5 = a0x5 ^ MASK1;
   assign ha0x6 = a0x6 ^ MASK2;
   assign ha0x7 = a0x7 ^ MASK1;
   assign Ab2x0 = ha0x0    ^ a1x0;
   assign Ab2x1 = ha0x1    ^ a1x1;
   assign Ab2x2 = ha0x2    ^ a1x2;
   assign Ab2x3 = ha0x3    ^ a1x3;
   assign Ab2x4 = ha0x4    ^ a1x4;
   assign Ab2x5 = ha0x5    ^ a1x5;
   assign Ab2x6 = ha0x6    ^ a1x6;
   assign Ab2x7 = ha0x7    ^ a1x7;
   assign Bb2x0 = a2_mul_2x0 ^ a3_mul_3x0;
   assign Bb2x1 = a2_mul_2x1 ^ a3_mul_3x1;
   assign Bb2x2 = a2_mul_2x2 ^ a3_mul_3x2;
   assign Bb2x3 = a2_mul_2x3 ^ a3_mul_3x3;
   assign Bb2x4 = a2_mul_2x4 ^ a3_mul_3x4;
   assign Bb2x5 = a2_mul_2x5 ^ a3_mul_3x5;
   assign Bb2x6 = a2_mul_2x6 ^ a3_mul_3x6;
   assign Bb2x7 = a2_mul_2x7 ^ a3_mul_3x7;
   assign b2x0 = Ab2x0 ^ Bb2x0;
   assign hb2x1 = Ab2x1 ^ Bb2x1;
   assign b2x1 = hb2x1 ^ MASK1;
   assign b2x2 = Ab2x2 ^ Bb2x2;
   assign b2x3 = Ab2x3 ^ Bb2x3;
   assign hb2x4 = Ab2x4 ^ Bb2x4;
   assign b2x4 = hb2x4 ^ MASK2;
   assign hb2x5 = Ab2x5 ^ Bb2x5;
   assign b2x5 = hb2x5 ^ MASK1;
   assign hb2x6 = Ab2x6 ^ Bb2x6;
   assign b2x6 = hb2x6 ^ MASK2;
   assign hb2x7 = Ab2x7 ^ Bb2x7;
   assign b2x7 = hb2x7 ^ MASK1;

   // b3 = 3*a0 + 1*a1 + 1*a2 + 2*a3
   assign Ab3x0 = a0_mul_3x0 ^ a1x0;
   assign Ab3x1 = a0_mul_3x1 ^ a1x1;
   assign Ab3x2 = a0_mul_3x2 ^ a1x2;
   assign Ab3x3 = a0_mul_3x3 ^ a1x3;
   assign Ab3x4 = a0_mul_3x4 ^ a1x4;
   assign Ab3x5 = a0_mul_3x5 ^ a1x5;
   assign Ab3x6 = a0_mul_3x6 ^ a1x6;
   assign Ab3x7 = a0_mul_3x7 ^ a1x7;
   assign Bb3x0 = ha2x0    ^ a3_mul_2x0;
   assign Bb3x1 = a2x1    ^ a3_mul_2x1;
   assign Bb3x2 = a2x2    ^ ha3_mul_2x2;
   assign Bb3x3 = a2x3    ^ ha3_mul_2x3;
   assign Bb3x4 = a2x4    ^ a3_mul_2x4;
   assign Bb3x5 = a2x5    ^ a3_mul_2x5;
   assign Bb3x6 = a2x6    ^ a3_mul_2x6;
   assign Bb3x7 = a2x7    ^ a3_mul_2x7;
   assign b3x0 = Ab3x0 ^ Bb3x0;
   assign b3x1 = Ab3x1 ^ Bb3x1;
   assign b3x2 = Ab3x2 ^ Bb3x2;
   assign b3x3 = Ab3x3 ^ Bb3x3;
   assign b3x4 = Ab3x4 ^ Bb3x4;
   assign b3x5 = Ab3x5 ^ Bb3x5;
   assign b3x6 = Ab3x6 ^ Bb3x6;
   assign b3x7 = Ab3x7 ^ Bb3x7;

endmodule // mixcolumns