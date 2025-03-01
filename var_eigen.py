import numpy as np
import matplotlib.pyplot as plt

# Load eigenvalues from GROMACS output (two-column format)
eigenvalues = []
with open('eigenval.xvg', 'r') as f:
    for line in f:
        if line.startswith(('#', '@')):  # Skip header lines
            continue
        parts = line.strip().split()
        if len(parts) >= 2:
            eigenvalues.append(float(parts[1]))  # Second column contains eigenvalues

# Convert to numpy array and calculate variance proportions
eigenvalues = np.array(eigenvalues)
total_variance = np.sum(eigenvalues)
proportion_var = (eigenvalues / total_variance) * 100  # Convert to percentage
ranks = np.arange(1, len(eigenvalues) + 1)  # Eigenvalue ranks (x-axis)

# Create the plot
plt.figure(figsize=(10, 6), dpi=300)
plt.plot(ranks, proportion_var, 'bo-', markersize=5, linewidth=1.5, 
         markerfacecolor='white', markeredgewidth=1.5, label='Proportion of Variance')

# Formatting
plt.xlabel('Eigenvalue Rank', fontsize=12, fontweight='bold')
plt.ylabel('Proportion of Variance (%)', fontsize=12, fontweight='bold')
plt.title('Variance Distribution by Eigenvalue Rank', fontsize=14, pad=15)
plt.grid(True, alpha=0.3, linestyle='--')

# Focus on relevant range (first 20 ranks typically contain most variance)
plt.xlim(0.5, 20.5)
plt.ylim(0, proportion_var[0] + 5)  # Auto-scale y-axis based on first value

# Add text annotation for first few components
for i, (rank, var) in enumerate(zip(ranks[:5], proportion_var[:5])):
    plt.text(rank + 0.3, var - 2, f'PC{rank}\n{var:.1f}%', 
             ha='left', va='top', fontsize=9)

plt.legend()
plt.tight_layout()

# Save in both formats
plt.savefig('variance_vs_rank.png', bbox_inches='tight', dpi=300)  # Original PNG
plt.savefig('variance_vs_rank.svg', format='svg', bbox_inches='tight')  # New SVG version

plt.show()
