# -*- coding: utf-8 -*-

"""
    Preprocess the data
"""

#######################################

import re
import logging
import io

import spacy
import gensim

from sptm.utils import force_unicode

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

# Setup logging for gensim
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                                                            level=logging.INFO)

# Setup spacy model for custom preprocessing of data used in tokenize_custom()
NLP = spacy.load('en_core_web_sm')

class Corpus:
    """Corpus object to handle all pre-processing of data

    read_reviews() method assumes data in the file to be in the following
    format:

    <metadata></t>...</t><data_in_multiple_sentences>

    Data to be preprocessed must be in the last column.

    Attributes:
        path: path to the data file
        raw_review: data read from the file in a list
        sentences: list of lists containing data number and
            sentence
        tokens: list of lists of data index number followed by tokenized
            sentence
    """

    def __init__(self, path=None, raw_review=None, sentences=None,\
                                                                tokens=None):
        """Inits Corpus with path, raw_review, sentences and tokens if passed

        One can directly pass semi processed data at different stages and use
        methods provided in the class to complete the preprocessing.

        Args:
            path: Path to data file
            raw_review: data in a list
            sentences: list of lists containing data index number and sentences
            tokens: list of lists of data index number followed by tokenized
                sentence
        """
        self.path = path
        self.raw_review = raw_review if (raw_review is not None) else []
        self.sentences = sentences if (sentences is not None) else []
        self.tokens = tokens if (tokens is not None) else []

    def read_reviews(self, delimiter='\t', reg=r"(\\u[0-z][0-z][0-z])\w",\
                                                                    rep=" "):
        """Read reviews and store it in a list

        Args:
            delimiter: The seperator between data
            reg: Custom regex to filter
            rep: String to replace the regex values

        Raises:
            IOError: file not found
            Exception: Data format in the file opened does not follow the
                specified template style
        """

        # Open the data file
        try:
            with io.open(self.path, 'rb') as raw:
                self.raw_review = [x.strip().split(delimiter) for x in raw]
        except IOError:
            raise IOError('File not found')

        try:
            # Select data only
            for i, val in enumerate(self.raw_review):
                # Take the last column values
                self.raw_review[i] = self.raw_review[i][-1]
                # Run regex
                self.raw_review[i] = re.sub(reg, rep, self.raw_review[i])
        except:
            raise Exception('Data format in the file does not follow template')

    def split_sentence(self, min_len=2):
        """Split each data index into its individual sentences

        Splits data index at periods.

        Args:
            min_len: Minimum length of a sentence above which to include
        """

        # Iterate over every unique data value
        for i, val in enumerate(self.raw_review):
            # Split the sentences
            sentence = self.raw_review[i].split('.')

            # Append the other sentences to the end of the self.sentences
            for j, v in enumerate(sentence):
                # Make sure the sentence has more than <min_len> words
                if len(sentence[j]) > min_len:
                    self.sentences.append([i, sentence[j]])

    def tokenize_simple(self, deacc=False, min_len=2, max_len=15):
        """Processes sentences

        Tokenize, ignore tokens that are too small

        Args:
            deacc: Remove accentuation
            min_len: Minimal length of token in result
            max_len: Maximum length of token in result
        """

        # Simple tokens, de-accent and lowercase processor
        for i, val in enumerate(self.sentences):
            self.tokens.append([self.sentences[i][0], \
            gensim.utils.simple_preprocess(self.sentences[i][1], deacc, \
                                                            min_len, max_len)])

    def tokenize_custom(self, min_len=1):
        """Processes sentences

        Tokenize, ignore tokens that are too small, lemmatize, filter out
        grammar {stop words, symbols, prepositions, numbers etc}

        Args:
            min_len: Minimum length of tokens
        """

        # POS Tagging and filtering sentences
        for i, val in enumerate(self.sentences):
            doc = NLP(force_unicode(self.sentences[i][1]))
            to = [unicode(self.sentences[i][0])]
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
        """Save to file

        Appends tokens to given file

        Args:
            name: Name of file

        Raises:
            IOError: Path does not exist
            Exception: self.tokens structure not supported, manually check its
                value
        """

        try:
            # Write the preprocessed reviews to file
            with io.open(name, "a", encoding='utf8') as outfile:
                for i, val in enumerate(self.tokens):
                    outfile.write(unicode(','.join(self.tokens[i]) + "\n"))
        except IOError:
            raise IOError('Path does not exist')
        except Exception:
            raise Exception('Error while saving file, check self.tokens value')
