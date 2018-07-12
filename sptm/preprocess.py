# -*- coding: utf-8 -*-

"""
	This script is to be used to preprocess the data
"""

#######################################

import spacy, re, logging, gensim, io, sys
from utils import force_unicode

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
nlp = spacy.load('en_core_web_sm')
reload(sys)
sys.setdefaultencoding('utf8')

class Corpus:

	def __init__(self, path):
		self.path = path
		self.raw_review = []
		self.sentences = []
		self.tokens = []

	def read_reviews(self, delimiter='\t', reg=r"(\\u[0-z][0-z][0-z])\w", rep=" "):
		"""
		Function to read reviews and store it in a list

		Arguments
		---------
		delimiter: The seperator between data  
		reg: Custom regex to filter  
		rep: String to replace the regex values

		Return
		---------
		None
		"""

		# Open the file
		with io.open(self.path, 'rb') as raw:
			self.raw_review = [x.strip().split(delimiter) for x in raw]

		# Select full review only
		for i, val in enumerate(self.raw_review):
			self.raw_review[i] = self.raw_review[i][-1]
			self.raw_review[i] = re.sub(reg, rep, self.raw_review[i])

	def splitsentence(self, min_len=2):
		"""
		Splits each review into its individual sentences.

		Arguments
		---------
		min_len: Minimum length of a sentenceo above which to concider it

		Return
		---------
		None
		"""

		# Iterate over every unique review
		for i, val in enumerate(self.raw_review):
			# Split the sentences
			sentences = self.raw_review[i].split('.')

			# Append the other sentences to the end of the review_buf
			for j, val in enumerate(sentences):
				# Make sure the sentence has more than two words
				if len(sentences[j]) > min_len:
					self.sentences.append(sentences[j])

	def tokenize_simple(self, deacc=False, min_len=2, max_len=15):
		"""
		Processes sentences before passing on to train models

		Arguments
		---------
		deacc: Remove accentuation  
		min_len: Minimal length of token in result  
		max_len: Maximum length of token in result

		Returns
		---------
		tokens: tokenized, de-accent and lowercased word list
		"""

		# Simple tokens, de-accent and lowercase processor
		tokens = []
		for i, val in enumerate(self.sentences):
			tokens.append(gensim.utils.simple_preprocess(self.sentences[i], deacc, min_len, max_len))
		return tokens

	def tokenize_custom(self, min_len=1):
		"""
		Processes sentences before passing on to train models

		Arguments
		---------
		min_len: Minimum length of tokens

		Returns
		---------
		None
		"""

		# POS Tagging and filtering sentences
		for i, val in enumerate(self.sentences):
			doc = nlp(force_unicode(self.sentences[i]))
			to = [unicode(i)]
			for tok in doc:
				if tok.is_stop != True and tok.pos_ != 'SYM' and \
					tok.tag_ != 'PRP' and tok.tag_ != 'PRP$' and \
					tok.pos_ != 'NUM' and tok.dep_ != 'aux' and \
					tok.dep_ != 'prep' and tok.dep_ != 'det' and \
					tok.dep_ != 'cc' and len(tok) != min_len:
					to.append(tok.lemma_)
			if len(to) > 1:
				self.tokens.append(to)

	def write_processed(self, name):
		"""
		Function to save reviews in a file buffer.

		Arguments
		---------
		name: Name of the file to save as

		Return
		---------
		None
		"""

		# Write the preprocessed reviews to a SINGLE file
		with io.open(name, "a", encoding='utf8') as outfile:
			for i, val in enumerate(self.tokens):
				outfile.write(unicode(','.join(self.tokens[i]) + "\n"))
