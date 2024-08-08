import glob
import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the path to the files
path = 'C:\\Users\\soyyo\\Documents\\TempicoSoftwareData\\StartStop1'

# Retrieve all text files from the specified folder
txt_files = glob.glob(os.path.join(path, '*.txt'))
value = 0  # Index of the file to be used
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

# Filter data to include only tau values greater than 0.4
filtered_x_data = []
filtered_y_data = []

for i in range(len(x_data)):
    # Uncomment the following line to filter only tau values greater than 0.4
    # if x_data[i] > 0.4:
        filtered_x_data.append(x_data[i])
        filtered_y_data.append(y_data[i])

# Define the exponential function for curve fitting
def exponential(x, a, b, c):
    """Exponential function for curve fitting."""
    return a * np.exp(b * x) + c

# Fit the exponential curve to the data
# Uncomment the following lines to fit the curve and print the optimized parameters
# popt_exponential, pcov_exponential = curve_fit(exponential, filtered_x_data, filtered_y_data, p0=[1, -0.1, 1])
# print("Optimized Exponential parameters:", popt_exponential)

# Plot the data and the fitted curve
plt.figure(figsize=(10, 6))
plt.title(r"Parameters $\frac{N_1}{T_1}$: " + str(parameters[0]) + r" , $\frac{N_2}{T_2}$:" + str(parameters[1]))
plt.plot(filtered_x_data, filtered_y_data, label='Data')
# Uncomment the following line to plot the exponential fit
# plt.plot(filtered_x_data, exponential(np.array(filtered_x_data), *popt_exponential), label='Exponential Fit', color='red')
plt.xlabel(r'$\tau$ (ms)')
plt.ylabel(r'$g^{(2)}$ Values')
plt.legend()
plt.savefig(path + "\\MeasurementPlot" + str(value + 1) + ".png")
plt.show()
