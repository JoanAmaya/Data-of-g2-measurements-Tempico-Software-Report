import glob
import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the path to the files
path = 'C:\\Users\\soyyo\\Documents\\TempicoSoftwareData\\measurementsData8'

# Retrieve all text files from the specified folder
txt_files = glob.glob(os.path.join(path, '*.txt'))
value = 2  # Index of the file to be used
new_files = [txt_files[value]]

##############################
######## Load Files ##########
##############################
def loadFiles(txt_files):
    parameters = []  # To store experiment parameters
    tau = []         # To store tau values
    g2Values = []    # To store g2 values

    # Loop through each file and extract data
    for file in txt_files:
        with open(file, 'r') as g2measure:
            txtLines = g2measure.readlines()
            
            # Extract parameters from specific lines
            parameter1 = txtLines[2].split(':')[1].replace('\n', '').replace(' ', '')
            parameter2 = txtLines[5].split(':')[1].replace('\n', '').replace(' ', '')
            parameters.append(parameter1)
            parameters.append(parameter2)
            
            # Extract tau and g2 values from the remaining lines
            for j in range(7, len(txtLines)):
                currentValue = txtLines[j]
                valuesReplaced = currentValue.replace('\n', '')
                valuesSplit = valuesReplaced.split('\t')
                tau.append(float(valuesSplit[0]))
                g2Values.append(float(valuesSplit[1]))
    
    return tau, g2Values, parameters

# Load data from files
x_data, y_data, parameters = loadFiles(new_files)
print(parameters)

##############################
####### Curve Fitting ########
##############################

def exponential(x, a, b, c):
    """Exponential function for curve fitting."""
    return a * np.exp(b * x) + c

def gaussian(x, a, x0, sigma):
    """Gaussian function for curve fitting."""
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

def lorentzian(x, x0, a, gamma):
    """Lorentzian function for curve fitting."""
    return a * gamma**2 / (gamma**2 + (x - x0)**2)

# Fit Gaussian curve to the data
popt_gaussian, pcov_gaussian = curve_fit(gaussian, x_data, y_data, p0=[1, 0, 1])
print("Optimized Gaussian parameters:", popt_gaussian)

# Fit Lorentzian curve to the data
popt_lorentzian, pcov_lorentzian = curve_fit(lorentzian, x_data, y_data, p0=[0, 1, 1])
print("Optimized Lorentzian parameters:", popt_lorentzian)

# Create subplots for Gaussian and Lorentzian fittings
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle(r"Parameters $\frac{N_1}{T_1}$: " + str(parameters[0]) + r" , $\frac{N_2}{T_2}$:" + str(parameters[1]))

# Plot for Gaussian fitting
axs[0].scatter(x_data, y_data, s=1, label='Data')
axs[0].plot(x_data, gaussian(x_data, *popt_gaussian), label=f'Gaussian fitting\na={popt_gaussian[0]:.3f}, x0={popt_gaussian[1]:.3f}, sigma={popt_gaussian[2]:.3f}', color='red')
axs[0].legend()
axs[0].set_title('Gaussian fitting')
axs[0].set_xlabel(r'$\tau$ (ms)')
axs[0].set_ylabel(r'$g^{(2)}$ Values')

# Plot for Lorentzian fitting
axs[1].scatter(x_data, y_data, s=1, label='Data')
axs[1].plot(x_data, lorentzian(x_data, *popt_lorentzian), label=f'Lorentzian fitting\nx0={popt_lorentzian[0]:.3f}, a={popt_lorentzian[1]:.3f}, gamma={popt_lorentzian[2]:.3f}', color='red')
axs[1].legend()
axs[1].set_title('Lorentzian fitting')
axs[1].set_xlabel(r'$\tau$ (ms)')
axs[1].set_ylabel(r'$g^{(2)}$ Values')

plt.tight_layout()
plt.savefig(path + "\\Measurement" + str(value + 1) + ".png")
plt.show()
