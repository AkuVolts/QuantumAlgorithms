from qiskit import QuantumCircuit
import numpy as np
from qiskit_aer import AerSimulator

# play the game
def play_game(x, y, a, b):
    if (a != b) == (x & y):
        return 1
    return 0


# classical strategy
def classical_strategy(x, y):
    return 0, 0

# quantum strategy
def quantum_strategy(x, y):
    # make a quantum circuit for each situation
    qc = QuantumCircuit(2, 2)

    # make a bell state
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # apply gates according to the input
    if x == 0:
        qc.ry(0, 0)
    else:
        qc.rx(-np.pi / 2, 0)

    if y == 0:
        qc.ry(-np.pi / 4, 1)
    else:
        qc.rx(np.pi / 4, 1)

    qc.barrier()
    qc.measure([0, 1], [0, 1])

    sampler = AerSimulator()
    result = sampler.run(qc).result()
    counts = result.get_counts(qc)
    a, b = list(counts.keys())[0][0], list(counts.keys())[0][1]

    return a, b



NUM_TRIALS = 1000
games_won_c = 0
games_won_q = 0

for i in range(NUM_TRIALS):
    # choose x and y randomly
    x = np.random.randint(0, 2)
    y = np.random.randint(0, 2)

    # choose a and b according to the strategy
    ac, bc = classical_strategy(x, y)
    aq, bq = quantum_strategy(x, y)

    # play the game
    games_won_c += play_game(x, y, ac, bc)
    games_won_q += play_game(x, y, aq, bq)

print("Fraction of games won by classical strategy: ", games_won_c / NUM_TRIALS)
print("Fraction of games won by quantum strategy: ", games_won_q / NUM_TRIALS)







