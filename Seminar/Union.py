import numpy as np
import matplotlib.pyplot as plt

Xaxis = lambda v: np.isclose(v[1], 0)
YAxis = lambda v: np.isclose(v[0], 0)
in_union = lambda v: Xaxis(v) or YAxis(v)

u = np.array([2.0, 0.0])      # in X
v = np.array([0.0, 2.0])      # in Y
w = u + v                     # sum

print("u in S ∪ T?  ", in_union(u))
print("v in S ∪ T?  ", in_union(v))
print("u+v in S ∪ T?", in_union(w), " -> closure under addition FAILS")
print("0 in S ∪ T?  ", in_union(np.zeros(2)), "(zero vector is fine, but that's not enough)")

fig, ax = plt.subplots(figsize=(6, 6))
L = np.array([-3, 3])
ax.plot(L, 0 * L, "tab:blue", lw=3, label="subspace S (x-axis)")
ax.plot(0 * L, L, "tab:orange", lw=3, label="subspace T (y-axis)")

for vec, col, name in [(u, "tab:blue", "u in S"),
                       (v, "tab:orange", "v in T"),
                       (w, "tab:red", "u+v not in S ∪ T")]:
    ax.annotate("", xy=vec, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=col, lw=2))
    ax.text(vec[0] + 0.1, vec[1] + 0.1, name, color=col)

ax.set(xlim=(-3, 3), ylim=(-3, 3), aspect="equal",
       title="S ∪ T is not closed under addition")
ax.axhline(0, c="gray", lw=0.5); ax.axvline(0, c="gray", lw=0.5)
ax.legend(loc="lower left")
plt.tight_layout()
plt.show()