# This script will read the results of sequenced samples of CCA. MUST BE ORGANIZED AND STAT ANALYZED
# see this url to retreive sequencing data: https://tcga-data.nci.nih.gov/tcga/tcgaCancerDetails.jsp?diseaseType=CHOL&diseaseName=Cholangiocarcinoma
# There are two different types... RNA and Micro-RNA
# This script just samples RNA...

#This script is personalized to the specific data my brother wanted. But ideally this will be a command line tool... so that means
# doing something like this: http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html

# this is a library used to read files in
import csv

# cabinet is an array. we will populate with objects of class Case..
# each index (like cabinet[0] or cabinet[1]) is an object you can explore
# with something like cabinet[9].barcode or cabinet[]
cabinet = []
numberOfCases = 36 + 9 #36 matched cases plus 9 healthy cases.

#these arrays are to store user input, it is a step towards making this code reproducable for any dataset of sequenced genomes.
samplesYouNeed = [];
barcodeFilenamesYouNeed = [];


#this is the overall structure of each case. There will be 45 total for the RNA
class Case:
	def __init__(self,sample,tissue_type):
		self.sample = sample;
		self.tissue_type = tissue_type;
		#self.files
	genes_results = "nothing added yet..."
	isoforms_results = "nothing added yet..."
	genes_norms = "..."
	isoforms_norms = "..."
	def isoforms_norms(self,isoforms_norms):
		self.isoforms_norms = isoforms_norms;
	def genes_norms(self,genes_norms):
		self.genes_norms = genes_norms;
	def genes_results(self,genes_results):
		self.genes_results = genes_results;
	def isoforms_results(self,isoforms_results):
		self.isoforms_results = isoforms_results;
# you can add attributes (or attr's) to your cases by defining (or def) functions to input
# check out the code i already wrote and mess figure out how it works...
# learned from: http://sthurlow.com/python/lesson08/


###### sample of initiating the cases...
#for num in range(0, numberOfCases):
#	x = Case("sample","tissue_type")
#	cabinet.append(x)
##### you can use "Case.attr(...)" to make attributes for your case...

samples = [];
samplesLinkedToFiles = {};
fileInCabinet = False;
placeHolder = -1;

# reading in the RNA file_manifest
i = 0;
with open('TCGA CHOL RNA-seq/file_manifest.txt', 'rb') as f:
	reader = csv.reader(f, delimiter="\t")
	print "reading in file_manifest, now iterating through line by line..."
	for line in reader:
		i = i+1
		for bb in cabinet:
			print "Current state of the cabinet: ", bb.sample
		if "TCGA" in line[5]: #removed the top three rows of manifest b/c unnecessary
			print "Sample", i,"from manifest:", line[5], "barcode_filename: ",line[6] #not necessary
			samples.append(line[5]) #not necassary but shines a light on sample names
			print "		searching cabinet..."
			for l in cabinet:
				print "		current case in Cabinet: ", l.sample
				if (line[5] == l.sample): #the sample is already in cabinet
					fileInCabinet = True;
					placeHolder = cabinet.index(l); #find position of the Case  #THERES SOMETHING WRONG HERE!!!
					print "		Found the case in cabinet"
					print "		placeHolder: ", placeHolder, "for case in cabinet"
			if (fileInCabinet == True): #this needs to be after the for loop
										#b/c we search the whole cabinet
				if "genes.normalized" in line[6]:
					cabinet[placeHolder].genes_norms(line[6])
					print "		Genes_norms added to case in cabinet"
				elif "genes.results" in line[6]:
					cabinet[placeHolder].genes_results(line[6])
					print "		genes_results added to case in cabinet"
				elif "isoforms.normalized" in line[6]:
					cabinet[placeHolder].isoforms_norms(line[6])
					print "		isoforms_norms added to case in cabinet"
				elif "isoforms.results" in line[6]:
					cabinet[placeHolder].isoforms_results(line[6])
					print "		genes_results added to case in cabinet"
				else:
					print "		the associated barcode_filename is not needed"
			else: #the sample is not already in Cabinet... (fileInCabinet == false)
				print "		the case wasn't found in cabinet"
				x = Case(line[5], 'none')
				if "genes.normalized" in line[6]:
					x.genes_norms(line[6])
					print "		genes_norms added to new case", x.sample
				elif "genes.results" in line[6]:
					x.genes_results(line[6])
					print "		genes_results added to new case", x.sample
				elif "isoforms.results" in line[6]:
					x.isoforms_results(line[6])
					print "		isoforms_results added to new case", x.sample
				elif "isoforms.normalized" in line[6]:
					x.isoforms_norms(line[6])
					print "		isoforms_norms added to new case", x.sample
				else:
					print "		the associated barcode_filename is not needed"
					#print new line
				cabinet.append(x)
				print "		case with sample", x.sample, "added to filing cabinet"
		else:
			print "current row",i,"does not contain a sample"
		#cabinet.append(x)

print "whole list of samples: ", len(samples), "verified by lines in RNA manifest: ", i/6
setSamples = list(set(samples))
for l in setSamples:
	print "sample name in array 'samples': ", l
print "simplified list of samples: ", len(setSamples)


# once i get all of the proper files into the proper gene Case, i can move to read in those files and extract
# the results Larry needs for his research
# instead of storing those values in python, i want to output them into files that he can read with R or Perl...
