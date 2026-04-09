#!/usr/bin/env python3
# Qcore_hybrid.py — Resonance Emulator with Law of Harmonic Resonance + Stabilizer Engine

import re, csv
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
from itertools import combinations

# =============================
# Parser (handles nested groups and multipliers)
# =============================
def parse_formula(formula: str) -> Counter:
    formula = ''.join(formula.split())  # remove spaces
    stack = [Counter()]
    i = 0
    while i < len(formula):
        if formula[i].isalpha():
            elem = formula[i]
            i += 1
            if i < len(formula) and formula[i].islower():
                elem += formula[i]
                i += 1
            count = 0
            while i < len(formula) and formula[i].isdigit():
                count = count * 10 + int(formula[i])
                i += 1
            amount = 1
            if i < len(formula) and formula[i] == '^':
                i += 1
                amount = 0
                while i < len(formula) and formula[i].isdigit():
                    amount = amount * 10 + int(formula[i])
                    i += 1
                amount = max(amount, 1)
            stack[-1][elem] += max(count, 1) * amount

        elif formula[i] in '([{':
            stack.append(Counter())
            i += 1

        elif formula[i] in ')]}':
            i += 1
            count = 0
            while i < len(formula) and formula[i].isdigit():
                count = count * 10 + int(formula[i])
                i += 1
            group = stack.pop()
            for k in group:
                stack[-1][k] += group[k] * max(count, 1)
        else:
            i += 1
    return stack[0]

# =============================
# Reaction Parser (stoichiometric coefficients + amount syntax)
# e.g. ":2 Fe2O3 + H2^3"
# =============================
def parse_reaction(expr: str) -> Counter:
    total = Counter()
    terms = re.split(r'\s*\+\s*', expr.strip())
    for term in terms:
        term = term.strip()
        if not term:
            continue
        # Check for leading stoichiometric coefficient ":N"
        m = re.match(r'^:(\d+)\s*(.*)', term)
        if m:
            coeff = int(m.group(1))
            formula = m.group(2).strip()
        else:
            coeff = 1
            formula = term
        if not formula:
            continue
        sub = parse_formula(formula)
        for elem, cnt in sub.items():
            total[elem] += cnt * coeff
    return total

# =============================
# Load CSVs and Merge
# =============================
FREQ_CSV = "resonance_phi2_results.csv"
META_CSV = "Res_csv.csv"

def load_frequencies(csv_path):
    out = {}
    if not Path(csv_path).exists(): return out
    with open(csv_path, newline='') as f:
        for row in csv.DictReader(f):
            sym = row['Symbol'].strip().capitalize()
            out[sym] = {
                'f_std': float(row.get('f_std_Hz') or 0),
                'f_phi2': float(row.get('f_phi2_Hz') or 0)
            }
    return out

def load_metadata(csv_path):
    out = {}
    if not Path(csv_path).exists(): return out
    with open(csv_path, newline='') as f:
        for row in csv.DictReader(f):
            sym = row['Symbol'].strip().capitalize()
            out[sym] = {
                'Element': row.get('Element', '').strip(),
                'Category': row.get('Category', '').strip().upper(),
                'Type': row.get('Type', '').strip().lower(),
                'Phase': row.get('Phase', '').strip().lower(),
                'AtomicRadius': row.get('AtomicRadius', ''),
                'Electronegativity': row.get('Electronegativity', ''),
                'MeltingPoint_K': row.get('MeltingPoint_K', ''),
                'BoilingPoint_K': row.get('BoilingPoint_K', ''),
                'Density_gcc': row.get('Density_gcc', '')
            }
    return out

def merge(freq, meta):
    merged = {}
    for sym in meta:
        f = freq.get(sym, {'f_std': 0, 'f_phi2': 0})
        merged[sym] = {
            **meta[sym],
            'f_std': f['f_std'],
            'f_phi2': f['f_phi2'],
            'state': meta[sym].get('Category', 'NEU').upper()
        }
    return merged

FREQS = merge(load_frequencies(FREQ_CSV), load_metadata(META_CSV))

# =============================
# Pair Compatibility Rules
# =============================
PAIR_RULES = {
    "radius_close_pm": 30,
    "en_close": 0.5,
    "en_too_far": 2.5,
    "bp_mp_gap_K": 300,
    "density_very_far": 10.0,
    "score_stabilize": 2,
    "score_destabilize": -2
}

def _f(x):
    try: return float(x)
    except: return None

def score_pair(e1, e2):
    score, reasons = 0, []
    r1, r2 = _f(e1['AtomicRadius']), _f(e2['AtomicRadius'])
    if r1 and r2:
        dr = abs(r1 - r2)
        if dr <= PAIR_RULES['radius_close_pm']:
            score += 1; reasons.append(f"Δradius={dr:.0f}pm +1")
        elif dr >= 2 * PAIR_RULES['radius_close_pm']:
            score -= 1; reasons.append(f"Δradius={dr:.0f}pm −1")

    e1en, e2en = _f(e1['Electronegativity']), _f(e2['Electronegativity'])
    if e1en and e2en:
        den = abs(e1en - e2en)
        if den <= PAIR_RULES['en_close']:
            score += 1; reasons.append(f"ΔEN={den:.2f} +1")
        elif den > PAIR_RULES['en_too_far']:
            score -= 2; reasons.append(f"ΔEN={den:.2f} −2")

    label = 'NEUTRAL'
    if score >= PAIR_RULES['score_stabilize']: label = 'STABILIZER'
    elif score <= PAIR_RULES['score_destabilize']: label = 'DESTABILIZER'
    return label, score, reasons

# =============================
# Resonance Color Reduction
# =============================
COLORS = {
    "CON": (0,255,0), "DIV": (255,0,0), "RET": (0,0,255),
    "OFF": (255,255,0), "NEU": (128,0,128), "ANOM": (0,0,0)
}

def transition(s1, s2):
    if s1 == "NEU": return s2
    if s2 == "NEU": return s1
    if "ANOM" in (s1, s2): return "ANOM"
    return "NEU"

def reduce_states(states):
    result = states[0] if states else "NEU"
    for s in states[1:]:
        result = transition(result, s)
    return result

# =============================
# GUI
# =============================
root = tk.Tk()
root.title("QCore Resonance Emulator")

frm = ttk.Frame(root, padding=10)
frm.grid(row=0, column=0)

entry = ttk.Entry(frm, width=40)
entry.grid(row=0, column=1)
ttk.Label(frm, text="Formula / Reaction:").grid(row=0, column=0)
phi2_var = tk.BooleanVar(value=True)
ttk.Checkbutton(frm, text="Use ϕ²", variable=phi2_var).grid(row=0, column=2)

final_lbl = ttk.Label(frm, text="Final State: ---")
final_lbl.grid(row=1, column=0, columnspan=3, sticky="w")

freq_box = scrolledtext.ScrolledText(frm, width=70, height=10)
freq_box.grid(row=2, column=0, columnspan=3)

dest_box = scrolledtext.ScrolledText(frm, width=70, height=10)
dest_box.grid(row=4, column=0, columnspan=3)

def evaluate():
    expr = entry.get().strip()
    try:
        counts = parse_reaction(expr)
    except Exception as e:
        messagebox.showerror("Parse error", str(e))
        return

    lines, states, symbols = [], [], []
    for sym, n in counts.items():
        sym = sym.capitalize()
        info = FREQS.get(sym)
        if not info:
            lines.append(f"{sym} x{n} → not found")
            continue
        state = info['state']
        fval = info['f_phi2'] if phi2_var.get() else info['f_std']
        lines.append(f"{sym} x{n} → {fval:.3e} Hz | State: {state}")
        states += [state]*n
        symbols += [sym]*n

    final = reduce_states(states)
    final_lbl.config(text=f"Final State: {final}")

    freq_box.delete("1.0", tk.END)
    freq_box.insert(tk.END, "\n".join(lines))

    stab, neu, dest = [], [], []
    for a, b in combinations(symbols, 2):
        e1, e2 = FREQS.get(a), FREQS.get(b)
        if not e1 or not e2: continue
        label, score, reasons = score_pair(e1, e2)
        line = f"{a}-{b}: {label} ({score}) — {'; '.join(reasons)}"
        (stab if label == 'STABILIZER' else dest if label == 'DESTABILIZER' else neu).append(line)

    dest_box.delete("1.0", tk.END)
    if stab: dest_box.insert(tk.END, "STABILIZERS:\n" + "\n".join(stab) + "\n\n")
    if neu: dest_box.insert(tk.END, "NEUTRAL:\n" + "\n".join(neu) + "\n\n")
    if dest: dest_box.insert(tk.END, "DESTABILIZERS:\n" + "\n".join(dest))

ttk.Button(frm, text="Evaluate", command=evaluate).grid(row=6, column=0, columnspan=3)
root.bind("<Return>", lambda e: evaluate())

root.mainloop()
