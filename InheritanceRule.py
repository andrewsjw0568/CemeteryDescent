class InheritanceRule:
    """
    Encapsulates inheritance logic for a population.
    """
    def __init__(self, type='matrilineal', transition_gen=None):
        """
        Args:
            inheritance_type (str): 'matrilineal', 'patrilineal', 'bilineal', or 'transitional'
            transition_gen (int): generation number at which transitional behavior changes
        """
        self.type = type
        self.transition_gen = transition_gen  # Feature not fully implemented

    def current_type(self, generation):
        """Return effective inheritance type at a given generation."""
        if self.type == 'transitional' and self.transition_gen and generation >= self.transition_gen:
            return self.type
        return self.type

    def assign_inheritors(self, children, generation=None):
        """
        Assign the eldest child as the inheritor based on inheritance type.
        Only one inheritor per generation.
        """
        if not children:
            return

        # Filter candidates based on inheritance type
        effective_type = self.current_type(generation)
        if effective_type == 'matrilineal':
            candidates = [c for c in children if c.sex == 'F']
        elif effective_type == 'patrilineal':
            candidates = [c for c in children if c.sex == 'M']
        else:  # bilineal
            candidates = children

        if candidates:
            # Eldest is simply the first in the list (or could be age attribute)
            inheritor = candidates[0]
            inheritor.inheritor = True
