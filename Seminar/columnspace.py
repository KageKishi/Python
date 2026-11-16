import numpy as np
import matplotlib.pyplot as plt

A = np.array([[1, 2, 1],
              [2, 4, 1],
              [3, 5, 2]], dtype=float)
v1, v2, v3 = A.T                         # columns of A
b = np.array([3., 6., 7.])


def in_column_space(A, b):
    return np.linalg.matrix_rank(np.column_stack([A, b])) == np.linalg.matrix_rank(A)

print("A =\n", A)
print("rank =", np.linalg.matrix_rank(A))
print("Is b in Col(A)?", in_column_space(A, b))

x = np.array([-1, 2, 0])              # solution from the slide
print("A @ [-1, 2, 0] =", A @ x, "-> equals b:", np.allclose(A @ x, b))
print("2*v2 - v1      =", 2 * v2 - v1)
print("np.linalg.solve =", np.linalg.solve(A, b))
print("det(A) = %.1f -> Col(A) is all of R^3, so every b is solvable." % np.linalg.det(A))

fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(projection="3d")
O = np.zeros(3)

for vec, col, name in [(v1, "tab:blue", "v1"), (v2, "tab:orange", "v2"), (v3, "tab:purple", "v3")]:
    ax.quiver(*O, *vec, color=col, arrow_length_ratio=0.08)
    ax.text(*vec, " " + name, color=col)
ax.quiver(*O, *b, color="tab:red", linewidth=2.5, arrow_length_ratio=0.08)
ax.text(*b, " b = 2v2 - v1", color="tab:red")
ax.plot(*np.column_stack([O, -v1, -v1 + 2 * v2]), "k--", lw=1, label="path: -v1 then +2·v2")
ax.set(xlabel="x", ylabel="y", zlabel="z", title="Column space: b = 2v2 − v1")
ax.legend()
ax.view_init(elev=23, azim=-89)
plt.tight_layout()
plt.savefig("column_space.png", dpi=150)
plt.show()