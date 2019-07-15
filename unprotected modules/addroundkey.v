module addroundkey (
		   // s...state, k...key
		   input  i0, i1, i2, i3, i4, i5, i6, i7, k0, k1, k2, k3, k4, k5, k6, k7,
           output o0, o1, o2, o3, o4, o5, o6, o7
           );
           
           /* i0 -> 2, i1 -> 3, i2 -> 3, i3 -> 1, i4 -> 1, i5 -> 2, i6 -> 1, i7 -> 2, */
           assign MASK12 = MASK1 ^ MASK2;
           assign mk0 = k0 ^ MASK1; // 2 --> 3
           assign mk1 = k1 ^ MASK1; // 3 --> 2
           assign mk2 = k2 ^ MASK1; // 3 --> 2
           assign mk3 = k3 ^ MASK2; // 1 --> 3
           assign mk4 = k4 ^ MASK2; // 1 --> 3
           assign mk5 = k5 ^ MASK1; // 2 --> 3
           assign mk6 = k6 ^ MASK2; // 1 --> 3
           assign mk7 = k7 ^ MASK1; // 2 --> 3
           
           assign mo0 = i0 ^ mk0;   // 3 --> 1
           assign mo1 = i1 ^ mk1;   // 2 --> 1
           assign mo2 = i2 ^ mk2;   // 2 --> 1  
           assign mo3 = i3 ^ mk3;   // 3 --> 2
           assign mo4 = i4 ^ mk4;   // 3 --> 2
           assign mo5 = i5 ^ mk5;   // 3 --> 1
           assign mo6 = i6 ^ mk6;   // 3 --> 2
           assign mo7 = i7 ^ mk7;   // 3 --> 1            
           
           assign o0 = mo0 ^ MASK12;  // 1 --> 2
           assign o1 = mo1 ^ MASK2;   // 1 --> 3
           assign o2 = mo2 ^ MASK2;   // 1 --> 3  
           assign o3 = mo3 ^ MASK12;  // 2 --> 1
           assign o4 = mo4 ^ MASK12;  // 2 --> 1
           assign o5 = mo5 ^ MASK12;  // 1 --> 2
           assign o6 = mo6 ^ MASK12;  // 2 --> 1
           assign o7 = mo7 ^ MASK12;  // 1 --> 2 
           
endmodule // addroundkey
