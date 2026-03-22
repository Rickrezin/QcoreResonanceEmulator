# QCore Emulator v0.7 — Resonance-Aware Simulator with Element Matching
# ---------------------------------------------------------------------

import sys, math

# constants
h = 6.62607015e-34
phi = (1 + math.sqrt(5)) / 2

# optional resonance lookup (Hz)
element_resonances = {
    "H": 1e14, "C": 2e13, "N": 2.5e13, "O": 5e13,
    "P": 3.2e13, "S": 3.5e13, "Mg": 7e13, "Ti": 3e13, "Fe": 4e13,
}

# full periodic table → QCore states
element_class_map = {
    "H": "C", "He": "N", "Li": "O", "Be": "O", "B": "C", "C": "C", "N": "C", "O": "D", "F": "C", "Ne": "N",
    "Na": "O", "Mg": "D", "Al": "O", "Si": "O", "P": "O", "S": "O", "Cl": "O", "Ar": "N",
    "K": "O", "Ca": "R", "Sc": "O", "Ti": "C", "V": "O", "Cr": "O", "Mn": "O", "Fe": "C", "Co": "C", "Ni": "C",
    "Cu": "O", "Zn": "O", "Ga": "O", "Ge": "O", "As": "O", "Se": "O", "Br": "D", "Kr": "N",
    "Rb": "O", "Sr": "R", "Y": "O", "Zr": "O", "Nb": "O", "Mo": "O", "Tc": "A", "Ru": "O", "Rh": "O", "Pd": "C",
    "Ag": "C", "Cd": "O", "In": "O", "Sn": "O", "Sb": "O", "Te": "O", "I": "R", "Xe": "N",
    "Cs": "O", "Ba": "R", "La": "O", "Ce": "O", "Pr": "O", "Nd": "O", "Pm": "A", "Sm": "O", "Eu": "R", "Gd": "O",
    "Tb": "O", "Dy": "O", "Ho": "O", "Er": "O", "Tm": "O", "Yb": "O", "Lu": "O", "Hf": "O", "Ta": "O", "W": "O",
    "Re": "O", "Os": "O", "Ir": "O", "Pt": "C", "Au": "C", "Hg": "O", "Tl": "O", "Pb": "A", "Bi": "O", "Po": "O",
    "At": "A", "Rn": "N",
    "Fr": "A", "Ra": "A", "Ac": "O", "Th": "O", "Pa": "O", "U": "A", "Np": "A", "Pu": "A", "Am": "A", "Cm": "A",
    "Bk": "A", "Cf": "A", "Es": "A", "Fm": "A", "Md": "A", "No": "A", "Lr": "A", "Rf": "O", "Db": "O", "Sg": "O",
    "Bh": "O", "Hs": "O", "Mt": "A", "Ds": "A", "Rg": "A", "Cn": "A", "Nh": "A", "Fl": "A", "Mc": "A", "Lv": "A",
    "Ts": "A", "Og": "A"
}

# reverse lookup: state → elements
reverse_map = {}
for elem, state in element_class_map.items():
    reverse_map.setdefault(state, []).append(elem)

# meanings
states = {
    "C": "Yes (Convergence)",
    "D": "No (Divergence)",
    "O": "Maybe (Offset)",
    "R": "Could be (Return)",
    "N": "Neutral",
    "A": "Huh? (Anomaly)"
}

# transitions
transition = {
    "C": {"C":"C", "D":"N", "O":"R", "R":"R", "N":"C", "A":"A"},
    "D": {"C":"N", "D":"D", "O":"D", "R":"R", "N":"D", "A":"A"},
    "O": {"C":"R", "D":"D", "O":"C", "R":"R", "N":"O", "A":"A"},
    "R": {"C":"R", "D":"R", "O":"R", "R":"R", "N":"R", "A":"A"},
    "N": {"C":"C", "D":"D", "O":"O", "R":"R", "N":"N", "A":"A"},
    "A": {"C":"A", "D":"A", "O":"A", "R":"A", "N":"A", "A":"A"},
}

colors = {"C":"\033[92m","D":"\033[91m","O":"\033[93m","R":"\033[94m","N":"\033[90m","A":"\033[95m","END":"\033[0m"}

def combine(a, b): return transition[a][b]

def show_step(a, b):
    result = combine(a, b)
    print(f"{colors[a]}{a}{colors['END']} ⊕ {colors[b]}{colors['END']} "
          f"= {colors[result]}{result}{colors['END']} → {states[result]}")
    return result

def run_chain(seq):
    print("\nRunning QCore chain:", seq)
    current = seq[0]
    for next_state in seq[1:]:
        current = show_step(current, next_state)

    print(f"\nFinal state: {colors[current]}{current}{colors['END']} → {states[current]}")
    matches = reverse_map.get(current, [])
    if matches:
        print(f"Elements with state {current}: {', '.join(matches[:10])} ... (total {len(matches)})")
    return current

if __name__ == "__main__":
    print("QCore Emulator v0.7 — Resonance-Aware Simulator\n")
    raw_input = sys.argv[1:] if len(sys.argv) > 1 else input("Enter elements or states (e.g. Ti O Mg OR C O D): ").split()
    sequence = []

    for token in raw_input:
        t = token.capitalize()
        if t in element_class_map:
            sequence.append(element_class_map[t])
        elif t.upper() in states:
            sequence.append(t.upper())
        else:
            print(f"Unknown input: {t}")

    if sequence:
        run_chain(sequence)
