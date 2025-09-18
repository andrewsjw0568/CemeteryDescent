from collections import Counter
import numpy as np

class Cemetery:
    """
    Represents the cemetery (burial site) for the population.
    Stores the inheritor and their spouse from each generation.
    """
    def __init__(self):
        self.generations = []  # List of lists: each generation's burials

    def add_generation(self, inheritor):
        """Add inheritor + spouse for this generation to the cemetery."""
        generation_group = []
        if inheritor:
            generation_group.append(inheritor)
            if inheritor.spouse:
                generation_group.append(inheritor.spouse)
        self.generations.append(generation_group)

    def print_cemetery(self):
        """
        Print all individuals in the cemetery, generation by generation.
        """
        for gen_idx, gen in enumerate(self.generations, start=1):
            print(f"\n--- Generation {gen_idx} Cemetery ---")
            if not gen:
                print("No individuals in this generation.")
                continue
            for i, ind in enumerate(gen, start=1):
                print(f"Individual {i}: Sex={ind.sex}, mtDNA={ind.mtDNA}, Y-DNA={ind.Y}")

    @staticmethod
    def compute_nei_h(haplotypes):
        """Compute sample-corrected Nei's haplotype diversity."""
        n = len(haplotypes)
        if n <= 1:
            return 0
        counts = Counter(haplotypes)
        freqs = np.array([c / n for c in counts.values()])
        D = np.sum(freqs**2)
        return (n / (n - 1)) * (1 - D)

    def diversity_trajectory(self):
        """Compute Nei_h per generation for mtDNA and Y-DNA (non-cumulative)."""
        mt_traj = []
        y_traj = []
        for gen in self.generations:
            mt_haps = [ind.mtDNA for ind in gen]
            y_haps = [ind.Y for ind in gen if ind.Y]
            mt_traj.append(self.compute_nei_h(mt_haps))
            y_traj.append(self.compute_nei_h(y_haps))
        return mt_traj, y_traj

    def cumulative_diversity_trajectory(self):
        """
        Compute cumulative Nei_h diversity for mtDNA and Y-DNA across generations.
        At each generation g, includes all individuals from generations 1..g.
        """
        mt_traj = []
        y_traj = []
        cumulative_individuals = []

        for gen in self.generations:
            cumulative_individuals.extend(gen)
            mt_haps = [ind.mtDNA for ind in cumulative_individuals]
            y_haps = [ind.Y for ind in cumulative_individuals if ind.Y]
            mt_traj.append(self.compute_nei_h(mt_haps))
            y_traj.append(self.compute_nei_h(y_haps))

        return mt_traj, y_traj

    def print_cemetery(self):
        """
        Print all individuals in the cemetery, generation by generation.
        Shows sex, mtDNA, and Y-DNA.
        """
        for gen_idx, gen in enumerate(self.generations, start=1):
            print(f"\n--- Generation {gen_idx} Cemetery ---")
            if not gen:
                print("No individuals in this generation.")
                continue
            for i, ind in enumerate(gen, start=1):
                print(f"Individual {i}: Sex={ind.sex}, mtDNA={ind.mtDNA}, Y-DNA={ind.Y}")