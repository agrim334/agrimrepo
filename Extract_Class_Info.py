import os
import subprocess
import re
import sys

COMMENTS = re.compile(r'''(//[^\n]*(?:\n|$))''',re.VERBOSE)				#regex for comment removal
def remove_comments(content):
	return COMMENTS.sub('\n', content)
											#command line arguments 1 and 2 for txt file(storage) and comment removal request
comment_flag = sys.argv[1]
path = "libraries/"
category_list = os.listdir(path)
comment_flag = int(comment_flag)
for category in category_list: 
	path = "libraries/"+category 								#path for libraries	
	lib_list = os.listdir(path)
	for lib in lib_list:
		p = path+"/"+lib
		jar_files = os.listdir(p)
		for jar in jar_files:
			jar_name = jar[:-4]
			op = p+"/"+jar_name
			p1 = "'"+p+"/"+jar_name
			p2 = p1 +".jar'"
			p1 = p1+"'"
			os.makedirs(op,exist_ok=True)				#creates subdirectories to extract jar files 
			c1 = "unzip -o -j "+p2+" '*.class' -d "+p1		
			subprocess.run(c1,shell=True,stdout=subprocess.DEVNULL)		#jar files extracted via unzip command output of unzip is redirected to null device as it is not needed
																			# os.makedirs and subprocess.run(c1) have to be executed once only for each dir
																			# if needed to run this program multiple times then comment these so as to avoid unnecessary creation of subdirectories
			try:
				class_files = os.listdir(op)
				for jar_class in class_files:
					jar_class=jar_class[:-6]
					if len(jar_name) == 0 :
						c2 = "echo " + jar 		#extracts all classes and methods alongwith bytecode,line table 
					else:
						file = op + ".txt"
						file = os.getcwd()+"/"+file 
						c2 = "javap -p -c -l -classpath '" + op +"/' "+ jar_class  		#extracts all classes and methods alongwith bytecode,line table 
						fp = open(file,mode = 'a')
						subprocess.run(c2,shell = True,stdout = fp)					#javap command runs and stores output to specified file
						if (comment_flag != 0):											#removing comments from disassembled code
							code_w_comments = open(file).read()
							code_wo_comments = remove_comments(code_w_comments)
							fh = open(file+"_nocomments", "w")
							fh.write(code_wo_comments)					#stored in seperate file
							fh.close()
							fp.close()
						else:
							fp.close()
			except:
				pass