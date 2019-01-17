from genetic.components import Component

class LearnerChoice(Component):

    def initializeMember(self, member):
        learners = list(member.configuration.learners.__dict__)
        random_state = member.simulation.random_state
        learner_index = random_state.randint(0, len(learners))
        member.configuration.learner_name = learners[learner_index]

    def copyMember(self, member, parent0):
        member.configuration.learner_name = parent0.configuration.learner_name

    def crossoverMember(self, member, parent0, parent1):
        member.configuration.learner_name = parent0.configuration.learner_name

    def mutateMember(self, member):
        current_learner = member.configuration.learner_name
        learners = list(member.configuration.learners.__dict__)
        learners.remove(current_learner)
        if len(learners) == 0:
            return false

        random_state = member.simulation.random_state
        learner_index = random_state.randint(0, len(learners))
        member.configuration.learner_name = learners[learner_index]
