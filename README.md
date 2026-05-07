# QcoreResonanceEmulator
# QCore Resonance Emulator

A material resonance calculator built on the **phi-resonance framework** developed by Richard Jackson / QCore Labs.

---

## What It Does

The emulator takes a chemical formula or reaction as input and returns:

- The **phi-resonance state** of each element in the compound
- The **combined resonance state** of the full formula
- The **total resonance frequency** scaled by φ² (phi squared)
- A **pair compatibility analysis** — which element combinations stabilize or destabilize the compound

---

## The Framework

The phi-resonance framework classifies all 118 elements according to their position on a geometric energy ladder defined by:

**E_n = ℏ · ω · φⁿ**

Where φ (phi) = 1.6180339... (the golden ratio) and n is the rung position on the ladder.

Each element occupies one of six resonance states:

| State | Symbol | Description |
|-------|--------|-------------|
| Convergent | CON | Stable attractor. Strong phi-alignment. |
| Return | RET | Stabilizing. Pulls toward convergence. |
| Neutral | NEU | Transitional. Weakly coupled. |
| Offset | OFF | Bridge state. Conditionally essential. |
| Divergent | DIV | Resists phi-alignment. Reactive. |
| Anomalous | ANOM | No stable rung. Unstable or synthetic. |

When elements combine, their states interact according to defined transition rules to produce a **compound resonance state**.

---

## Example

Input: `H2O`

- H × 2 → RET (Return)
- O × 1 → RET (Return)
- **Final State: RET | Total Resonance: [calculated Hz]**

The water molecule resolves to Return resonance — a stabilizing, convergence-seeking state. This is consistent with water's role as a universal solvent and biological stabilizer.

---

## How To Use

### Web Interface
The live emulator is available at:
`https://rickrezin.github.io/QcoreResonanceEmulator/`

### Local (Python)
```bash
git clone https://github.com/Rickrezin/QcoreResonanceEmulator
cd QcoreResonanceEmulator
pip install tkinter
python Qcore_hybrid.py
```

### Input Format
- Standard chemical formulas: `Fe2O3`, `NaCl`, `H2O`
- Reactions with stoichiometry: `:2 Fe2O3 + H2`
- Nested groups: `Ca(OH)2`

### φ² Mode
The checkbox "Use φ²" applies phi-squared frequency scaling as defined by the framework. This is the default and recommended setting.

---

## What a Result Tells You

The **resonance state** of a compound predicts its harmonic behavior — how the material interacts with resonant energy fields, how stable it is under phi-scaled energy conditions, and whether its elemental components reinforce or oppose each other.

The **pair compatibility scores** show which element pairs in the compound are:
- **Stabilizers** — close atomic radius and electronegativity, reinforce each other
- **Neutral** — compatible but not reinforcing
- **Destabilizers** — large mismatches that introduce instability

---

## Data

- All 118 elements are classified and included
- Frequencies sourced from `resonance_phi2_results.csv`
- Element metadata in `Res_csv.csv`

---

## Independent Testing

This tool makes testable predictions. If you run a compound and want to report your results — whether they confirm or challenge the framework's output — open an Issue on this repository.

Results that don't match expected physical behavior are as valuable as those that do.

---

## License

CC0-1.0 — Public domain. Use freely.

---

## QCore Labs

Framework developed by Richard Jackson.
DOI: 10.5281/zenodo.19558017
