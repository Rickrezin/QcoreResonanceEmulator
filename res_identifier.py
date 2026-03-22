# QCore Emulator v0.6 — Resonance-Aware Simulator with Full Periodic Table
# ------------------------------------------------------------------------

import json
import math

# Load resonance table from external JSON file
with open("res_table.json", "r", encoding="utf-8") as f:
    resonance_table = json.load(f)

# Build lookup dictionary from symbol
element_data = {entry["symbol"]: entry for entry in resonance_table}

# Mapping from resonance category to QCore state
category_to_state = {
    "Attractor": "C",
    "Offset": "O",
    "Divergent": "D",
    "Return": "R",
    "Neutral": "N",
    "Anomaly": "A"
}

# State meanings
states = {
    "C": "Yes (Convergence)",
    "D": "No (Divergence)",
    "O": "Maybe (Offset)",
    "R": "Could be (Return)",
    "N": "Neutral",
    "A": "Huh? (Anomaly)"
}

# Transition logic
transition = {
    "C": {"C": "C", "D": "N", "O": "R", "R": "R", "N": "C", "A": "A"},
    "D": {"C": "N", "D": "D", "O": "D", "R": "R", "N": "D", "A": "A"},
    "O": {"C": "R", "D": "D", "O": "C", "R": "R", "N": "O", "A": "A"},
    "R": {"C": "R", "D": "R", "O": "R", "R": "R", "N": "R", "A": "A"},
    "N": {"C": "C", "D": "D", "O": "O", "R": "R", "N": "N", "A": "A"},
    "A": {"C": "A", "D": "A", "O": "A", "R": "A", "N": "A", "A": "A"}
}

# Colors for pretty printing
colors = {
    "C": "\033[92m",  # Green
    "D": "\033[91m",  # Red
    "O": "\033[93m",  # Yellow
    "R": "\033[94m",  # Blue
    "N": "\033[90m",  # Grey
    "A": "\033[95m",  # Magenta
    "END": "\033[0m"
}

def combine(a, b):
    return transition[a][b]

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
    return current

if __name__ == "__main__":
    print("QCore Emulator v0.6 — Resonance-Aware Simulator (Full Table Support)\n")

    # 🔧 Edit this list to run any set of element symbols or direct states
    test_input = ["H", "O", "Ti", "Fe", "Pb", "Rn", "D"]

    sequence = []
    for token in test_input:
        t = token.strip().capitalize()
        if t in element_data:
            entry = element_data[t]
            category = entry["category"]
            state = category_to_state.get(category)
            print(f"{t}: {category} → {state} ({states[state]}) — {entry['notes']}")
            sequence.append(state)
        elif t.upper() in states:
            sequence.append(t.upper())
        else:
            print(f"Unknown input: {t}")

    if sequence:
        run_chain(sequence)
