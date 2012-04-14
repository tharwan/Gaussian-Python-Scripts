import re
import subprocess
import sys


def isNaN(x):
	return str(x) == str(1e400*0)



basename=sys.argv[1]
i = 0
erg = open(basename+"_erg.txt","w+")
while True:
	proc = "formchk %s_%i.chk %s_%i.fchk"%(basename,i,basename,i)
	try:
		open("%s_%i.chk"%(basename,i))
	except IOError:
		break
	print proc
	if (subprocess.call(proc,shell=True) != 0):
		break
	
	#parse fchk files
	f = open(basename+"_%i.fchk"%i)
	electrons = 0
	orbs = []
	parse = True
	n=0
	ex_reg = re.compile("Number of electrons\s+I\s+(\d+)")
	for line in f:
		if "Alpha Orbital Energies" in line:
			parse=True
			n=0
		if parse:
			n+=1
		if parse and n>=2:
			try:
				orbs.extend([float(s) for s in line.split()])
			except:
				parse=False
		match = ex_reg.search(line)
		if match:
			electrons = int(match.group(1))


	#parse log files:
	f = open(basename+"_%i.log"%i)
	ex_reg = re.compile("Excited State\W+1:.*[^-]([+-]?\d+\.\d+)\W+eV")
	#matches the energy of the first exitation state
	Ex = float('nan');
	for line in f:
		match = ex_reg.search(line)
		if match:
			Ex = float(match.group(1))
	if isNaN(Ex):
		print "Error, exitation state energy not found"

	erg.write("%i %.10e %.10e\n"%(i,orbs[electrons/2-1]-orbs[electrons/2],Ex)) 
	#the homo/lumo orbitals are assumed to be at halfe the number of electrons
	i+=1
erg.close()
	
