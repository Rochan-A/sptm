# -*- coding: utf-8 -*-

"""
	Conditional probability functions
"""

#######################################

import csv, ast, operator
import numpy as np

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

class ConditionalMatrix:

	def __init__(self, doctopics_path, tokens_path):
		"""
		Compute the conditional probability matrix of each sentence
		versus another. Open the document topic file, Get the review
		number for every sentence used

		Arguments
		---------
		doctopics_path: Location of the document topic file
		tokens_path: Path to token file
		"""
		self.doc_matrix = []
		with open(doctopics_path, 'r') as F:
			reader = csv.reader(F, delimiter='\t')
			for row in reader:
				# Delete the first two columns in the file
				self.doc_matrix.append(row[2:])

		self.tokens_matrix = []
		with open(tokens_path, 'rU') as F:
			reader = csv.reader((line.replace('\0', '') for line in F), delimiter=',')
			for row in reader:
				try:
					if len(row) > 0:
						self.tokens_matrix.append(int(row[0]))
				except:
					print('Some error while reading the row')

		self.num_sent = len(self.doc_matrix)
		self.num_topics = len(self.doc_matrix[0])

	def construct_matrix(self):
		"""
		Construct a simple frequency matrix of each topic (current sentence)
		vs topic (next sentence)
		Identify the topics with high probabilities for each sentence
		Compute the conditional probabilities
		"""

		# Create a dictionary of all the topic frequencies
		self.topic_freq = dict()
		for i in range(0, self.num_topics):
			self.topic_freq[i] = 0

		# Construct an empty matrix
		self.freq_matrix = np.zeros((self.num_topics, self.num_topics), dtype=float)

		# Iterate over all the sentences - 1
		for i in range(self.num_sent - 1):

			try:
				if self.tokens_matrix[i] == self.tokens_matrix[i + 1]:

					# Create a dictionary of all the probabilities for the two sentences
					topic_dict = [dict(), dict()]
					for j in range(0, self.num_topics):
						topic_dict[0][j] = ast.literal_eval(self.doc_matrix[i][j])
						topic_dict[1][j] = ast.literal_eval(self.doc_matrix[i + 1][j])

					for x in range(self.num_topics):
						for y in range(self.num_topics):
							self.freq_matrix[x][y] += \
								float(topic_dict[1][y])*float(topic_dict[0][x])
							self.topic_freq[x] += float(topic_dict[0][x])
			except:
				print("Sentence Missing")

		# Conditional probability
		for i in range(self.num_topics):
			for j in range(self.num_topics):
				if float(self.topic_freq[i]) != 0:
					self.freq_matrix[i][j] = (float(self.freq_matrix[i][j])/float(self.topic_freq[i]))*65

	def sort_and_label(self, labels_path):
		"""
		Sort and label each value in the matrix

		Arguments
		---------
		labels_path: Path to a labels file
		"""

		self.labels = []
		with open(labels_path, 'r') as F:
			reader = csv.reader(F, delimiter=',')
			for row in reader:
				self.labels.append(row)

		self.labeled = []
		for i in range(self.num_topics):
			self.labeled.append({})
			self.labeled[i]['label'] = self.labels[i][0]
			for j in range(self.num_topics):
				self.labeled[i][self.labels[j][0]] = self.freq_matrix[i][j]

		self.sorted = []
		for i in range(self.num_topics):
			sort_row = sorted(self.labeled[i].items(), key=operator.itemgetter(1))
			self.sorted.append(sort_row)

	def save(self, output_path, matrix):
		"""
		Save the matrix

		Arguments
		---------
		output_path: Location with filename to save matrix
		matrix: Matrix to save
		"""
		with open(output_path, 'w') as F:
			writer = csv.writer(F, delimiter=',')
			for r in matrix:
				writer.writerow(r)
