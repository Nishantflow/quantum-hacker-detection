"""
============================================================
  Quantum Cryptography-Based Hacker Detection System
  Using the No-Cloning Theorem (BB84 Protocol Simulation)
============================================================
Author  : CSE Engineering Project
Platform: Qiskit 2.x + NumPy
Concept : BB84 QKD + No-Cloning Theorem + QBER-Based Detection

BB84 Protocol Flow:
  Alice → [Quantum Channel] → Bob
               ↑
           (Eve lurks here)

Steps:
  1. Alice encodes random bits in random bases → qubits
  2. Qubits travel through quantum channel
  3. (Optional) Eve intercepts, measures, re-sends
  4. Bob measures in random bases
  5. Alice & Bob SIFT key (keep only matching-basis bits)
  6. They SACRIFICE a subset of sifted bits to compute QBER
  7. If QBER > 15% → hacker detected → abort
     If QBER ≤ 15% → channel is clean → use remaining bits as key
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# ─────────────────────────────────────────────────────────────
#  GLOBAL CONFIGURATION
# ─────────────────────────────────────────────────────────────
NUM_QUBITS      = 100    # Total qubits sent (more = more reliable QBER)
SACRIFICE_FRAC  = 0.50   # Fraction of sifted key used for QBER check
QBER_THRESHOLD  = 0.15   # 15% error rate → hacker detected
SIMULATOR       = AerSimulator()

print("=" * 62)
print("  Quantum Cryptography-Based Hacker Detection System")
print("  Demonstrating the No-Cloning Theorem via BB84 Protocol")
print("=" * 62)
print(f"  Config: {NUM_QUBITS} qubits | sacrifice={int(SACRIFICE_FRAC*100)}% | threshold={int(QBER_THRESHOLD*100)}%")


# ─────────────────────────────────────────────────────────────
#  MODULE 1 — ALICE'S QUBIT ENCODING
# ─────────────────────────────────────────────────────────────
def alice_encode(num_qubits: int):
    """
    Alice randomly picks a bit (0/1) and a basis (+/x) for each qubit.

    BB84 Encoding:
      Basis '+' (Rectilinear): bit-0 → |0⟩,  bit-1 → |1⟩
      Basis 'x' (Diagonal)  : bit-0 → |+⟩,  bit-1 → |−⟩
        where |+⟩ = H|0⟩  and  |−⟩ = H|1⟩  (Hadamard gate)

    These four states are the BB84 quantum states.
    """
    bits  = np.random.randint(0, 2, num_qubits)
    bases = np.random.choice(['+', 'x'], num_qubits)

    circuits = []
    for i in range(num_qubits):
        qc = QuantumCircuit(1, 1)   # 1 qubit, 1 classical bit

        # Encode the classical bit into quantum state
        if bits[i] == 1:
            qc.x(0)          # |0⟩ → |1⟩  (Pauli-X / NOT gate)

        # Rotate to diagonal basis if needed
        if bases[i] == 'x':
            qc.h(0)          # |0⟩ → |+⟩  or  |1⟩ → |−⟩  (Hadamard gate)

        circuits.append(qc)

    return bits, bases, circuits


# ─────────────────────────────────────────────────────────────
#  MODULE 2 — EVE'S INTERCEPTION (The No-Cloning Attack)
# ─────────────────────────────────────────────────────────────
def eve_intercept(circuits: list):
    """
    Eve tries to steal information by measuring each qubit.

    ★ THE NO-CLONING THEOREM ★
      Proven by Wootters & Zurek (1982):
      "It is impossible to create an identical copy of an
       arbitrary unknown quantum state."

      Eve CANNOT copy the qubit and measure the copy later.
      She MUST measure the original — which:
        (a) collapses the superposition (destroys |+⟩ or |−⟩)
        (b) forces Eve to guess a basis (50% chance of being wrong)
        (c) when Eve guesses wrong, she re-sends the WRONG state
        (d) Bob gets a disturbed qubit → error rate ≈ 25%

    This 25% QBER is the quantum fingerprint of eavesdropping.
    """
    print("\n  ⚠  [EVE] Intercepting all qubits...")
    print("           No-Cloning Theorem: Eve cannot copy — must measure!")
    print("           Wrong-basis measurements collapse superpositions.")

    eve_bases = np.random.choice(['+', 'x'], len(circuits))
    disturbed_circuits = []

    for i, qc in enumerate(circuits):
        # Eve measures in her randomly guessed basis
        eve_qc = qc.copy()
        if eve_bases[i] == 'x':
            eve_qc.h(0)      # rotate to diagonal basis before measuring
        eve_qc.measure(0, 0)

        job    = SIMULATOR.run(eve_qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        eve_bit = int(list(counts.keys())[0])

        # Eve re-encodes what SHE measured and forwards it
        # (NOT the original state when her basis was wrong)
        new_qc = QuantumCircuit(1, 1)
        if eve_bit == 1:
            new_qc.x(0)
        if eve_bases[i] == 'x':
            new_qc.h(0)

        disturbed_circuits.append(new_qc)

    return disturbed_circuits, eve_bases


# ─────────────────────────────────────────────────────────────
#  MODULE 3 — QUANTUM CHANNEL (Alice → Bob)
# ─────────────────────────────────────────────────────────────
def quantum_channel(circuits: list, with_eve: bool):
    """
    Simulates qubit transmission over the quantum channel.
    If with_eve=True, Eve is active and disturbs the qubits.
    """
    if with_eve:
        print("\n[CHANNEL] COMPROMISED — Eve is intercepting qubits!")
        received, eve_bases = eve_intercept(circuits)
        return received, eve_bases
    else:
        print("\n[CHANNEL] SECURE — Qubits transmitted without disturbance.")
        return circuits, None


# ─────────────────────────────────────────────────────────────
#  MODULE 4 — BOB'S MEASUREMENT
# ─────────────────────────────────────────────────────────────
def bob_measure(circuits: list, num_qubits: int):
    """
    Bob randomly picks a basis for each received qubit and measures.
    Same basis as Alice → correct bit.
    Different basis → random result (discarded during sifting).
    """
    bob_bases = np.random.choice(['+', 'x'], num_qubits)
    bob_bits  = []

    for i, qc in enumerate(circuits):
        meas_qc = qc.copy()
        if bob_bases[i] == 'x':
            meas_qc.h(0)     # rotate to diagonal basis before measuring
        meas_qc.measure(0, 0)

        job    = SIMULATOR.run(meas_qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        bob_bits.append(int(list(counts.keys())[0]))

    return bob_bases, np.array(bob_bits)


# ─────────────────────────────────────────────────────────────
#  MODULE 5 — BASIS SIFTING (Classical Public Channel)
# ─────────────────────────────────────────────────────────────
def sift_key(alice_bases, bob_bases, alice_bits, bob_bits):
    """
    Alice and Bob publicly announce their BASIS choices (not the bits!).
    They keep only positions where both used the SAME basis.
    These positions form the 'sifted key' — roughly 50% of qubits.

    Why this works:
      Same basis   → Bob's measurement deterministically gives Alice's bit.
      Diff. basis  → Bob's result is random (uninformative → discard).
    """
    matching     = alice_bases == bob_bases
    sifted_alice = alice_bits[matching]
    sifted_bob   = bob_bits[matching]
    return sifted_alice, sifted_bob, matching


# ─────────────────────────────────────────────────────────────
#  MODULE 6 — QBER CALCULATION
# ─────────────────────────────────────────────────────────────
def calculate_qber(sifted_alice: np.ndarray, sifted_bob: np.ndarray,
                   sacrifice_frac: float = SACRIFICE_FRAC):
    """
    Alice & Bob publicly compare a random SACRIFICE subset of sifted bits.
    These bits are used ONLY for QBER estimation, then discarded.

    QBER = mismatched_bits / total_sacrifice_bits

    Expected QBER:
      No Eve  → QBER ≈ 0%   (no disturbance in noiseless simulation)
      Eve     → QBER ≈ 25%  (Eve wrong 50% → disturbs 50% of those)

    Threshold 15% sits safely between 0% and 25%.
    """
    n = len(sifted_alice)
    if n == 0:
        return 0.0, 0, np.array([]), np.array([])

    sacrifice_size = max(1, int(n * sacrifice_frac))
    indices = np.random.choice(n, sacrifice_size, replace=False)
    mask    = np.zeros(n, dtype=bool)
    mask[indices] = True

    sacrifice_alice = sifted_alice[mask]
    sacrifice_bob   = sifted_bob[mask]
    errors = np.sum(sacrifice_alice != sacrifice_bob)
    qber   = errors / sacrifice_size

    # Remaining bits = raw secret key
    remaining_alice = sifted_alice[~mask]
    remaining_bob   = sifted_bob[~mask]

    return qber, sacrifice_size, remaining_alice, remaining_bob


# ─────────────────────────────────────────────────────────────
#  MODULE 7 — HACKER DETECTION DECISION
# ─────────────────────────────────────────────────────────────
def detect_hacker(qber: float, threshold: float = QBER_THRESHOLD):
    """
    Binary decision: QBER > threshold → hacker detected.
    Triggers key exchange abort and channel re-establishment.
    """
    return qber > threshold


# ─────────────────────────────────────────────────────────────
#  MODULE 8 — FULL SCENARIO RUNNER
# ─────────────────────────────────────────────────────────────
def run_simulation(scenario_label: str, with_eve: bool):
    """
    Orchestrates the complete BB84 simulation for one scenario.
    Prints step-by-step logs and returns QBER + detection result.
    """
    print("\n\n" + "━" * 62)
    print(f"  SCENARIO : {scenario_label}")
    print("━" * 62)

    # STEP 1 — Alice encodes
    print(f"\n[STEP 1] Alice encodes {NUM_QUBITS} classical bits into qubits...")
    alice_bits, alice_bases, circuits = alice_encode(NUM_QUBITS)
    preview = 20
    print(f"  Alice bits  (first {preview}): {alice_bits[:preview]}")
    print(f"  Alice bases (first {preview}): {list(alice_bases[:preview])}")

    # STEP 2 — Quantum channel
    print(f"\n[STEP 2] Transmitting qubits through quantum channel...")
    received, eve_bases = quantum_channel(circuits, with_eve)
    if eve_bases is not None:
        print(f"  Eve bases   (first {preview}): {list(eve_bases[:preview])}")

    # STEP 3 — Bob measures
    print(f"\n[STEP 3] Bob measures received qubits in random bases...")
    bob_bases, bob_bits = bob_measure(received, NUM_QUBITS)
    print(f"  Bob bases (first {preview}): {list(bob_bases[:preview])}")
    print(f"  Bob bits  (first {preview}): {bob_bits[:preview]}")

    # STEP 4 — Basis sifting
    print(f"\n[STEP 4] Sifting key — comparing bases over public channel...")
    sifted_alice, sifted_bob, match_mask = sift_key(
        alice_bases, bob_bases, alice_bits, bob_bits
    )
    n_sifted = len(sifted_alice)
    print(f"  Basis matches : {n_sifted}/{NUM_QUBITS} qubits kept (~50% expected)")
    print(f"  Sifted (Alice, first 20): {sifted_alice[:20]}")
    print(f"  Sifted (Bob,   first 20): {sifted_bob[:20]}")

    # STEP 5 — QBER estimation
    print(f"\n[STEP 5] Computing QBER from sacrificed bits...")
    qber, sac_size, key_alice, key_bob = calculate_qber(sifted_alice, sifted_bob)
    errors = int(round(qber * sac_size))
    print(f"  Sacrifice bits used : {sac_size}")
    print(f"  Errors detected     : {errors}/{sac_size}")
    print(f"  QBER                : {qber*100:.2f}%")
    print(f"  Threshold           : {QBER_THRESHOLD*100:.0f}%")
    print(f"  Remaining key bits  : {len(key_alice)}")

    # STEP 6 — Detection
    hacked = detect_hacker(qber)

    print("\n" + "─" * 62)
    if hacked:
        print("  ALERT  : HACKER DETECTED!")
        print(f"      QBER = {qber*100:.2f}% EXCEEDS {QBER_THRESHOLD*100:.0f}% threshold.")
        print("      Key exchange ABORTED — channel is compromised.")
        print("      The No-Cloning Theorem exposed Eve's presence!")
    else:
        print("  SECURE : No eavesdropper detected.")
        print(f"      QBER = {qber*100:.2f}% is WITHIN safe threshold.")
        print(f"      Key exchange SUCCESSFUL — {len(key_alice)} secret bits established.")
    print("─" * 62)

    return qber, hacked


# ─────────────────────────────────────────────────────────────
#  MAIN — Run Both Scenarios and Compare
# ─────────────────────────────────────────────────────────────
def main():
    np.random.seed(7)    # Fixed seed for reproducibility

    # Scenario A: Clean channel
    qber_clean, hacked_clean = run_simulation(
        scenario_label="WITHOUT HACKER  (Clean Quantum Channel)",
        with_eve=False
    )

    # Scenario B: Eve intercepts
    qber_eve, hacked_eve = run_simulation(
        scenario_label="WITH HACKER  (Eve Intercepts Every Qubit)",
        with_eve=True
    )

    # Final comparison table
    print("\n\n" + "=" * 62)
    print("  FINAL COMPARISON SUMMARY")
    print("=" * 62)
    print(f"  {'Scenario':<33} {'QBER':>7}   Result")
    print(f"  {'─'*33} {'─'*7}   {'─'*20}")
    print(f"  {'Without Hacker':<33} {qber_clean*100:>6.2f}%   "
          f"{'HACKER DETECTED' if hacked_clean else 'SECURE — Key Exchanged'}")
    print(f"  {'With Hacker (Eve)':<33} {qber_eve*100:>6.2f}%   "
          f"{'HACKER DETECTED' if hacked_eve else 'SECURE — Key Exchanged'}")
    print("=" * 62)

    print("""
  EXPECTED BEHAVIOUR:
    Without Eve  →  QBER ~  0%  →  Key exchanged safely
    With Eve     →  QBER ~ 25%  →  Attack exposed & aborted

  WHY 25%?
    Eve guesses basis randomly (50% correct, 50% wrong).
    When wrong, her re-sent qubit has 50% chance of wrong bit.
    Net error rate = 0.5 × 0.5 = 0.25 = 25%
""")


if __name__ == "__main__":
    main()