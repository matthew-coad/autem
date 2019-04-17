class ParameterEvaluation:

    def __init__(self):
        self.predicted_score = None
        self.predicted_score_std = None
        self.contribution_count = None

def get_parameter_evaluation(member):
    parameter_evaluation = member.get_evaluation("parameter_evaluation", lambda: ParameterEvaluation())
    return parameter_evaluation

def set_parameter_evaluation(member, evaluation):
    member.set_evaluation("parameter_evaluation", evaluation)

class ParameterModel:

    def __init__(self, model, contribution_count):
        self.model = model
        self.contribution_count = contribution_count

class ParameterModelResources:

    def __init__(self):
        self.models = {}

def get_parameter_models(specie):
    resources = specie.get_resource("parameter_models", lambda: ParameterModelResources())
    return resources

