read_verilog mixcolumns.v;
flatten;
techmap;
delete mix* ;
cd verification_wrapper;
stat;
show;
write_ilang mixcolumns.ilang;
