module verification_wrapper(
   input m0, m1,
   input a0_0, a1_0, a2_0, a3_0, a4_0, a5_0, a6_0, a7_0, b0_0, b1_0, b2_0, b3_0, b4_0, b5_0, b6_0, b7_0,
   input a0_1, a1_1, a2_1, a3_1, a4_1, a5_1, a6_1, a7_1, b0_1, b1_1, b2_1, b3_1, b4_1, b5_1, b6_1, b7_1,
   output o0, o1, o2, o3, o4, o5, o6, o7);

      // Ensure mask encoding and relation as we assume
      // i      
      assign i0 = (a0_0 ^ m1) ^ a0_1;      // 2
      assign i1 = (a1_0 ^ m0 ^ m1) ^ a1_1; // 3 
      assign i2 = (a2_0 ^ m0 ^ m1) ^ a2_1; // 3 
      assign i3 = (a3_0 ^ m0) ^ a3_1;      // 1 
      assign i4 = (a4_0 ^ m0) ^ a4_1;      // 1 
      assign i5 = (a5_0 ^ m1) ^ a5_1;      // 2 
      assign i6 = (a6_0 ^ m0) ^ a6_1;      // 1 
      assign i7 = (a7_0 ^ m1) ^ a7_1;      // 2   

      // k      
      assign k0 = (b0_0 ^ m1) ^ b0_1;      // 2
      assign k1 = (b1_0 ^ m0 ^ m1) ^ b1_1; // 3 
      assign k2 = (b2_0 ^ m0 ^ m1) ^ b2_1; // 3 
      assign k3 = (b3_0 ^ m0) ^ b3_1;      // 1 
      assign k4 = (b4_0 ^ m0) ^ b4_1;      // 1 
      assign k5 = (b5_0 ^ m1) ^ b5_1;      // 2 
      assign k6 = (b6_0 ^ m0) ^ b6_1;      // 1 
      assign k7 = (b7_0 ^ m1) ^ b7_1;      // 2   
      
      // DUV
    addroundkey addroundkey_ins(
   m0, m1,
   i0, i1, i2, i3, i4, i5, i6, i7, k0, k1, k2, k3, k4, k5, k6, k7,
   o0, o1, o2, o3, o4, o5, o6, o7);
   
endmodule

module addroundkey(
   input MASK1, MASK2,
   input  i0, i1, i2, i3, i4, i5, i6, i7, k0, k1, k2, k3, k4, k5, k6, k7,
   output o0, o1, o2, o3, o4, o5, o6, o7) ;

   assign MASK12 = MASK1 ^ MASK2; 
   assign mk0 = k0 ^ MASK1; 
   assign mk1 = k1 ^ MASK1; 
   assign mk2 = k2 ^ MASK1; 
   assign mk3 = k3 ^ MASK2; 
   assign mk4 = k4 ^ MASK2; 
   assign mk5 = k5 ^ MASK1; 
   assign mk6 = k6 ^ MASK2; 
   assign mk7 = k7 ^ MASK1; 
   assign mo0 = i0 ^ mk0; 
   assign mo1 = i1 ^ mk1; 
   assign mo2 = i2 ^ mk2; 
   assign mo3 = i3 ^ mk3; 
   assign mo4 = i4 ^ mk4; 
   assign mo5 = i5 ^ mk5; 
   assign mo6 = i6 ^ mk6; 
   assign mo7 = i7 ^ mk7; 
   assign o0 = mo0 ^ MASK12; 
   assign o1 = mo1 ^ MASK2; 
   assign o2 = mo2 ^ MASK2; 
   assign o3 = mo3 ^ MASK12; 
   assign o4 = mo4 ^ MASK12; 
   assign o5 = mo5 ^ MASK12; 
   assign o6 = mo6 ^ MASK12; 
   assign o7 = mo7 ^ MASK12; 

endmodule // addroundkey