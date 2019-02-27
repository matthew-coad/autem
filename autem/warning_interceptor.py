# Warnings intercept

# Some modules in Sklearn don't respect the warnings filters
# Its important to be able to intercept warnings so we can discard models that
# have problems. In general if a model raises Warnings we simply aren't interested
# in it.

import warnings

import sklearn.exceptions

_current_interceptor = None
_prior_warn = warnings.warn

class WarningInterceptor:

    def __enter__(self):
        global _current_interceptor
        warnings.resetwarnings()
        warnings.simplefilter("error", RuntimeWarning)
        _current_interceptor = self
        self.messages = []
        return self.messages

    def __exit__(self, type, value, traceback):
        global _current_interceptor
        _current_interceptor = None
        warnings.resetwarnings()
        return False

    def intercept_message(self, message):
        if isinstance(message, sklearn.exceptions.ConvergenceWarning):
            return True
        if isinstance(message, UserWarning):
            return True            
        return False

    def warn(self, message, category, stacklevel, source):
        if isinstance(message, Warning):
            text = str(message)
            category = message.__class__
        else:
            text = message
            message = category(message)
        intercept = self.intercept_message(message)
        if intercept:
            self.messages.append(message)
        return intercept

def _override_warn(message, category=None, stacklevel=1, source=None):

    intercepted = False
    if not _current_interceptor is None:
        intercepted = _current_interceptor.warn(message, category, stacklevel, source)
    if not intercepted:
        _prior_warn(message, category, stacklevel, source)

warnings.warn =  _override_warn   

