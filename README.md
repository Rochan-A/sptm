# sptm: Sentence Topic Prediction using Topic Modeling

![sptm logo](img/sptm-logo.png)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/Rochan-A/sptm/blob/master/LICENSE)

## Quick rundown

sptm is a high-level API, written in Python and capable of training Topic Models using [Gensim](https://github.com/rare-technologies/gensim) and [MALLET](http://mallet.cs.umass.edu/). It was developed as a summer internship project under the guidance of [@Anupam Mediratta](https://github.com/anupamme). The package was wriiten with a focus on enabling fast experimentation. *Being able to go from idea to result with the least possible delay is key to doing good research.*

Use sptm if you need a library that:

- Allows for easy and fast topic model training
- Draw Inter-topic Distance Maps
- Construct Conditional Probability Matrix for topics
- Predict topic of sentences

Read the documentation at [sptm_source]/docs/_build/html/index.html.

sptm is compatible (tested) with: __Python 2.7__.

------------------

## Some good stuff about sptm

- __User friendliness.__ The source code is very simple to follow

- __Modularity.__ You can use your own models, training algorithms etc. as long as it is supported by gensim

------------------

## Getting started: 30 seconds to sptm

In the [test folder](https://github.com/Rochan-A/sptm/tree/master/test) of the repository, you will find a single script with almost all classes and functions used.

------------------


## Installation

- **Important**

sptm makes use of MALLET whose installtion steps can be found [here](http://mallet.cs.umass.edu/download.php).

This is required only if you want to train the topic model using gensim's LDAMallet wrapper that is the default training algorithm used in sptm.

Then, you can install sptm itself. There are two ways to install sptm:

- **Install sptm from PyPI (recommended):**

```sh
sudo pip install sptm
```

If you are using a virtualenv, you may want to avoid using sudo:

```sh
pip install sptm
```

- **Alternatively: install sptm from the GitHub source:**

First, clone sptm using `git`:

```sh
git clone https://github.com/Rochan-A/sptm.git
```

 Then, `cd` to the sptm folder and run the install command:
```sh
cd sptm
sudo python setup.py install
```

- **NOTE: You will need to specifically download spacy's **en_core_web_sm** model.**

This step needs to be done irrespective the method of installation.

You can do that by running:

```sh
python -m spacy download en_core_web_sm
```
------------------

## Support

You can post **bug reports and feature requests** in [GitHub issues](https://github.com/Rochan-A/sptm/issues). Make sure to read the [guidelines](https://github.com/Rochan-A/sptm/blob/master/CONTRIBUTING.md) first.

------------------

## Why name it sptm?

sptm stands for - *Sentence topic Prediction using Topic Modeling*

## Why is this readme oddly familiar?

This README is a heavily edited version of [keras's](https://keras.io)

------------------
