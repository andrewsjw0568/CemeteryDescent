import uuid

class Individual:
    """
    Represents an individual in the population.
    """
    def __init__(self, sex, mtDNA=None, Y=None):
        """
        Args:
            sex (str): 'M' or 'F'
            mtDNA (str, optional): mtDNA haplotype. Auto-generated if None.
            Y (str, optional): Y chromosome haplotype. Auto-generated if None and male.
        """
        self.sex = sex            # 'M' or 'F'
        self.mtDNA = mtDNA or str(uuid.uuid4())
        self.Y = Y if Y is not None else (str(uuid.uuid4()) if sex == 'M' else None)
        self.spouse = None        # Reference to spouse
        self.children = []        # List of children
        self.inheritor = False    # True if this individual is the inheritor

    def print_individual(self):
        if self.Y is None:
            print(f"sex: {self.sex}, mtDNA: {self.mtDNA}, Y: None")
        else:
            print(f"sex: {self.sex}, mtDNA: {self.mtDNA}, Y: {self.Y}")