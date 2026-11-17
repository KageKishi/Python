import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

# 1. Load your image
img = Image.open("image.png").convert("L")
img = img.resize((600, 600))

pixels = np.array(img, dtype=float) / 255

# 2. Camera matrix
A = sp.Matrix([
    [1, 0, 0],
    [0, 1, 0]
])

# 3. Find nullspace and column space
for i in A.nullspace():
    print("Nullspace vector:", i)
for i in A.columnspace():
    print("Column space vector:", i)
print("Rank:", A.rank())
print("Nullity:", len(A.nullspace()))

# 4. Create 3D coordinates for image pixels
x = np.arange(600)
y = np.arange(600)
X, Y = np.meshgrid(x, y)

# Use brightness as the height of the 3D surface

Z = np.zeros_like(pixels)

fig = plt.figure(figsize=(12, 6))
fig.subplots_adjust(bottom=0.2)

ax1 = fig.add_subplot(121, projection="3d")
ax2 = fig.add_subplot(122)

def draw(depth):
    ax1.clear()
    ax2.clear()

    # Change the depth of the image
    current_Z = Z + depth

    # Display image as a 3D surface
    ax1.plot_surface(
        X, Y, current_Z,
        facecolors=plt.cm.gray(pixels),
        rstride=2, cstride=2
    )
    ax1.invert_yaxis()
    ax1.set_title("Image in 3D")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("Depth")
    # Project image onto 2D camera plane
    ax2.imshow(pixels, cmap="gray")
    ax2.set_title("2D Projection")
    ax2.axis("off")

    fig.canvas.draw_idle()

draw(0)

# 5. Depth slider
slider_ax = fig.add_axes([0.2, 0.07, 0.6, 0.04])

slider = Slider(
    slider_ax,
    "Depth",
    0,
    20,
    valinit=0
)

slider.on_changed(draw)

plt.show()