from .feedback import Feedback

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

class ConsoleFeedback(Feedback):
    """
    Feedback object that reports directly to the console.
    """

    def __init__(self):
        self._progress_reported = False

    def report(self, value, *args):
        """
        Feedback report
        """
        if self._progress_reported:
            print()
            self._progress_reported = False
        print(value, *args)

    def progress(self, iteration, total, prefix = '', suffix = ''):
        """
        Report progress
        """
        printProgressBar(iteration, total, prefix, suffix, length = 50)        
        self._progress_reported = True
