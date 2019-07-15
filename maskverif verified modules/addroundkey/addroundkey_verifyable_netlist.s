read_verilog addroundkey.v;
flatten;
techmap;
delete add* ;
cd verification_wrapper;
stat;
show;
write_ilang addroundkey.ilang;
