class FitState:
    """
    Contains state information regarding a single scoring fit.
    """

    def __init__(self):
        self.fold_index = None 
        self.score = None 
        self.predictions = None
        self.duration = None
        self.fault = None
        