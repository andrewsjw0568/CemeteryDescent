import random
from Individual import Individual
import uuid


class Population:
    """
    Represents a population of individuals.
    """
    def __init__(self, N, inheritance_rule, mean_offspring=10, sd_offspring=0.5):
        self.N = N                                  # Population size
        self.inheritance_rule = inheritance_rule    # Inheritance rule
        self.mean_offspring = mean_offspring        # mean number of offspring, 2.5?
        self.sd_offspring = sd_offspring            # standard deviation of offspring 1?
        self.individuals = []                       # List of individuals
        self.init_founders()                        # Set-up the founders
        self.inheritance_rule_bilineal = []         # Store generational rule for bilineal inheritance

    def init_founders(self):
        """Initialize population with ceil(N/2) males and floor(N/2) females, unique haplotypes."""
        males_founders = [Individual('M') for _ in range(self.N - self.N // 2)]
        females_founders = [Individual('F') for _ in range(self.N // 2)]
        self.individuals = males_founders + females_founders
        self.inherit_founder(males_founders, females_founders)
        self.inheritance_rule_bilineal = []
        """Find mates for each founder from other founders population"""
        count = 0
        for female in females_founders:
            female.spouse = males_founders[count]   # Some males may be left unpaired
            males_founders[count].spouse = female          # Complete the couple
            count = count + 1                       # Increment to next male
        print(self.inheritance_rule.pval)

    def inherit_founder(self, males, females):
        # Set the founder inheritor
        if self.inheritance_rule.current_type(0) == 'patrilineal':
            males[0].inheritor = True
        elif self.inheritance_rule.current_type(0) == 'matrilineal':
            females[0].inheritor = True
        elif self.inheritance_rule.current_type(0) == 'bilineal':
            if self.inheritance_rule.pval <= random.uniform(0, 1):  # Matrilineal, probably should record outcome
                # self.inheritance_rule_bilineal.append('matrilineal')
                females[0].inheritor = True
                print('matrilineal')
            else:                                # Patrilineal
                # self.inheritance_rule_bilineal.append('patrilineal')
                males[0].inheritor = True

    def find_inheritor(self):
        # Identify the inheritor and spouse.
        for individual in self.individuals:
            if individual.inheritor == True:
                return individual

    def find_inheritor_population(self, population):
        # Identify the inheritor and spouse.
        for individual in population:
            if individual.inheritor == True:
                return individual

    def get_inheritance_type(self, current_gen):
        if self.inheritance_rule.current_type(current_gen) != 'bilineal':
            effective_type = self.inheritance_rule.current_type(current_gen)
        elif self.inheritance_rule.current_type(0) == 'bilineal':
            if self.inheritance_rule.pval <= random.uniform(0, 1):  # Matrilineal, probably should record outcome
                self.inheritance_rule_bilineal.append('matrilineal')
                print('matrilineal')
            else:                                # Patrilineal
                self.inheritance_rule_bilineal.append('patrilineal')
            effective_type = self.inheritance_rule_bilineal[-1]

        return effective_type

    def mate_and_reproduce_inheritors(self, current_gen=1):
        # Identify the inheritor and spouse.
        inheritor = self.find_inheritor()
        spouse = inheritor.spouse

        if inheritor.sex == 'M':
            father = inheritor
            father.print_individual
            mother = spouse
        else:
            mother = inheritor
            father = spouse

        # Get current inheritance type
        effective_type = self.get_inheritance_type(current_gen)

        # Produce offspring
        next_gen = []
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

        # Maintain population size
        number_of_males = self.number_of_gender('M', next_gen)
        number_of_females = self.number_of_gender('F', next_gen)

        # Find inheritor from list of children
        inheritor= self.find_inheritor_population(next_gen)

        if inheritor.sex == 'M':
            if number_of_females < self.N//2-1: # Need to add more females
                next_gen.append(Individual('F', str(uuid.uuid4()), None))
            spouse = Individual('F', str(uuid.uuid4()), None)
            inheritor.spouse = spouse
            spouse.spouse = inheritor
            next_gen.append(spouse)
            number_of_females = self.number_of_gender('F', next_gen)
            if number_of_females + number_of_males < self.N: # Need to add more males
                next_gen.append(Individual('M', str(uuid.uuid4()), str(uuid.uuid4())))
        else:
            if number_of_females < self.N//2: # Need to add more females
                next_gen.append(Individual('F', str(uuid.uuid4()), None))
            number_of_females = self.number_of_gender('F', next_gen)
            if number_of_females + number_of_males < self.N-1: # Need to add more males
                next_gen.append(Individual('M', str(uuid.uuid4()), str(uuid.uuid4())))
            spouse = Individual('M', str(uuid.uuid4()), str(uuid.uuid4()))
            inheritor.spouse = spouse
            spouse.spouse = inheritor
            next_gen.append(spouse)

        self.individuals = next_gen

    def number_of_gender(self, sex_string, population):
        gender_count = 0
        for individual in population:
            if individual.sex == sex_string:
                gender_count = gender_count + 1
        return gender_count

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
