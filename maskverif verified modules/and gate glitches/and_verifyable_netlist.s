read_verilog and.v;
hierarchy -check -top and_gate;
proc;
flatten;
opt;
memory;
opt;
techmap;
opt;
write_ilang and.ilang;
