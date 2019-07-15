module and_gate(
input   a0, a1,
input   b0, b1,
output  q0, q1
); 

     wire t1,t2,t3,t4,t5;
     wire mask1ormask2;

    // and gate 
   assign t1 = a0&b0;
   assign t2 = a0&b1 ^ b1;
   assign t4 = a1&b0;
   assign mask1ormask2 = a1|b1;

   assign t3 = t1 ^ t2;
   assign t5 = t4 ^ mask1ormask2;

   assign q0 = t3 ^ t5;
   assign q1 = a1;
        
endmodule