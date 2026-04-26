import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def run_assignment(roll_number, csv_path):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False, encoding='latin1')
    
    if 'no2' not in df.columns:
        df.columns = [c.lower() for c in df.columns]
    
    x = df['no2'].dropna().values
    
    ar = 0.5 * (roll_number % 7)
    br = 0.3 * ((roll_number % 5) + 1)
    
    print(f"Parameters for Roll No {roll_number}: ar={ar:.3f}, br={br:.3f}")
    
    z = x + ar * np.sin(br * x)
    
    counts, bin_edges = np.histogram(z, bins=100, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    def pdf_model(z_val, c, lmbda, mu):
        return c * np.exp(-lmbda * (z_val - mu)**2)

    initial_guess = [max(counts), 1.0 / (2 * np.var(z)), np.mean(z)]
    
    try:
        params, _ = curve_fit(pdf_model, bin_centers, counts, p0=initial_guess)
        c_learned, lambda_learned, mu_learned = params
        
        print("\n--- Learned Parameters ---")
        print(f"c      : {c_learned:.6f}")
        print(f"lambda : {lambda_learned:.6f}")
        print(f"mu     : {mu_learned:.6f}")
        print("--------------------------")
        
        plt.figure(figsize=(10, 6))
        plt.hist(z, bins=100, density=True, alpha=0.6, color='skyblue', label='Transformed Data (z)')
        z_range = np.linspace(min(z), max(z), 500)
        plt.plot(z_range, pdf_model(z_range, *params), 'r-', lw=2, label='Learned PDF')
        plt.title(f"PDF Estimation for Roll Number: {roll_number}")
        plt.xlabel("z")
        plt.ylabel("Probability Density")
        plt.legend()
        plt.show()
        
    except Exception as e:
        print(f"Error in parameter estimation: {e}")

if __name__ == "__main__":

    my_roll_number = int(input("Enter your University Roll Number: "))
    path_to_csv = "india-air-quality-data.csv" 
    
    run_assignment(my_roll_number, path_to_csv)
