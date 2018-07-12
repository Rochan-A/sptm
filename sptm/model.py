# -*- coding: utf-8 -*-

"""
	Model functions
"""

#######################################

import gensim.corpora as corpora
import gensim.models.wrappers as Wrappers
import gensim.utils as utils
from gensim.models import CoherenceModel
import preprocess
from utils import force_unicode

# Enable logging for gensim - optional
import logging, codecs, multiprocessing

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

class Model:

	def __init__(self, mallet_path, tokens=None, input_path=None):
		"""
		This class is responsible for traning the Topic Model using Mallet's
		LDA which can be found [here](http://mallet.cs.umass.edu/topics.php)

		Arguments
		---------
		mallet_path: Location of Mallet binary  
		input_path: Location of saved preprocessed tokens file  
		tokens: tokens of preprocessed data

		NOTE: If both input_path and tokens is given, tokens will always take
		higher preference
		"""
		self.mallet_path = mallet_path
		self.tokens = []

		if (tokens is not None and input_path is None) or (tokens is not None and input_path is not None):
			self.tokens = tokens
		elif tokens is None and input_path is not None:

			# Read the saved tokens file
			with codecs.open(input_path, 'r', encoding='utf8') as F:
				for row in F:
					token_in_row = row.split(",")
					for i in enumerate(token_in_row):
						token_in_row[i] = force_unicode(token_in_row[i])
					self.tokens.append(token_in_row)
		elif tokens is None and input_path is None:
			print("Assuming user to load model from saved file, use Model.load()")
		else:
			print("Missing tokens")

	def fit(self):
		"""
		Generate the id2word dictionary and term document frequency of
		the given tokens

		NOTE: Should be called only after making sure that the tokens
		have been properly read
		"""
		if self.tokens is not []:
			# Create Dictionary
			self.id2word = corpora.Dictionary(self.tokens)
			# Term Document Frequency
			self.corpus = [self.id2word.doc2bow(text) for text in self.tokens]
		else:
			print("Tokens not initialized")

	def model_params(self, alpha=50, workers=multiprocessing.cpu_count(), \
	prefix=None, optimize_interval=0, iterations=1000, topic_threshold=0.0, num_topics=100):
		"""
		Specify all model parameters

		NOTE: These are the same parameters used while traning models
		for coherence computation. Call this function to re-initialize
		parameter values

		Arguments
		---------
		alpha: Alpha value (Dirichlet Hyperparameter)  
		workers: Number of threads to spawn to parallel traning process  
		prefix: prefix  
		optimize_interval: Number of intervals after which to recompute hyperparameters  
		iterations: Number of iterations  
		topic_threshold: Topic threshold  
		num_topics: Number of topics
		"""
		self.alpha = alpha
		self.workers = workers
		self.prefix = prefix
		self.optimize_interval = optimize_interval
		self.iterations = iterations
		self.topic_threshold = topic_threshold
		self.num_topics = num_topics

	def train(self):
		"""
		Train LDA Mallet model using gensim's Mallet wrapper
		"""
		self.lda_model_mallet = Wrappers.LdaMallet(self.mallet_path, \
			corpus=self.corpus, num_topics=self.num_topics, \
			alpha=self.alpha, id2word=self.id2word, \
			workers=self.workers, prefix=self.prefix, \
			optimize_interval=self.optimize_interval, \
			iterations=self.iterations, \
			topic_threshold=self.topic_threshold)

	def return_model(self):
		"""
		Returns
		-------
		gensim wrapper for Mallet LDA Model
		"""
		return self.lda_model_mallet

	def print_topics(self, num_topics=100, num_words=10):
		"""
		Print the top <num_words> for <num_topics> topics.

		Arguments
		---------
		num_topics: Number of topics to print  
		num_words: Number of top words to print for each topic

		Returns
		-------
		List of topics and top words
		"""
		return self.lda_model_mallet.print_topics(num_topics, num_words)

	def save(self, output_path):
		"""
		Save the Mallet lDA model. Also, save the document_topic							TODO
		distribution

		Arguments
		---------
		output_path: Location to save the LDA model
		"""
		self.lda_model_mallet.save(output_path + "LDA-Mallet")

	def get_coherence(self):
		"""
		Compute Coherence Score of the model

		Returns
		-------
		Coherence value
		"""
		coherence_model_lda = CoherenceModel(model=self.lda_model_mallet, \
				texts=self.tokens, dictionary=self.id2word, \
				coherence='c_v')
		coherence_lda = coherence_model_lda.get_coherence()
		return coherence_lda

	def optimum_topic(self, start=10, limit=100, step=11):
		"""
		Compute c_v coherence for various number of topics

		Arguments
		---------
		dictionary: Gensim dictionary  
		corpus: Gensim corpus  
		texts: List of input texts  
		limit: Max num of topics

		Return
		---------
		Dictionary of {num_topics, c_v}
		"""
		coherence_values = []
		model_list = []
		for num_topics in range(start, limit, step):
			model = Wrappers.LdaMallet(self.mallet_path, \
				corpus=self.corpus, num_topics=num_topics, \
				alpha=self.alpha, id2word=self.id2word, \
				workers=self.workers, prefix=self.prefix, \
				optimize_interval=self.optimize_interval, \
				iterations=self.iterations, \
				topic_threshold=self.topic_threshold)
			model_list.append(model)
			coherencemodel = CoherenceModel(model=model, \
				texts=self.tokens, dictionary=self.id2word, \
				coherence='c_v')
			coherence_values.append(coherencemodel.get_coherence())
		x = range(start, limit, step)
		out = dict()
		for m, cv in zip(x, coherence_values):
			out["num_topics"] = m
			out["c_v"] = round(cv, 4)
		return out

	def load(self, saved_model):
		"""
		Load a Mallet LDA model previously saved

		Arguments
		---------
		saved_model: Location to saved model
		"""
		self.lda_model_mallet = utils.SaveLoad.load(saved_model)
