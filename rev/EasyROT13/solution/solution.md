Complete solution:

Running the program in a windows VM, the user must enter the correct flag as a parameter. This input is tested and (most likely) rejected for being wrong. 

Loading the program up in ghidra will only create more confusion. Searching for strings shows nothing useful, there is a strange selection of imports and functions in the symbol tree that are completely unhelpful. The user may check for entropy in each section of the binary and find that the .huan section is encrypted. 

At this stage, the user may wish to search online and will find this is evidence the PE was cyphered with a program called Huan. There is a seperate security research project that will decrypt these programs, called huan_unpack. It the user wants a codeless solution to this problem, they should use this script to extract the encryption keys stored at the start of .huan and unpack the binary. 


They should put the new binary back in ghidra and see that its a fairly straight forward ROT13 challenge from here. It was compiled with MSVC so contains several redundant sections of code, but a string search will lead them to FUN_140001070, then reading the decompilation will reveal TbbfrPGS{vqn_jnf_birexvyy}. This is ROT13 for GooseCTF{ida_was_overkill}
