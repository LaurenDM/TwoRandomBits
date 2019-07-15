module and_gate(
input   clk,
input   a0, a1,
input   b0, b1,
output  q0, q1
);

   wire t1,t2,t3,t4,t5,t6;
   reg mask1ormask2; // this is normally precomputed
   reg r1,r2,r3,r4,r5;


   // and gate 
   assign t1 = a0&b0;
   assign t2 = a0&b1 ^ b1;
   assign t4 = a1&b0;

   assign t3 = r1 ^ r2;
   assign t5 = r4 ^ mask1ormask2;

   assign t6 = r3 ^ r5;


   always @ (posedge clk) begin 
      mask1ormask2 <= a1|b1;
      r1 <= t1;
      r2 <= t2;
      r3 <= t3;
      r4 <= t4;
      r5 <= t5;
      q0 <= t6;
      q1 <= a1;
   end 

        
endmodule
