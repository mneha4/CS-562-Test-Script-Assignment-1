# Assignment testing script CS562
# Author - Neha M
# Date - 20/11/2017


import time
import os, zipfile, tarfile
import subprocess
import psutil
import signal


def extract():
	dir_name = '/home/neha/AI_Asgn/Archive/Assign_1_Submissions'
	os.mkdir('Assignments')
	for item in os.listdir(dir_name): # loop through items in dir
		file_name = os.path.abspath(item)
		print (file_name)
		name = item.split('.')[0]
		create_dir_name = dir_name + '/Assignments/' + name
		if item.endswith(".zip"): 
			os.mkdir(create_dir_name)
			zip_ref = zipfile.ZipFile(file_name) 
			zip_ref.extractall(path=create_dir_name) 
			zip_ref.close()
			
		elif item.endswith("tar.gz"):
			os.mkdir(create_dir_name)
			tar = tarfile.open(item, mode = 'r:gz')
			tar.extractall(path=create_dir_name)
			tar.close()

	print ("Extraction Completed\n")			   


def run(input_file,out_file):
	dir_name = '/home/neha/AI_Asgn/Archive/Assign_1_Submissions/Assignments/'

	for item in os.listdir(dir_name): 
		print ("Currently running "+ item)
		abspath = dir_name+item
		list_item = os.listdir(abspath)
		
		if len(list_item) == 1:
			abspath = abspath+"/"+list_item[0]
		
		p = subprocess.Popen(["make"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=abspath)
		exit, err = p.communicate()
		print (err)
		if err=="":
			try:
				command = "./tsp <{} >{}".format(input_file,out_file)
				p = subprocess.Popen([command],shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=abspath, preexec_fn=os.setsid)
				process = psutil.Process(p.pid)
				time.sleep(120)
				os.killpg(os.getpgid(p.pid), signal.SIGTERM)
				print ("Process Stopped\n")

			except OSError:
				print ("Run Error for - " + abspath + "\n")
		else:
			print ("Make command failed to run\n")

		
			


def adjacency_matrix(input_file):
	a = int((input_file.split('_'))[1]) + 2
	with open(input_file) as f:
		data = []
		for i, line in enumerate(f):
			if (i == a or i>a):
				number_strings = line.split() # Split the line on runs of whitespace
				numbers = [float(n) for n in number_strings] # Convert to integers
				data.append(numbers)	
		return (data)

def get_path(path_to_file):
	try:
		fileHandle = open (path_to_file,"r")
		lineList = fileHandle.readlines()
		fileHandle.close()
		if len(lineList)!=0:
			return (lineList[-1]).split()
		return list(lineList)
	except IOError:
		print (path_to_file)
		print("Error while opening file\n")		

def get_cost(path , cost_matrix, input_file):
	path_length = int(input_file.split('_')[1])
	cost = 0

	if (path)!=None:
		if len(path) == path_length:
			for i in range (0, len(path)-1):
				cost = cost + cost_matrix[int(path[i])-1][int(path[i+1])-1]
			return cost	
		else:
			print (path)
			print len(path)
			print("Path length is is not equal to " + str(path_length))
			return float("inf")
	else:
		return float("inf")		
			 


def calculate_cost(input_file , file_index):
	resultfile = "Results " + str(file_index)
	out_file = open(resultfile,'w')

	dir_name = '/home/neha/AI_Asgn/Archive/Assign_1_Submissions/Assignments/'
	cost_matrix = adjacency_matrix(input_file)

	for item in os.listdir(dir_name): 
		print ("Currently calculating "+ item)
		abspath = dir_name+item
		list_item = os.listdir(abspath)
		
		if len(list_item) == 1:
			abspath = abspath+"/"+list_item[0]

		abspath = abspath + "/" + str(file_index)
		path = get_path(abspath)
		cost = get_cost(path , cost_matrix, input_file)

		out_file.writelines("Group " + item + ", File Index " + str(file_index) + ", Cost - " + str(cost))
		out_file.write("\n")

	out_file.close()
	


if __name__ == '__main__':
	# extract()
	run('"euc_100"','1')
	run('"euc_250"','2')
	run('"euc_500"','3')
	run('"noneuc_100"','4')
	run('"noneuc_250"','5')
	run('"noneuc_500"','6')

	input_files=['euc_100','euc_250','euc_500','noneuc_100','noneuc_250','noneuc_500']
	
	j = 1
	for i in input_files:
		calculate_cost(i,j)
		j = j + 1

