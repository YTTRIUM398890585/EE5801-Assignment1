import math
import numpy as np
import matplotlib.pyplot as plt


def ferrite_bead_impedance(L, C, R, Rs, f):
    """
    returns the impedance of a ferrite bead model at a given frequency

                   |-----[L]-----|
    O-----[Rs]-----|-----[C]-----|-----O
                   |-----[R]-----|

    Args:
        L (float): inductance (H)
        C (float): capacitance (F)
        R (float): resistance (Ohm)
        Rs (float): series resistance (Ohm)
        f (float): frequency (Hz)
    """

    w = 2 * math.pi * f
    re = Rs + (1/R)/((1/R)**2 + (w*C - 1/(w*L))**2)
    im = (w*C - 1/(w*L))/((1/R)**2 + (w*C - 1/(w*L))**2)
    return math.sqrt(re**2 + im**2)


def find_C(csv_file, Cmin, Cmax, Cstep):
    """
    takes in csv and returns the capacitance value of the ferrite bead model
    """

    # Load experimental data
    # two columns [frequency in MHz, impedance in Ohm]
    experimental_data = np.loadtxt(
        csv_file, delimiter=',', dtype=str, skiprows=1)
    frequency_MHz_exp = experimental_data[:, 0]
    impedance_Ohm_exp = experimental_data[:, 1]

    # Convert to float
    frequency_MHz_exp = frequency_MHz_exp.astype(float)
    impedance_Ohm_exp = impedance_Ohm_exp.astype(float)

    # Loop through capacitance values and find the smallest MSE
    min_MSE = float('inf')
    best_C = 0

    for C in np.arange(Cmin, Cmax, Cstep):
        # Calculate impedance for each frequency
        impedance_Ohm_calc = []
        for f in frequency_MHz_exp:
            impedance_Ohm_calc.append(ferrite_bead_impedance(
                1.208e-6, C, 1.082e3, 300e-3, f*1e6))

        # Calculate MSE
        MSE = np.square(np.subtract(
            impedance_Ohm_exp, impedance_Ohm_calc)).mean()
        # print('C:', C, 'MSE:', MSE)
        if MSE < min_MSE:
            min_MSE = MSE
            best_C = C

    # Calculate impedance for best C
    impedance_Ohm_calc = []
    for f in frequency_MHz_exp:
        impedance_Ohm_calc.append(ferrite_bead_impedance(
            1.208e-6, best_C, 1.082e3, 300e-3, f*1e6))

    # Plot calculated data and experimental data on the same graph
    plot_str = 'Calculated Best C: ' + "{:.4f}".format(best_C * 1e12) + ' pF'

    plt.plot(frequency_MHz_exp, impedance_Ohm_exp, label='Experimental')
    plt.plot(frequency_MHz_exp, impedance_Ohm_calc, label=plot_str)
    plt.xscale('log')
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Impedance (Ohm)')
    plt.title('Impedance vs Frequency Experimental vs Calculated')
    plt.legend()
    plt.grid(True, which="both")
    plt.savefig('Ferrite_Bead.png')
    plt.show()

    return best_C, min_MSE


best_C, min_MSE = find_C('EE5801_FB_Extracted.csv', 1e-12, 2e-12, 1e-16)

print('Best C:', best_C)
print('MSE:', min_MSE)
