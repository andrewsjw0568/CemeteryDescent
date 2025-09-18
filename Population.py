import random
from Individual import Individual
import uuid


class Population:
    """
    Represents a population of individuals.
    """
    def __init__(self, N, inheritance_rule, mean_offspring=3, sd_offspring=0.5):
        self.N = N
        self.inheritance_rule = inheritance_rule
        self.mean_offspring = mean_offspring
        self.sd_offspring = sd_offspring
        self.individuals = []
        self.init_founders()

    def init_founders(self):
        """Initialize population with N/2 males and N/2 females, unique haplotypes."""
        males = [Individual('M') for _ in range(self.N // 2)]
        females = [Individual('F') for _ in range(self.N - self.N // 2)]
        self.individuals = males + females

    def mate_and_reproduce(self, current_gen=1):
        """
        Perform one generation of mating with exogamy based on inheritance rules.
        Only the inheritor brings in an exogamous spouse.
        """
        next_gen = []
        males = [ind for ind in self.individuals if ind.sex == 'M']
        females = [ind for ind in self.individuals if ind.sex == 'F']
        couples = min(len(males), len(females), self.N // 2)
        random.shuffle(males)
        random.shuffle(females)

        for i in range(couples):
            father = males[i]
            mother = females[i]

            # Determine inheritor and spouse sex
            effective_type = self.inheritance_rule.current_type(current_gen)
            if effective_type == 'matrilineal':
                inheritor_parent = mother
                spouse_sex = 'M'
            elif effective_type == 'patrilineal':
                inheritor_parent = father
                spouse_sex = 'F'
            else:  # bilineal
                if random.random() < 0.5:
                    inheritor_parent = father
                    spouse_sex = 'F'
                else:
                    inheritor_parent = mother
                    spouse_sex = 'M'

            # Create exogamous spouse
            print('Spouse:')
            spouse_mtDNA = str(uuid.uuid4())
            spouse_Y = str(uuid.uuid4()) if spouse_sex == 'M' else None
            spouse = Individual(spouse_sex, spouse_mtDNA, spouse_Y)
            inheritor_parent.spouse = spouse
            spouse.spouse = inheritor_parent
            print(f"Spouse mtDNA: {spouse.mtDNA}")
            print(f"Spouse Y: {spouse.Y}")

            # Produce offspring
            num_offspring = max(0, round(random.gauss(self.mean_offspring, self.sd_offspring)))
            children = []
            for _ in range(num_offspring):
                sex = random.choice(['M', 'F'])
                mtDNA = mother.mtDNA  # mtDNA always from mother
                Y = father.Y if sex == 'M' else None
                child = Individual(sex, mtDNA, Y)
                children.append(child)
                next_gen.append(child)

            # Assign single eldest inheritor
            self.inheritance_rule.assign_inheritors(children, generation=current_gen)

        # Cap population to N
        if len(next_gen) > self.N:
            next_gen = random.sample(next_gen, self.N)
        self.individuals = next_gen
        self.print_population(current_gen)

    def print_population(self, generation):
        """
        Print the full population with sex, mtDNA, Y-DNA, and inheritor status.

        Args:
            generation (int): Current generation number.
        """
        print(f"\n--- Generation {generation} ---")
        for i, ind in enumerate(self.individuals, 1):
            print(f"ID {i}: Sex={ind.sex}, mtDNA={ind.mtDNA}, Y-DNA={ind.Y}, "
                  f"Inheritor={ind.inheritor}")

    def print_inheritors(self, generation):
        """
        Print all inheritors in the population with sex, mtDNA, Y-DNA.

        Args:
            generation (int): Current generation number.
        """
        inheritors = [ind for ind in self.individuals if ind.inheritor]
        print(f"\n--- Generation {generation} Inheritors ---")
        if not inheritors:
            print("No inheritors in this generation.")
            return

        for i, ind in enumerate(inheritors, 1):
            print(f"ID {i}: Sex={ind.sex}, mtDNA={ind.mtDNA}, Y-DNA={ind.Y}")
