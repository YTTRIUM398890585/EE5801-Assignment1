import math

def generate_tl_circuit(L_per_m, C_per_m, trise, length, epsilon_r, fraction, file_name):
    """
    Generate LTspice circuit file for lumped transmission line model.
    
    Args:
        L_per_m (float): Inductance per meter (H/m)
        C_per_m (float): Capacitance per meter (F/m)
        trise (float): Rise time (seconds)
        length (float): Total transmission line length (meters)
        epsilon_r (float): Relative permittivity (the real part)
        fraction (int): Lambda fraction for segment length (e.g., 20 for λ/20)
        file_name (str): Name of the output file (without extension)
    """
    # Calculate maximum frequency and wavelength
    fmax = 0.35 / trise
    c = 3e8  # Speed of light (m/s)
    velocity = c / math.sqrt(epsilon_r)
    wavelength = velocity / fmax
    
    # Calculate segment length and number of segments
    if fraction == 1:
        unit_length = length
        num_segments = 1
    else:
        unit_length = wavelength / fraction
        num_segments = max(1, round(length / unit_length))
    
    # Calculate per-segment values
    L_segment = L_per_m * unit_length
    C_segment = C_per_m * unit_length
    
    # Generate circuit file
    with open(file_name + ".cir", "w") as f:
        # Write header
        f.write(f"* Lumped Transmission Line Model\n")
        f.write(f"* Length: {length}m, Segments: {num_segments}\n")
        f.write(f"* L/segment: {L_segment:.3e}H, C/segment: {C_segment:.3e}F\n")
        f.write("\n")
        
        # Set param for L and C
        f.write(".param L_segment=" + str(L_segment) + "\n")
        f.write(".param C_segment=" + str(C_segment) + "\n")
        f.write("\n")
        
        # Include segment subcircuit
        f.write(".include Segment.sub\n")
        f.write("\n")
        
        # Write components
        f.write("* Instantiation " + str(num_segments) + " segments\n")    
        for i in range(num_segments):
            if i == 0 and i == num_segments-1:
                f.write(f"X{i} Vin Vout Segment\n")
            elif i == 0:
                f.write(f"X{i} Vin N{i+1} Segment\n")
            elif i == num_segments-1:
                f.write(f"X{i} N{i} Vout Segment\n")
            else:
                f.write(f"X{i} N{i} N{i+1} Segment\n")
        f.write("\n")
                
        # Add source and load
        f.write("* Source and load\n")
        f.write(f"V1 Vsource 0 PULSE(0 10 0 {trise:.1e} {trise:.1e} 5n)\n")
        f.write(f"Rsource Vsource Vin 50\n")
        f.write(f"Rload Vout 0 121.3\n")
        f.write("\n")
        
        # Simulation command
        f.write("* Simulation command\n")
        f.write(".tran 20n\n")
        f.write(".end\n")
        
# ================================
# Main
# ================================
L_PER_M = 6.2672e-7
C_PER_M = 4.2609e-11

# Q2.2 ===========================
# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-10,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=1,
#     file_name="TL_One_Segment"
# )

# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-10,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=4,
#     file_name="TL_lambda_over_4"
# )

# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-10,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=10,
#     file_name="TL_lambda_over_10"
# )

# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-10,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=15,
#     file_name="TL_lambda_over_15"
# )

# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-10,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=20,
#     file_name="TL_lambda_over_20"
# )

# Q2.3 ===========================
# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-10,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=15,
#     file_name="TL_0-5ns"
# )

# # edit the simulation time by hand after generating the circuit file
# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-4,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=15,
#     file_name="TL_0-5ms"
# )

# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-13,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=15,
#     file_name="TL_0-5ps"
# )

# Q2.4 ===========================
# use this one but manually change the load
# generate_tl_circuit(
#     L_per_m=L_PER_M,
#     C_per_m=C_PER_M,
#     trise=5e-10,
#     length=0.6925,
#     epsilon_r=2.4,
#     fraction=15,
#     file_name="TL_lambda_over_15"
# )