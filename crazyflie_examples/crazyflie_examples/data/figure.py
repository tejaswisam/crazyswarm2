import numpy as np
import matplotlib.pyplot as plt

# Define the radius and duration for one full circle
radius = 1.0
duration = 10.0
omega = 2 * np.pi / duration

# Create polynomials for x(t), y(t), z(t), yaw(t)
# x(t) = r * cos(omega * t) => coefficients for cos(omega * t)
# y(t) = r * sin(omega * t) => coefficients for sin(omega * t)
# z(t) = 0
# yaw(t) = omega * t

t_values = np.linspace(0, duration, 100)
x_values = radius * np.cos(omega * t_values)
y_values = radius * np.sin(omega * t_values)
z_values = np.zeros_like(t_values)
yaw_values = omega * t_values

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(x_values, y_values)
plt.title("Trajectory in x-y plane (Circle)")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t_values, yaw_values)
plt.title("Yaw over time")
plt.xlabel("time [s]")
plt.ylabel("yaw [rad]")
plt.grid(True)

plt.tight_layout()
plt.show()
