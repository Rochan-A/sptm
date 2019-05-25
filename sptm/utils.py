# -*- coding: utf-8 -*-

"""
    Utility functions
"""

#######################################

__author__ = "Rochan Avlur Venkat"
__credits__ = ["Anupam Mediratta"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Rochan Avlur Venkat"
__email__ = "rochan170543@mechyd.ac.in"

#######################################

def force_unicode(string, encoding='utf-8', errors='ignore'):
    """Force converts a string to unicode object

    Treats bytestrings using the 'encoding' codec.

    Args:
        string: string to be encoded
        encoding: encoding type, defaults to `utf-8`
        errors: whether or not to ignore errors, defaults to `ignore`

    Returns:
        unicode object

    Raises:
        TypeError: string argument left empty
    """

    if string is None:
        raise TypeError('Function call has string argument left empty')

    try:
        if not isinstance(string, basestring,):
            if hasattr(string, '__unicode__'):
                string = unicode(string)
            else:
                try:
                    string = unicode(str(string), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(string, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    string = ' '.join([force_unicode(arg, encoding, errors) for arg in string])
        elif not isinstance(string, unicode):
            # Note: We use .decode() here, instead of unicode(string, encoding,
            # errors), so that if string is a SafeString, it ends up being a
            # SafeUnicode at the end.
            string = string.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(string, Exception):
            raise UnicodeDecodeError(string, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            string = ' '.join([force_unicode(arg, encoding, errors) for arg in string])
    return string
