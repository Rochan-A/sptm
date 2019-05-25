# -*- coding: utf-8 -*-

"""
	Testing all functionalities
"""

#######################################

from argparse import ArgumentParser
import sptm

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "1.1"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

if __name__ == '__main__':

	# Parse command-line arguments
	parser = ArgumentParser()
	parser.add_argument("-i", "--input-path", \
			help="Path to input file", type=str)
	parser.add_argument("-m", "--mallet-path", \
			help="Path to Mallet binary", type=str)
	parser.add_argument("-l", "--labels-path", \
			help="Path to labels", type=str)
	ARGS = parser.parse_args()

	"""
	Test Corpus object
	"""
	# Simple corpus object
	corpus_custom = sptm.Corpus(ARGS.input_path)

	# Read the reviews form the file
	corpus_custom.read_reviews()

	# Split the review into sentences
	corpus_custom.split_sentence()

	# Tokenize the data
	corpus_custom.tokenize_custom()

	# Write out both the processed files
	corpus_custom.write_processed("custom_corpus.csv")

	"""
	Test Model object:
	"""
	# New model object
	model_load = sptm.Model(ARGS.mallet_path, tokens=corpus_custom.tokens, input_path='custom_corpus.csv')

	# Fit the tokens
	model_load.fit()

	# Define model parameters
	model_load.params(num_topics=65)

	# Train the model
	model_load.train()

	# Print the topics
	print(model_load.topics(num_topics=65))

	# Save model
	model_load.save("LDA_MALLET")

	# Compute the coherence score of the model
	print(model_load.get_coherence())

	# Train multiple models to get optimal topic number
	print(model_load.optimum_topic())

	# Get gensim Mallet LDA wrapper object
	model = model_load.lda_model_mallet

	"""
	Test TopicDistanceMap object:
	"""
	# Make the new
	Map = sptm.TopicDistanceMap(model, "test/test_labels.csv")

	# Compute the intertopic distance
	Map.intertopic_distance()

	# Save the distances
	Map.save_dist("matrix.csv")

	# Plot the map
	Map.plot_map()

	"""
	Test ConditionalMatrix object:
	"""
	# Initialize the object
	cond = sptm.ConditionalMatrix(doctopics_path="LDA_MALLET_doctopic", tokens_path="custom_corpus.csv")

	# Construct the matrix
	cond.construct_matrix()

	# Sort and label the matrix
	cond.sort_and_label(labels_path=ARGS.labels_path)

	# Display the matrix
	print(cond.sorted)

	"""
	Test Inferencer object:
	"""
	# Initialize object
	inference = sptm.Inferencer(model, model_load.id2word)

	# Display the topic distribution
	print(inference.infer(["There was a lot of noise"], 2, 1))
