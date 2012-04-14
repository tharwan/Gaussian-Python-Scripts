from os import system
import os
import sys
import re
import math
from copy import deepcopy

def numbers(s):
	# keine lust auf regex
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
	# leider gibt es kein numpy
	ret = deepcopy(input)  # copy
	for i in xrange(start,stop):
		ret[i][pos]+=value
	return ret


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
# die positionen der atome werden in pos gespeichert

pos0 = deepcopy(pos)  # ausgangspositionen
imax=15  # Anzahl der Durchlaeufe
ex_reg = re.compile("%chk=(\S+.chk)")
for i in range(0,imax+1):
	name = basename+"_"+str(i)+".com"
	new = open(name,"w+")  # datei basename_i.com schreiben fuer i=0 keine verschiebung
	orig.seek(0)
	n=0
	write = False
	for line in orig:  # alle zeilen aus der originaldatei uebernehmen
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
	pos = add(pos0,2,math.exp(i/10.0)-1,0,len(pos0)/2)  # verschiebung der haelfte aller atome
			       # Koordiante: x->0 y->1 z->2
			         # Verschiebung in Angstroem
			           # Atom von Position x
			             # Bis Position y
	system("bsub -q Batch24 \"cd %s; g09 %s \""%(os.path.dirname(os.path.realpath(__file__)),name)) #job erstellen
