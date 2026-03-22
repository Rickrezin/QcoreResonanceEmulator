import math

# constants
h = 6.62607015e-34   # Planck's constant (J*s)
phi = (1 + math.sqrt(5)) / 2

def resonance_energy(freq_hz):
    """Compute resonance energy using E_n = h * ω * φ^2"""
    omega = 2 * math.pi * freq_hz  # angular frequency
    return h * omega * phi**2

def classify_state(E):
    """Classify resonance energy into a QCore state"""
    # arbitrary thresholds (tunable!)
    if abs(E % phi) < 0.05:
        return "C"  # near φ harmonic
    elif abs((E/phi) % 1 - 0.5) < 0.05:
        return "O"  # offset
    elif E < 0:
        return "D"  # divergent
    elif E != 0 and abs(E) < 1e-22:
        return "N"  # neutral
    elif E > 1e-19:
        return "A"  # anomaly / unstable
    else:
        return "R"  # fallback: return

# Example usage
freq = 1e12  # 1 THz vibration
E = resonance_energy(freq)
state = classify_state(E)

print(f"Frequency {freq} Hz → Energy {E:.3e} J → State {state}")
