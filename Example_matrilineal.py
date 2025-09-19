from InheritanceRule import InheritanceRule
from Population import Population
import matplotlib.pyplot as plt
from Cemetery import Cemetery

# Define inheritance rule
rule = InheritanceRule(type='matrilineal')

# Population size N
population = Population(N=10, inheritance_rule=rule)

cemetery = Cemetery()

generations = 10  # Number of generations to simulate

# population.print_population(1)  # Founders are set up correctly this is just a debug step

for gen in range(1, generations + 1):
    # Evolve the population
    population.mate_and_reproduce_inheritors(current_gen=gen)

    # Identify the single inheritor
    inheritor = population.find_inheritor()

    # Add inheritor + spouse to cemetery
    cemetery.add_generation([inheritor, inheritor.spouse])

    # print("Population:")
    # population.print_population(gen)


    # Optional: print the cemetery for debugging
    print(f"\nGeneration {gen} Cemetery:")
    if inheritor:
        print(f"Inheritor: Sex={inheritor.sex}, mtDNA={inheritor.mtDNA}, Y-DNA={inheritor.Y}")
        if inheritor.spouse:
            print(f"Spouse: Sex={inheritor.spouse.sex}, mtDNA={inheritor.spouse.mtDNA}, Y-DNA={inheritor.spouse.Y}")
    else:
        print("No inheritor this generation")

mt_traj, y_traj = cemetery.cumulative_diversity_trajectory()
print("\nNei_h trajectory for mtDNA:", mt_traj)
print("Nei_h trajectory for Y-DNA:", y_traj)

plt.plot(range(1, generations + 1), mt_traj, label='mtDNA Nei_h', marker='o')
plt.plot(range(1, generations + 1), y_traj, label='Y-DNA Nei_h', marker='x')
plt.xlabel('Generation')
plt.ylabel("Nei's haplotype diversity (H)")
plt.title("Cemetery Diversity Trajectory")
plt.legend()
plt.show()
