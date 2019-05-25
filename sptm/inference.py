# -*- coding: utf-8 -*-

"""
    Inferencer functions
"""

#######################################

import numpy as np

import sptm.preprocess

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "1.1"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

class Inferencer:
    """Inferncer object to compute probability of next sentence given the
    current sentence

    Attributes:
        model: LDA Mallet model
        dictionary: Dictionary used to train LDA model
    """

    def __init__(self, model, dictionary):
        """Inits Inferencer with model and vocabulary dictionary

        Args:
            model: sptm.Model object
            dictionary: sptm.Model.id2word
        """
        self.model = model
        self.dictionary = dictionary

    def infer(self, query, sentence_ml=2, token_ml=1):
        """Run an inference on the query

        NOTE: use the same minimum lengths here as used during preprocessing

        Args:
            query: List of reviews
            sentence_ml: Minimum length of the sentence in words
            token_ml: Minimum length of the tokens in characters
        Returns:
            List of topics with their probability
        """
        query_corpus = sptm.preprocess.Corpus(None, query, None, None)
        query_corpus.split_sentence(min_len=sentence_ml)
        query_corpus.tokenize_custom(min_len=token_ml)
        query_bow = self.dictionary.doc2bow(query_corpus.tokens)
        return self.model.get_document_topics(query_bow)
