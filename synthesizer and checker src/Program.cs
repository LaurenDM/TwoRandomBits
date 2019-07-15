using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;

namespace BoyarPeralta2ShareswithZ3
{
    class Program
    {
        static string getMaskNameFromNumber(string mask_num)
        {
            if (mask_num == "1") return "MASK1_1";
            if (mask_num == "2") return "MASK2_1";
            if (mask_num == "3") return "MASK1_1 ^ MASK2_1";
            return "ERROR";
        }
        static string getInputConstraintsForMixColumns(string port_name_ending)
        {
            switch(port_name_ending)
            {
                case "0": return "2";
                case "1": return "3";
                case "2": return "3";
                case "3": return "1";
                case "4": return "1";
                case "5": return "2";
                case "6": return "1";
                case "7": return "2";
                default: return "ERROR";
            }
        }
        static void Main(string[] args)
        {
            #region Configuration
            bool do_make_output_and_input_mapping_equal = true;
            bool do_optimize_second_domain = true; // replace logic for second share domain by keeping track of masks
            bool do_mixcolumns = false; // specifics for mixcolumns design, like seting the input sharing to defined value
            bool do_add_roundkey = true; // specifics for addroundkey design, 
            #endregion

            #region Parsing Input
            // 1. Read verilog file
            StreamReader reader;
            if (!do_mixcolumns)
            {
                if (!do_add_roundkey)
                    reader = new System.IO.StreamReader("../../aes_sbox_boyar_peralta_without_changes.v");
                else
                    reader = new System.IO.StreamReader("../../addroundkey.v");
            }
            else
                reader = new System.IO.StreamReader("../../mixcolumns.v");

            String current_line = "";

            // 1.a Read input_ports
            String[] input_ports;
            while (!reader.EndOfStream && !(current_line = reader.ReadLine()).Contains("input")) ;
            input_ports = current_line.Replace("input", "").Replace(" ", "").Replace("\t", "").TrimEnd(',').Split(',');

            // 1.b Read output_ports
            String[] output_ports;
            while (!reader.EndOfStream && !(current_line = reader.ReadLine()).Contains("output")) ;
            output_ports = current_line.Replace("output", "").Replace(" ", "").Replace("\t", "").TrimEnd(',').Split(',');

            // 1.c Read assignments
            List<String> assignments = new List<string>();
            while (!reader.EndOfStream)
            {
                current_line = reader.ReadLine(); // read one line
                if (current_line.Contains("assign")) //Check if line contains "assign"
                    assignments.Add(current_line.Replace("assign", "").Replace(" ", "").Replace("\t", "").Split(';')[0]);
            }

            // 1.d Parse assignments into DEST, PORTA, PORTB, FUNCTION
            List<Tuple<String, String, String, String>> assignments_parsed = new List<Tuple<string, string, string, string>>();

            foreach (var assignment in assignments)
            {
                String[] dest_and_rest = assignment.Split('=');
                String dest = dest_and_rest[0]; // DEST
                String rest = dest_and_rest[1];

                rest = rest.Replace(";", "").Replace("(", "").Replace(")", ""); // Replace unnecessary characters

                // Extract function and opeands
                String function = "=";
                String[] ops;
                if (rest.Contains("~")) // XNOR?
                {
                    rest = rest.Replace("~", "");
                    function = "~";
                    ops = rest.Split('^');
                }
                else if (rest.Contains("^"))
                {
                    function = "^";
                    ops = rest.Split('^');
                }
                else if (rest.Contains("&"))
                {
                    function = "&";
                    ops = rest.Split('&');
                }
                else
                {
                    ops = new String[] { rest, "" };
                }

                // Add to list of parsed assigments
                assignments_parsed.Add(new Tuple<string, string, string, string>(dest, ops[0], ops[1], function));
            }
            #endregion

            #region Create SMT formulars
            // 2. Write SMT formulars
            StreamWriter writer = new StreamWriter("../../output.smt", false);

            // 2.a Write inputs
            writer.WriteLine("; Inputs");
            foreach (var input in input_ports)
                writer.WriteLine("(declare-const " + input + " Int)");

            // 2.b Write input constraints 1 = m0, 2 = m1, 3 = m0 + m1
            if (!do_mixcolumns && !do_add_roundkey)
            {
                writer.WriteLine("\r\n; Input constraints");
                foreach (var input in input_ports)
                {
                    writer.WriteLine("(assert(> " + input + " 0))");
                    writer.WriteLine("(assert(< " + input + " 4))");
                }
            }
            else // MixColumns Constraints taken from constraints defined by Sbox
            {
                foreach (var input in input_ports)
                {
                    if(do_mixcolumns)
                        writer.WriteLine("(assert(= " + input +  " " + getInputConstraintsForMixColumns(input.Split('x')[1]) + "))");
                    else
                        writer.WriteLine("(assert(= " + input + " " + getInputConstraintsForMixColumns(input[1].ToString()) + "))");
                }
                
            }

            // Declare helpers --> MASKS to use for resharing
            writer.WriteLine("(declare-const MASK1 Int)");
            writer.WriteLine("(assert(= MASK1 1))");
            writer.WriteLine("(declare-const MASK2 Int)");
            writer.WriteLine("(assert(= MASK2 2))");

            // 2.c Declare gates
            writer.WriteLine("\r\n; Gates");
            foreach (var assigment in assignments_parsed)
            {
                // Unpack
                string dest = assigment.Item1;
                string op_a = assigment.Item2;
                string op_b = assigment.Item3;
                string func = assigment.Item4;

                // Declare gate outputs and its constraitns
                writer.WriteLine("(declare-const " + dest + " Int)");
                writer.WriteLine("(assert(> " + dest + " 0))");
                writer.WriteLine("(assert(< " + dest + " 4))");

                // Apply rules
                switch (func)
                {
                    case "^": // XOR
                        {
                            // always take the mask that is not one the first and not on the second input
                            writer.WriteLine("(assert (not (or (= " + dest + " " + op_a + ") (= " + dest + " " + op_b + "))))");
                            break;
                        }
                    case "&": // AND
                        {
                            // either mask with the first or the second mask
                            writer.WriteLine("(assert (or (= " + dest + " " + op_a + ") (= " + dest + " " + op_b + ")))");
                            break;
                        }
                    case "~": // XNOR
                        {
                            // always take the mask that is not one the first and not on the second input
                            writer.WriteLine("(assert (not (or (= " + dest + " " + op_a + ") (= " + dest + " " + op_b + "))))");
                            break;
                        }
                    case "=": // ASSIGN
                        {
                            // just feed the input forward
                            writer.WriteLine("(assert(= " + dest + " " + op_a + "))");
                            break;
                        }
                    default:
                        {
                            writer.WriteLine("!!!!! ERROR !!!!" + assigment.ToString());
                            break;
                        }
                }

                writer.WriteLine("\r\n");
            }

            // 2.d Declare safety constraints
            writer.WriteLine("\r\n; Safety constraints");
            foreach (var assigment in assignments_parsed)
            {
                // Unpack
                string dest = assigment.Item1;
                string op_a = assigment.Item2;
                string op_b = assigment.Item3;
                string func = assigment.Item4;

                if (func == "=") continue; // Skip direct assignments
                writer.WriteLine("(assert (not (= " + op_a + " " + op_b + ")))");
            }

            // 2.[?] Define that outputs and inputs must have the same sharing!
            if (do_make_output_and_input_mapping_equal)
            {
                if (!do_mixcolumns)
                {
                    writer.WriteLine("; Outputs must have the same sharing as inputs");
                    for (int i = 0; i < 8; i++)
                        writer.WriteLine("(assert (= o" + i + " i" + i + "))");
                }
                else // MixColumns
                {
                    writer.WriteLine("; Outputs must have the same sharing as inputs");
                    foreach (var input in input_ports)
                    {
                        writer.WriteLine("(assert (= " + input.Replace("a", "b") + " " + input + "))");
                    }
                }
            }

            // 2.e Finalize
            writer.WriteLine("\r\n; Check for satisfiablility");
            writer.WriteLine("(check-sat)");
            writer.WriteLine("(get-model)");
            writer.WriteLine("(exit)");
            writer.Close();
            #endregion

            #region Use Z3 to find secure mask mapping
            // 3. Run Z3 and get output
            String z3_output = "";
            Process z3 = new Process();
            z3.StartInfo.FileName = "C:\\Z3\\z3-4.5.0-x64-win\\bin\\z3.exe";
            z3.StartInfo.Arguments = "-smt2 ../../output.smt";
            z3.StartInfo.UseShellExecute = false;
            z3.StartInfo.RedirectStandardOutput = true;
            z3.Start();

            z3_output = z3.StandardOutput.ReadToEnd(); // Get output of Z3

            z3.WaitForExit();
            #endregion

            #region Parse Z3 output and write Verilog file
            // Interpret Z3 output
            Dictionary<string, string> mask_mapping = new Dictionary<string, string>();
            z3_output = z3_output.Replace("Int\r\n", "").Replace("(define-fun", "").Replace(")", "").Replace(" ", "").Replace("(", "=").Replace("sat\r\n=model\r\n", "");
            Console.Write(z3_output);
            foreach (var line in z3_output.Split())
            {
                if (line != "")
                {
                    mask_mapping.Add(line.Split('=')[0], line.Split('=')[1]);
                }
            }

            //DEBUG : Mixcolumns write ports with wrong input/output mask association
            /*foreach (var input in input_ports)
            {
                if(mask_mapping[input] != mask_mapping[input.Replace("a", "b")])
                    Console.WriteLine(input + " = " + mask_mapping[input] + " --> " + input.Replace("a", "b") + " = " + mask_mapping[input.Replace("a", "b")]);
            }*/
            


   // 4. Write Verilog file
   StreamWriter output_verilog = new StreamWriter("../../output.v", false);

            // Start writing Verilog file
            if (!do_mixcolumns && !do_add_roundkey)
                output_verilog.WriteLine("module aes_sbox(");
            else
            {
                if(!do_add_roundkey)
                    output_verilog.WriteLine("module mixcolumns(");
                else
                    output_verilog.WriteLine("module addroundkey(");
            }

            // 4.a write input shares
            output_verilog.Write("   input ");
            foreach (var inport in input_ports)
            {
                output_verilog.Write(inport + "_0, "); // Write two shares
                output_verilog.Write(inport + "_1, ");
            }

            // Write masks
            output_verilog.Write("MASK1_0, MASK1_1, MASK2_0, MASK2_1, "); // Write two shares
            output_verilog.Write("\r\n");

            // 4.b write output shares
            output_verilog.Write("   output ");
            foreach (var outport in output_ports)
            {
                output_verilog.Write(outport + "_0, "); // Write two shares
                output_verilog.Write(outport + "_1, ");
            }
            output_verilog.WriteLine("\r\n   input clk, rst) ;");

            // 4.c Write comment on which inputs use which mask combination
            output_verilog.Write("\r\n/* ");
            foreach (var inport in input_ports)
            {
                output_verilog.Write(inport + " -> " + mask_mapping[inport] + ", ");
            }
            output_verilog.WriteLine("*/");

            // 4.d Write masked assignments
            foreach (var assignment in assignments_parsed)
            {
                // Unpack
                string dest = assignment.Item1;
                string op_a = assignment.Item2;
                string op_b = assignment.Item3;
                string func = assignment.Item4;

                switch (func)
                {
                    case "^": // XOR
                        {
                            output_verilog.WriteLine("assign " + dest + "_0" + " = " + op_a + "_0" + " ^ " + op_b + "_0" + "; "); // First share
                            if (!do_optimize_second_domain) // Use second share domain optimization (save gates) or not?
                                output_verilog.WriteLine("assign " + dest + "_1" + " = " + op_a + "_1" + " ^ " + op_b + "_1" + "; "); // Second share
                            else
                                output_verilog.WriteLine("assign " + dest + "_1 = " + getMaskNameFromNumber(mask_mapping[dest]) + ";"); 
                            break;
                        }
                    case "&": // AND
                        {
                            // assign DEST_0 = (OPA_0 . OPB_0) OR  (~OPA_0 . OPB_1);
                            //
                            // Which share appears on output
                            if (mask_mapping[dest] == mask_mapping[op_a])
                            {
                                //Bugfinding variant
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_a + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_a + "_1)" + "; "); // Second share

                                //Variante 4
                                output_verilog.WriteLine("assign {2}_0 = (({0}_0 & {1}_0) ^ (({0}_0 & {1}_1) ^ {1}_1)) ^ ((({0}_1 & {1}_0) ^ (({0}_1 & {1}_1) ^ {1}_1)) ^ {0}_1);", op_a, op_b, dest); // First share
                                output_verilog.WriteLine("assign {2}_1 = {0}_1;", op_a, op_b, dest); // Second share

                                //Variante 3
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_b + "_0" + " & " + op_a + "_0)" + " ^ (((" + op_b + "_0" + " & " + op_a + "_1) ^ " + op_a + "_1)" + "^ " + op_b + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_b + "_1" + " & " + op_a + "_0)" + " ^ (((" + op_b + "_1" + " & " + op_a + "_1) ^ " + op_a + "_1)" + "^ " + op_b + "_1)" + "; "); // Second share

                                //Variante 2
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_b + "_0" + " & " + op_a + "_0)" + " ^ ((" + op_b + "_0" + " & " + op_a + "_1) ^ " + op_a + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_b + "_1" + " & " + op_a + "_0)" + " ^ ((" + op_b + "_1" + " & " + op_a + "_1) ^ " + op_a + "_1)" + "; "); // Second share

                                //Variante 1
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_b + "_0" + " & " + op_a + "_0)" + " | (~" + op_b + "_0" + " & " + op_a + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_b + "_1" + " & " + op_a + "_0)" + " | (~" + op_b + "_1" + " & " + op_a + "_1)" + "; "); // Second share
                            }
                            else if (mask_mapping[dest] == mask_mapping[op_b])
                            {
                                //Bugfinding variant
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_b + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_b + "_1)" + "; "); // Second share

                                // Variante 4
                                output_verilog.WriteLine("assign {2}_0 = (({0}_0 & {1}_0) ^ (({0}_0 & {1}_1) ^ {1}_1)) ^ ((({0}_1 & {1}_0) ^ (({0}_1 & {1}_1) ^ {1}_1)) ^ {0}_1);", op_b, op_a, dest); // First share
                                output_verilog.WriteLine("assign {2}_1 = {0}_1;", op_b, op_a, dest); // Second share

                                //Variante 3
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_a + "_0" + " & " + op_b + "_0)" + " ^ (((" + op_a + "_0" + " & " + op_b + "_1) ^ " + op_b + "_1)" + "^ " + op_a + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_a + "_1" + " & " + op_b + "_0)" + " ^ (((" + op_a + "_1" + " & " + op_b + "_1) ^ " + op_b + "_1)" + "^ " + op_a + "_1)" + "; "); // Second share

                                //Variante 2
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_a + "_0" + " & " + op_b + "_0)" + " ^ ((" + op_a + "_0" + " & " + op_b + "_1) ^ " + op_b + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_a + "_1" + " & " + op_b + "_0)" + " ^ ((" + op_a + "_1" + " & " + op_b + "_1) ^ " + op_b + "_1)" + "; "); // Second share

                                //Variante 1
                                //output_verilog.WriteLine("assign " + dest + "_0" + " = (" + op_a + "_0" + " & " + op_b + "_0)" + " | (~" + op_a + "_0" + " & " + op_b + "_1)" + "; "); // First share
                                //output_verilog.WriteLine("assign " + dest + "_1" + " = (" + op_a + "_1" + " & " + op_b + "_0)" + " | (~" + op_a + "_1" + " & " + op_b + "_1)" + "; "); // Second share
                            }
                            else
                            {
                                output_verilog.WriteLine("!!!! ERROR !!!");
                            }
                            break;
                        }
                    case "~": // XNOR
                        {
                            output_verilog.WriteLine("assign " + dest + "_0" + " = ~(" + op_a + "_0" + " ^ " + op_b + "_0" + "); "); // First share
                            if (!do_optimize_second_domain) // Use second share domain optimization (save gates) or not?
                                output_verilog.WriteLine("assign " + dest + "_1" + " =  (" + op_a + "_1" + " ^ " + op_b + "_1" + "); "); // Second share
                            else
                                output_verilog.WriteLine("assign " + dest + "_1 = " + getMaskNameFromNumber(mask_mapping[dest]) + ";");
                            
                            break;
                        }
                    case "=": // ASSIGN
                        {
                            // just feed the input forward
                            output_verilog.WriteLine("assign " + dest + "_0" + " = " + op_a + "_0" + "; "); // First share
                            if (!do_optimize_second_domain) // Use second share domain optimization (save gates) or not?
                                output_verilog.WriteLine("assign " + dest + "_1" + " = " + op_a + "_1" + "; "); // Second share
                            else
                                output_verilog.WriteLine("assign " + dest + "_1" + " = " + getMaskNameFromNumber(mask_mapping[dest]) + ";");
                            break;
                        }
                    default:
                        {
                            output_verilog.WriteLine("!!!!! ERROR !!!!" + assignment.ToString());
                            break;
                        }
                }
            }
            // Write end of module
            if (!do_mixcolumns && !do_add_roundkey)
                output_verilog.WriteLine("\r\n endmodule // aes_sbox");
            else
            {
                if(!do_add_roundkey)
                    output_verilog.WriteLine("\r\n endmodule // mixcolumns");
                else
                    output_verilog.WriteLine("\r\n endmodule // addroundkey");
            }

            // 4.e write wrapper for maskVerif tool
            // Start writing Verilog file
            output_verilog.WriteLine("\r\nmodule top(input m0_0, m0_1, m1_0, m1_1,"); // m0_0 = m0_1, m1_0 = m1_1 
            output_verilog.Write("   output ");
            foreach (var outport in output_ports)
            {
                output_verilog.Write(outport + "_0, "); // Write two shares
                output_verilog.Write(outport + "_1, ");
            }
            output_verilog.WriteLine("\r\n   input clk, rst) ;");

            if (!do_mixcolumns && !do_add_roundkey)
                output_verilog.WriteLine("aes_sbox aes_sbox_1("); // Instantiate module
            else
            {
                if (!do_add_roundkey)
                    output_verilog.WriteLine("mixcolumns mixcolumns_1("); // Instantiate module
                else
                    output_verilog.WriteLine("addroundkey addroundkey_1("); // Instantiate module
            }

            foreach (var inport in input_ports) // Connect inputs
            {
                if(mask_mapping[inport] == "1") // m0
                {
                    output_verilog.WriteLine("." + inport + "_0(m0_0),");
                    output_verilog.WriteLine("." + inport + "_1(m0_1),");
                }
                else if (mask_mapping[inport] == "2") // m1
                {
                    output_verilog.WriteLine("." + inport + "_0(m1_0),");
                    output_verilog.WriteLine("." + inport + "_1(m1_1),");
                }
                else // m2 = m0 + m1
                {
                    output_verilog.WriteLine("." + inport + "_0(m0_0 ^ m1_0),");
                    output_verilog.WriteLine("." + inport + "_1(m0_1 ^ m1_1),");
                }
            }

            // Connect mask inputs
            output_verilog.WriteLine(".MASK1_0(m0_0),");
            output_verilog.WriteLine(".MASK1_1(m0_1),");
            output_verilog.WriteLine(".MASK2_0(m1_0),");
            output_verilog.WriteLine(".MASK2_1(m1_1),");

            // Write outputs
            foreach (var outport in output_ports)
            {
                output_verilog.WriteLine("." + outport + "_0(" + outport + "_0),");
                output_verilog.WriteLine("." + outport + "_1(" + outport + "_1),");
            }
                output_verilog.WriteLine(".clk(clk),\r\n.rst(rst));");
            output_verilog.WriteLine("\r\n endmodule // top");

           
            output_verilog.Close();
            #endregion
            Console.ReadKey(); //Wait
        }
    }
}
