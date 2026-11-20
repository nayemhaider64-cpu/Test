import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 1. Setup the figure and axis
fig, ax = plt.subplots()
# Set fixed limits so the plot doesn't bounce around as the ball moves
ax.set_xlim(-5, 60)
ax.set_ylim(-5, 40)
ax.set_aspect('equal') # Keeps the ball from looking like an oval
ax.grid(True)

# Create an initial empty point for the ball (red circle)
ball, = ax.plot([], [], 'ro', ms=8)

# 2. Define Physics Parameters
V = 25              # Initial velocity (m/s)
g = 9.81            # Gravity (m/s^2)
theta_deg = 45      # Launch angle in DEGREES
theta = np.radians(theta_deg) # Convert to radians for numpy

# 3. Calculate Components and Time
# Physics correction: Vx uses cos(theta), Vy uses sin(theta)
Vx = V * np.cos(theta)
Vy = V * np.sin(theta)

# Total time of flight until it hits the ground (y=0)
t_max = (2 * Vy) / g

# Generate time steps (Note the correct spelling: np.linspace)
t = np.linspace(0, t_max, 100)

# Calculate all X and Y positions over time
x_vals = Vx * t
y_vals = Vy * t - 0.5 * g * t**2

# 4. The Animation Functions
def init():
    """Draws the initial empty frame."""
    ball.set_data([], [])
    return ball,

def animate(i):
    """Updates the ball position for frame 'i'."""
    # Index into our pre-calculated arrays using the current frame number
    ball.set_data([x_vals[i]], [y_vals[i]])
    return ball,

# 5. Run the Animation
# We match the number of frames to the number of time steps (100)
ani = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=len(t),
    interval=20,
    blit=True
)

plt.show()

