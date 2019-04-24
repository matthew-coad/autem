class SpecieManager:

    def configure_specie(self, specie):
        """
        Configure the epoch
        Value is the first component that returns a Non-Null value
        """
        pass

    def prepare_specie(self, specie):
        """
        Start a specie
        """
        pass

    def is_specie_finished(self, specie):
        """
        Is the specie finished.
        Value is the first component that returns a Non-Null value
        """
        return (None, None)

    def judge_specie(self, specie):
        """
        Judge the specie
        """
        pass

    def finish_specie(self, specie):
        """
        Finish an speciee
        """
        pass

    def bury_specie(self, specie):
        """
        Finish an speciee
        """
        pass


class SpecieManagerContainer:

    def list_specie_managers(self):
        managers = [c for c in self.list_components() if isinstance(c, SpecieManager) ]
        return managers
