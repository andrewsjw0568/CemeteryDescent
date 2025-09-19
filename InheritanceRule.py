import random

class InheritanceRule:
    """
    Encapsulates inheritance logic for a population.

    Supports the following inheritance types:
        - 'matrilineal'  : inheritance passes through female descendants
        - 'patrilineal'  : inheritance passes through male descendants
        - 'bilineal'     : inheritance may pass through male or female descendants
                           (stochastically determined by `pval`)
        - 'transitional' : (not fully implemented) placeholder for rules that
                           change after a certain generation
    """
    def __init__(self, type='matrilineal', transition_gen=None):
        """
        Initialize an inheritance rule.

        Args:
            type (str): Inheritance type. One of:
                        'matrilineal', 'patrilineal', 'bilineal', or 'transitional'.
            transition_gen (int, optional): Generation number when the inheritance
                        system changes (used only for transitional mode).
        """
        self.type = type
        self.transition_gen = transition_gen  # Feature not fully implemented
        self.pval = 0.1                       # Probability of matrilineal descent

    def current_type(self, generation):
        """
        Return the effective inheritance type at a given generation.

        Args:
            generation (int): The generation index being evaluated.

        Returns:
            str: Effective inheritance type for this generation.
        """
        if self.type == 'transitional' and self.transition_gen and generation >= self.transition_gen:
            return self.type
        return self.type

    def assign_inheritors(self, children, generation=None):
        """
        Assign the eldest eligible child as the inheritor based on inheritance type.

        Notes:
            - Only one inheritor is chosen per generation.
            - "Eldest" is assumed to be the first element of the `children` list.
              (If age is explicitly tracked in `Individual`, this could be refined.)

        Args:
            children (list): List of child `Individual` objects.
            generation (int, optional): Current generation index.
        """
        if not children:
            return

        # Filter candidates based on inheritance type
        effective_type = self.current_type(generation)
        if effective_type == 'matrilineal':
            candidates = [c for c in children if c.sex == 'F']
        elif effective_type == 'patrilineal':
            candidates = [c for c in children if c.sex == 'M']
        else:
            if self.pval <= random.uniform(0, 1): # Matrilineal
                candidates = [c for c in children if c.sex == 'F']
            else:
                candidates = [c for c in children if c.sex == 'M']

        if candidates:
            # Eldest is simply the first in the list (or could be age attribute)
            inheritor = candidates[0]
            inheritor.inheritor = True
