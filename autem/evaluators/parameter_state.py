class ParameterEvaluation:

    def __init__(self):
        self.predicted_score = None
        self.predicted_score_std = None

def get_parameter_evaluation(member):
    parameter_evaluation = member.get_evaluation("parameter_evaluation", lambda: ParameterEvaluation())
    return parameter_evaluation

class ParameterModelResources:

    def __init__(self):
        self.score_models = {}

def get_parameter_models(specie):
    resources = specie.get_resource("parameter_models", lambda: ParameterModelResources())
    return resources
