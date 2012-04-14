Some Python Scripts for automating some tasks in gaussian, extracting and analyzing the results.

*All scripts assumes a lot of things given by my working environment at tu ilmenau and are done so they do there job, not to be the very best solution*

# move.py #

When given an input file with two molecules it "moves" one of the molecules in given steps an calculates the given gaussian calculations for every step. 

The "moveing" is done by creating a seperate gaussian input file for every step and then submitting it to gaussian. The submitting is done via commandline statement using lsf (bsub) for loadbalancing. 

There is no deeper understanding in the script of what a molecule is, the two molecules are simply given by the number of atoms belonging to the first/second molecule assuming that the first n atoms belong to the first molecule and the next (n+1 … N) to the second.

To work properly the script is needs a "basename" for it‘s output files. It assumes that the basename is altough the name of the original input file. 

To alter the way the molecules are moved you must edit the variables in the script.

##Example:##
```
Input file: 
MG2MG.com

Script Command: 
python move.py MG2MG

Output Files:

MG2MG_0.com
MG2MG_1.com
MG2MG_2.com
...
```

The script is build to work with Python 2.4.

# parse_fchk.py #

To extract certain values, lets say the electron orbitals energies, you need information stored in the .chk files of a calculation. To do this you first have to make sure your calculation is setup to save the checkpoint files. To get the values out of the checkpoint file, which is in a binary format, you then have to convert the files via the formchk tool included in gaussian to get a formated checkpoint file (ASCI). 

This is done by the script saving every .chk file as a formated .fchk file. Then the alpha orbital energies are extraced, as well as the number of atoms to determin the energy gap between the HOMO/LUMO orbitals. Furthermore the first excited state energy from the .log files are read in. Both values are then stored in a text file, together with the number of the file from which they were read.

To work properly the script is needs a "basename" for it‘s input files.


##Example:##
```
Script Command: 
python parse_fchk.py MG2MG

Read Files: 
MG2MG_0.log
MG2MG_0.chk
MG2MG_1.log
MG2MG_1.chk
MG2MG_2.log
MG2MG_2.chk
...

Writen Files: 
MG2MG_0.fchk
MG2MG_1.fchk
MG2MG_2.fchk
...

MG2MG_erg.txt
``

