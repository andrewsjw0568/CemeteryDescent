# CemeteryDescent

Code relating to V-KEMS Problem 2: Cambridge archaeology

---

## Overview

This project provides Python code to simulate or analyse descent / inheritance rules over populations of individuals, under different models of kinship: patrilineal, matrilineal, bilineal, etc. It seems designed for archaeological / anthropological modelling, for descent of property, status, or lineage.

---

## Contents

| File | Purpose |
|---|---|
| `Cemetery.py` | Core logic for modelling a “cemetery” of individuals, i.e. a population with relationships, possibly burial data, etc. Determines the rules for being buried in the Cemetery and stores the mtDNA and Y-Chromosomal data generationally for those who are buried in the Cemetery.
| `Individual.py` | Defines the `Individual` class, with attributes of each person, e.g. sex/gender, parentage, etc. |
| `InheritanceRule.py` | Encapsulates rules for inheritance (how inheritance is passed: patrilineal, matrilineal, bilineal) and applies them. |
| `Population.py` | Perhaps builds / maintains subpopulations, simulates growth, connects many `Individual` objects. |
| `Example_patrilineal.py` | Example demonstrates usage script demonstrating patrilineal descent rules. |
| `Example_matrilineal.py` | Example demonstrates usage demonstrating matrilineal descent rules. |
| `Example_bilineal.py` | Example usage script demonstrating bilineal descent rules. |
| `theoretical_plots.py` | Scripts to produce theoretical plots (expected outcomes under different descent rules, over generations). |

---

## Getting Started

### Prerequisites

* Python 3.x  
* Standard Python packages 

  * uuid

  * random

  * collections

  * numpy

  * matplotlib

### Installation

Clone the repository:

```bash
git clone https://github.com/andrewsjw0568/CemeteryDescent.git
cd CemeteryDescent
