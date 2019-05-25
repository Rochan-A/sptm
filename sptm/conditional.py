# -*- coding: utf-8 -*-

"""
    Compute conditional probability matrix
"""

#######################################

import csv
import ast
import operator
import numpy as np

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "1.1"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

class ConditionalMatrix:
    """Compute the conditional matrix of topics

    From the data used to train the LDA model, make a matrix of topics vs
    topics and compute the conditional probability of topic B occuring after
    topic A. Take this matrix and process it (sort and label it).

    Attributes:
        doc_matrix: Output from training the LDA model provided by Mallet.
            Contains the topic probabilities of each sentence.
        data_index: list containing the data index number for each sentence.
        num_sent: Number of sentences
        num_topics: Number of topics
        topic_freq: Sum of the weights for a topic over the whole dataset
        freq_matrix: Matrix of floats (conditional probabilities)
        labels: List of strings, labels for each topic, has to be manually
            labeled
        labeled: freq_matrix with labels
        sorted: freq_matrix with labels and sorted in decending order
    """

    def __init__(self, doctopics_path, tokens_path):
        """Inits ConditionalMatrix with path to document topic file and tokens
        file

        Compute the conditional probability matrix of each sentence
        versus another. Open the document topic file, Get the data
        number for every sentence used

        Args:
            doctopics_path: Location of the document topic file
            tokens_path: Path to token file
        Raises:
            IOError: File not found
            Exception: Error while reading a row (Mostly due to empty row)
        """
        self.doc_matrix = []
        try:
            with open(doctopics_path, 'r') as F:
                reader = csv.reader(F, delimiter='\t')
                for row in reader:
                    # Delete the first two columns in the file
                    self.doc_matrix.append(row[2:])
        except IOError:
            raise IOError('File not found')
        except Exception:
            raise Exception('Error reading doctopic file')

        self.data_index = []
        try:
            with open(tokens_path, 'rU') as F:
                reader = csv.reader((line.replace('\0', '') for line in F), \
                                                                delimiter=',')
                for row in reader:
                    try:
                        if len(row) > 0:
                            self.data_index.append(int(row[0]))
                    except Exception:
                        raise Exception('Some error while reading the row')
        except IOError:
             raise IOError('Error reading doctopic file')
        self.num_sent = len(self.doc_matrix)
        self.num_topics = len(self.doc_matrix[0])

    def construct_matrix(self):
        """Compute the conditional probabilities

        Construct a simple frequency matrix of each topic (current sentence)
        vs topic (next sentence), Identify the topics with high probabilities
        for each sentence

        Raises:
            Exception: Sentence Missing, you can ignore this message
        """

        # Create a dictionary of all the topic frequencies
        self.topic_freq = dict()
        for i in range(0, self.num_topics):
            self.topic_freq[i] = 0

        # Construct an empty matrix
        self.freq_matrix = np.zeros((self.num_topics, self.num_topics), \
                                                                dtype=float)

        # Iterate over all the (sentences - 1)
        for i in range(self.num_sent - 1):

            try:
                if self.data_index[i] == self.data_index[i + 1]:
                    topic_dict = [dict(), dict()]
                    for j in range(0, self.num_topics):
                        topic_dict[0][j] = \
                                    ast.literal_eval(self.doc_matrix[i][j])
                        topic_dict[1][j] = \
                                ast.literal_eval(self.doc_matrix[i + 1][j])

                    for x in range(self.num_topics):
                        for y in range(self.num_topics):
                            self.freq_matrix[x][y] += \
                                float(topic_dict[1][y])*float(topic_dict[0][x])
                            self.topic_freq[x] += float(topic_dict[0][x])
            except Exception:
                raise Exception('Sentence Missing, can ignore this message')

        # Conditional probability
        for i in range(self.num_topics):
            for j in range(self.num_topics):
                if float(self.topic_freq[i]) != 0:
                    self.freq_matrix[i][j] = \
                                            (float(self.freq_matrix[i][j]) / \
                                            float(self.topic_freq[i])) * 65

    def sort_and_label(self, labels_path):
        """Sort and label each value in the matrix

        Args:
            labels_path: Path to a labels file
        Raises:
            IOError: Labels file not found
            Exception: Error matching topics and labels, Error sorting
                Conditional Probabilities
        """

        self.labels = []
        try:
            with open(labels_path, 'r') as F:
                reader = csv.reader(F, delimiter=',')
                for row in reader:
                    self.labels.append(row)
        except IOError:
            raise IOError('Labels file not found')

        self.labeled = []
        try:
            for i in range(self.num_topics):
                self.labeled.append({})
                self.labeled[i]['label'] = self.labels[i][0]
                for j in range(self.num_topics):
                    self.labeled[i][self.labels[j][0]] = self.freq_matrix[i][j]
        except Exception:
            raise Exception('Error matching topics and labels')

        self.sorted = []
        try:
            for i in range(self.num_topics):
                sort_row = sorted(self.labeled[i].items(), \
                                                    key=operator.itemgetter(1))
                self.sorted.append(sort_row)
        except Exception:
            raise Exception('Error sorting Conditional Probabilities')

    def save(self, output_path, matrix):
        """Save matrix

        Args:
            output_path: Location with filename to save matrix
            matrix: Matrix to save
        Raises:
            IOError: Output path does not exist
        """
        try:
            with open(output_path, 'w') as F:
                writer = csv.writer(F, delimiter=',')
                for r in matrix:
                    writer.writerow(r)
        except IOError:
            raise IOError('Path does not exist')
