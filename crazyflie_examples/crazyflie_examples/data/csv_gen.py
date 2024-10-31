import numpy as np
import csv

def generate_circle_trajectory_csv(filename, radius, duration):
    omega = 2 * np.pi / duration
    
    # Polynomial coefficients for x(t) = r * cos(omega * t)
    # Approximating using Taylor series expansion
    px = [radius, 0, -radius * (omega ** 2) / 2, 0, radius * (omega ** 4) / 24, 0, -radius * (omega ** 6) / 720, 0]

    # Polynomial coefficients for y(t) = r * sin(omega * t)
    py = [0, radius * omega, 0, -radius * (omega ** 3) / 6, 0, radius * (omega ** 5) / 120, 0, -radius * (omega ** 7) / 5040]

    # Polynomial coefficients for z(t) = 0
    pz = [0] * 8
    
    # Polynomial coefficients for yaw(t) = omega * t
    pyaw = [0, omega] + [0] * 6

    # Create the CSV file
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header
        csvwriter.writerow(['duration'] + [f'px_{i}' for i in range(8)] +
                           [f'py_{i}' for i in range(8)] + [f'pz_{i}' for i in range(8)] +
                           [f'pyaw_{i}' for i in range(8)])
        
        # Write the polynomial data
        row = [duration] + px + py + pz + pyaw
        csvwriter.writerow(row)

# Parameters for the circular trajectory
radius = 1.0
duration = 10.0
filename = 'circle_trajectory.csv'

# Generate the CSV
generate_circle_trajectory_csv(filename, radius, duration)
print(f'CSV file "{filename}" generated successfully.')
