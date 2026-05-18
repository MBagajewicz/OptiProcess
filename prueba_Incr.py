import numpy as np

def expand_candidates(candidates, space_to_add):
    """
    Expands the candidates matrix with all possible combinations
    of the lists in space_to_add.
    """
    # Create all combinations from space_to_add
    new_spaces = np.meshgrid(*space_to_add, indexing='ij')
    new_combos = np.vstack([arr.ravel() for arr in new_spaces])

    # Expand candidates with new_combos
    # Repeat each row of candidates as many times as there are combinations in new_combos
    expanded_candidates = np.repeat(candidates, new_combos.shape[1], axis=1)

    # Repeat new_combos so it aligns with candidates
    tiled_new_combos = np.tile(new_combos, candidates.shape[1])

    # Concatenate vertically
    final = np.vstack([expanded_candidates, tiled_new_combos])

    return final

# Ejemplo de uso
problem_space = [
    [0.7874, 0.8382,2],
    [0.01905, 0.0254, 0.23]
]

# Generar candidates originales
new_spaces = np.meshgrid(*problem_space, indexing='ij')
candidates = np.vstack([arr.ravel() for arr in new_spaces])

# Ejemplo de candidates recortados (solo primeras 3 combinaciones)
candidates = candidates[:, :4]

print(candidates)

print('separator----------')

# space_to_add
space_to_add = [
    [0.7874, 0.8382,2],
    [0.01905, 0.0254, 0.23],
]

# Expansión
final_matrix = expand_candidates(candidates, space_to_add)

print(final_matrix)

print(final_matrix.shape)  # (2 + 6, N_total)
