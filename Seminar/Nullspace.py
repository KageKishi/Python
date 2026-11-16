import numpy as np
import matplotlib.pyplot as plt

def null_space(A, tol=1e-10):
    _, s, Vt = np.linalg.svd(A)
    rank = int(np.sum(s > tol))
    return Vt[rank:].T# columns span N(A)

A = np.array([[1, 2, 1],
              [2, 3, 1],
              [3, 4, 1]], dtype=float)

ns = null_space(A)
direction = ns[:, 0] / ns[0, 0]          
print("A =\n", A)
print("rank =", np.linalg.matrix_rank(A), "-> dim N(A) =", ns.shape[1])
print("N(A) = Span(", direction, ")")
print("A @ direction =", A @ direction)

for t in (-3, 0.5, 10):
    print(f"A @ ({t} * n) =", A @ (t * direction))

_, _, Vt = np.linalg.svd(A)
row_basis = Vt[:2]                       # orthonormal basis of row space
s, t = np.meshgrid(np.linspace(-3, 3, 8), np.linspace(-3, 3, 8))
plane = row_basis[0][:, None, None] * s + row_basis[1][:, None, None] * t

fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(projection="3d")
ax.plot(*np.outer(direction, np.array([-3, 3])), color="tab:red", lw=3,
        label="N(A) = Span(1, −1, 1)")
ax.plot_surface(*plane, alpha=0.3, color="tab:blue")
ax.plot([], [], color="tab:blue", lw=6, alpha=0.4, label="row space/Rank(A) = 2")
ax.set(xlabel="x", ylabel="y", zlabel="z", title="Null space: all x with Ax = 0")
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig("null_space.png", dpi=150)
plt.show()