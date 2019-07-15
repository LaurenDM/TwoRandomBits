read_verilog sbox.v;
flatten;
opt;
techmap;
delete aes* ;
cd verification_wrapper;
stat;
show;
write_ilang top.ilang;
