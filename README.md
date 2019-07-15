# README

## Contents

-"synthesizer and checker src\":    C# source code of our mask checking and synthesis tool requires the installation of Z3 and adaption of the source code to its environment. Tested with MSVS 2015 V 14.0.25424.00 and MS .NET Framework 4.7.02558

-"unprotected modules\":         The unprotected Verilog modules that serve as the source of the synthesis tool.

-"maskverif verified modules\":     The tested and verified masked modules: verilog code, yosis generated .ilang format and, maskverif input .mv and verification output
   - "addroundkey\", "aes sbox\", "mixcolumn\" : automatically generated code by the synthesis tool
   - "and gate composed\":       manual implementation of the new AND gate and its composition with XOR or another AND
   - "and gate glithces\":       manual implementation of the new AND gate with registers against glitches

-"m4-implementation\":          The tested full AES-128-CTR optimized software implementation based on the hardware implementation.


## How to use the synthesizer and checker tool
The tool is subdivided into five steps as highlighted by the regions in the code:

### 1. Configuration:

There are several options in the Configuration region, to define which input file should be used and how to treat them. 
Per default, the Sbox design is targeted. By setting one of the following switches, the MixColumns or AddRoundkey circuit is selected instead:
   - do_mixcolumns
   - do_add_roundkey

The "do_make_output_and_input_mapping_equal" switch forces a solution that has the same active mask for the ith input and output bit. 
For MixColumns and AddRoundKey a concrete mask encoding is enforced as defined in the function "getInputConstraintsForMixColumns()".

The "do_optimize_second_domain" switch removes unnecessary logic for the second mask domain (second share of each variable) and replaces it with the resulting mask instead.

### 2. Parsing inputs:
Reads the input files according to the settings in the configuration region and parses it into a list containing the sequence of the instructions and the operands and destination variable.

### 3. Create SMT formulas:
This step is described in more detail in the paper. Basically, the constraints for the subsequent search for a valid masked realization are defined including the input masking constraints, the propagation and safety rules for respective gates, as well as the output constraints.

### 4. Use Z3 to find secure mask mapping
In this part, the Z3 theorem solver is used to find a possible solution for the input mask encoding.
However, if the input mask encoding is already defined, as automatically used for MixColumns and AddRoundKey, this step becomes a pure security evaluation.

### 5. Parse Z3 output and write Verilog file
Writes the new module description in masked form, e.g., replaces the AND function of the original circuit with the probing secure masked variant from the paper.
For linear gates (XOR, XNOR) the original function is duplicated if the "do_optimize_second_domain" switch is set to false. Otherwise, the information which masks appear on which gate is used to replace the second domain with the resulting mask which saves unnecessary logic.


## Parsing and synthesizing a new input file
We first note that the tool is not designed as generic and out-of-the-box synthesis and verification tool.
Adding a new input file thus requires some modifications of the source code in "Program.cs". In the following, we discuss the most important steps to do so.

### 1. The targeted design file must follow the same design rules as the modules used for the paper:
   - Verilog style module definition with "input" and "output" keywords
   - Use only one-bit signals for ports and wires
   - Inputs and outputs should be enumerated, e.g., i0, i1,... i7 if the "do_make_output_and_input_mapping_equal" switch should be used
   - The modules consist of SSA style "assign" statements (one per line) only
   - The used gates are either assignments "=", XOR "^", AND "&", or XNOR "~(... ^ ...)". Other gate types need to be added manually to the source code

### 2. Adding a new input file
   - Add a "do_..." switch and modify the path of the StreamReader in the "Parsing Input" region accordingly
   - The switch also helps in modifying input file specific treatment in the code where required
   - The next step "Create SMT formulas" should work without throwing an error if the targeted design follows the design rules above

### 3. The next step "Use Z3 to find secure mask mapping" needs to be executed iteratively:
   - Remove all but one line of SSA code in the design file
   - Add the lines of code until the verification step fails
   - Use the information from the last step to see which signal needs to change its maks and modify the SSA code accordingly by adding an XOR with one of the masks for the affected signal (e.g., "assign ht8 = T8 ^ MASK1", in "aes_sbox_boyar_peralata.v")
   - These steps can be automated for larger projects, but the functionality is not implemented at the moment
   - After all lines of code are added to the input file, and the Z3 call generates a satisfiable model, the generation of the output file should work automatically. However, cosmetic modifications like module names and comments might be necessary.





authors: Hannes Gross, Ko Stoffelen, Lauren De Meyer




