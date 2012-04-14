from os import system
import os
import sys
import re
import math
from copy import deepcopy

def numbers(s):
	# skip regex for now
	ret=[0,0,0]
	n=0
	for part in s.split(" "):
		try:
			ret[n]=float(part)
			n+=1
		except ValueError:
			continue
	return ret


def first_number(s):
	for char,n in zip(s,range(len(s))):
		if char.isdigit() or char=="-":
			return n


def add(input,pos,value,start,stop):
	# no numpy, sadly
	ret = deepcopy(input)  # copy
	for i in xrange(start,stop):
		ret[i][pos]+=value
	return ret

### VARIABLES ###

imax=15  # number of steps
xyz = 2  # direction of the movement 0 for x, 1 for y, 2 for z  
first_atom = 0 # first atom to move
last_atom = lambda: len(pos0)/2 #last atom to move
step_func = lambda: math.exp(i/10.0)-1 #called for every step

### VARIABLES ###


basename=sys.argv[1]
orig = open(basename+".com")
pos = []
read = False
for line in orig:
	if line=="\n" and read:
		break
	if read:
		pos.append(numbers(line))
	if line.startswith("0 1"):
		read = True
# the position of the atoms is saved in pos

pos0 = deepcopy(pos)  # start position
ex_reg = re.compile("%chk=(\S+.chk)") #reg ex for checkpoint file

for i in range(0,imax+1):
	name = basename+"_"+str(i)+".com"
	new = open(name,"w+")
	orig.seek(0)
	n=0
	write = False
	for line in orig:  # copy all lines from origina file
		if line=="\n" and write:
			write = False
		if write:
			new.write("%3s %13.8f %13.8f %13.8f\n"%(line[:first_number(line)].strip(),pos[n][0],pos[n][1],pos[n][2]))
			n+=1
		elif ex_reg.search(line):
			new.write("%%chk=%s\n"%(name[:-4]+".chk"))
		else:
			new.write(line)
		if line.startswith("0 1"):
			write = True
	if callable(first_atom):
		first_atom = first_atom()
	if callable(last_atom):
		last_atom = last_atom()	
	pos = add(pos0,xyz,step_func(),first_atom,last_atom)
	system("bsub -q Batch24 \"cd %s; g09 %s \""%(os.path.dirname(os.path.realpath(__file__)),name)) #job erstellen
