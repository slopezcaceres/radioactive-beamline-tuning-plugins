import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

# Load data from histo.dat file (assuming one column of counts)
counts = np.loadtxt("histo.dat")

# Create x-axis (bins) as index numbers if not provided
x = np.arange(len(counts))

# Plot histogram
plt.figure(figsize=(10, 6))
plt.plot(x, counts, label="Histogram", color='blue')
plt.xlabel("Channel/Bin")
plt.ylabel("Counts")
plt.title("Histogram with FWHM")
plt.grid()
plt.legend()

# Find the peak position and its height
peaks, _ = find_peaks(counts)
if len(peaks) == 0:
    print("No peaks found.")
    plt.show()
    exit()

peak_pos = peaks[np.argmax(counts[peaks])]
peak_height = counts[peak_pos]
half_max = peak_height / 2

# Interpolate histogram to find FWHM
interp = interp1d(x, counts, kind='linear')
x_fine = np.linspace(min(x), max(x), 10000)
y_fine = interp(x_fine)

# Find crossing points with half maximum
crossings = np.where(np.diff(np.sign(y_fine - half_max)))[0]
if len(crossings) >= 2:
    fwhm = x_fine[crossings[1]] - x_fine[crossings[0]]
    print(f"FWHM: {fwhm:.2f}")
    plt.axvline(x_fine[crossings[0]], color='red', linestyle='--', label="FWHM Start")
    plt.axvline(x_fine[crossings[1]], color='red', linestyle=':', label="FWHM End")
    plt.axhline(half_max, color='green', linestyle='--', label="Half Max")
else:
    print("Could not calculate FWHM.")

plt.legend()
plt.show()
