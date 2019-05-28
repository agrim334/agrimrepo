import os
import subprocess

path = "lib/"
libraries = os.listdir(path)
for ele in libraries: 
	path = "lib/"+ele
	l2 = os.listdir(path)
	for e2 in l2:
		e3 = e2[:-4]
		op = "lib/"+ele+"/"+e3
		p1 = "'lib/"+ele+"/"+e3
		p2 = p1 +".jar'"
		p1 = p1+"'"
		
		#os.makedirs(op,exist_ok=True)
		
		c1 = "unzip -o -j "+p2+" *.class -d "+p1		
		#subprocess.run(c1,shell=True,stdout=subprocess.DEVNULL)	
		try:
			l3 = os.listdir(op)
			for e4 in l3:
				e4=e4[:-6]
				c3 = "javap -private -c -v -classpath '" + op +"/' "+ e4 # jvm instructions
				subprocess.run(c3,shell = True)
				
		except:
			pass