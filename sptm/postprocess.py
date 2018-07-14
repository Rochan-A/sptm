# -*- coding: utf-8 -*-

"""
    Used to graph the Hellingers distance between topic vectors
"""

#######################################

import csv, gensim
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

class TopicDistanceMap:

    def __init__(self, lda_mallet, label_filename):
        """
        Plot an Intertopic Distance Map

        NOTE: You need to pass the gensim Mallet LDA wrapper object.
        Pass Model.return_model() in lda_mallet argument.

        Arguments
        ---------
        lda_mallet: gensim wrapper object for Mallet LDA Model
        label_filename: Location of the labels for each topic,
        one label per line corresponding to the topic
        """
        self.lda_mallet = lda_mallet
        self.topics = self.lda_mallet.get_topics()
        self.num_topics = len(self.topics)
        self.matrix = np.zeros((self.num_topics, self.num_topics + 1), dtype=float)
        self.labels = []
        with open(label_filename, 'r') as F:
            spamwriter = csv.reader(F)
            for row in spamwriter:
                self.labels.append(row)

    def intertopic_distance(self):
        """
        Calculate the Hellinger Distance between all pairwise topic vectors
        """
        for i in range(self.num_topics):
            for j in range(1, self.num_topics + 1):
                self.matrix[i][j] = (gensim.matutils.hellinger(self.topics[i], self.topics[j-1]))

        # Add labels to each row
        for i in range(self.num_topics):
            self.matrix[i][0] = i

    def save_dist(self, filename):
        """
        Save the matrix

        Arguments
        ---------
        filename: Location with filename to save the topic matrix
        """
        with open(filename, 'w') as F:
            spamwriter = csv.writer(F, delimiter=',')
            for row in self.matrix:
                spamwriter.writerow(row)

    def plot_map(self):
        """
        Plot the Map
        """
        dists = []

        for d in self.matrix:
            dists.append(map(float, d[1:]))
            if len(self.labels) == 0:
                self.labels.append(d[0])

        adist = np.array(dists)
        amax = np.amax(adist)
        adist /= amax

        mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
        results = mds.fit(adist)

        coords = results.embedding_

        plt.subplots_adjust(bottom=0.1)
        plt.scatter(coords[:, 0], coords[:, 1], marker='o')
        for label, x, y in zip(self.labels, coords[:, 0], coords[:, 1]):
            plt.annotate( \
                label, \
                xy=(x, y), xytext=(-20, 20), \
                textcoords='offset points', ha='right', va='bottom', \
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5), \
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        plt.show()
