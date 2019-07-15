module and_and_gate(
input   clk,
input   a0, a1,
input   b0, b1,
output  m0, m1
);

   wire t1,t2,t3,t4,t5,q0,q1,s1,s2,s3,s4,s5;
   wire mask1ormask2;


   // first and gate
   assign t1 = a0&b0;
   assign t2 = a0&b1 ^ b1;
   assign t4 = a1&b0;
   assign mask1ormask2 = a1|b1;

   assign t3 = t1 ^ t2;
   assign t5 = t4 ^ mask1ormask2;

   assign q0 = t3 ^ t5;
   assign q1 = a1;

   // second and gate
   assign s1 = q0&b0;
   assign s2 = q0&b1 ^ b1;
   assign s4 = q1&b0;

   assign s3 = s1 ^ s2;
   assign s5 = s4 ^ mask1ormask2;

   assign m0 = s3 ^ s5;
   assign m1 = q1;

        
endmodule