"""
PCA Variance Visualization Script for GROMACS Eigenvalue Data
Author: Dr Saurabh Sharma, Department of Bioinformatics, Amity University Punjab
Caveat: Help taken by author from self-hosted AI models for some parts of the code 
License: GPL V3
Description: Creates proportion of variance vs eigenvalue rank plot from .xvg files
"""

# Import required libraries
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For plotting

# --------------------------
# DATA LOADING SECTION
# --------------------------

# Initialize empty list to store eigenvalues
eigenvalues = []

# Open and read the GROMACS eigenvalue file
with open('eigenval.xvg', 'r') as f:
    # Process each line in the file
    for line in f:
        # Skip header lines starting with # or @
        if line.startswith(('#', '@')):
            continue  # Move to next line
        
        # Split line into components (whitespace separator)
        parts = line.strip().split()
        
        # Check if line contains at least 2 columns (index + eigenvalue)
        if len(parts) >= 2:
            # Extract eigenvalue from second column and convert to float
            # GROMACS format: [index] [eigenvalue] [optional columns]
            eigenvalues.append(float(parts[1]))

# Convert list to numpy array for efficient numerical operations
eigenvalues = np.array(eigenvalues)

# --------------------------
# VARIANCE CALCULATION
# --------------------------

# Calculate total variance (sum of all eigenvalues)
total_variance = np.sum(eigenvalues)

# Calculate proportional variance for each eigenvalue (as percentage)
proportion_var = (eigenvalues / total_variance) * 100

# Create array of eigenvalue ranks (1, 2, 3,...)
ranks = np.arange(1, len(eigenvalues) + 1)

# --------------------------
# PLOTTING CONFIGURATION
# --------------------------

# Create figure with specified size and resolution
# figsize: 10" wide x 6" tall (1 inch = 2.54 cm)
# dpi: 300 dots per inch for high-resolution output
plt.figure(figsize=(10, 6), dpi=300)

# Create main plot line with formatting:
# 'b' = blue, 'o' = circle markers, '-' = solid line
# markerfacecolor: White fill for circles
# markeredgewidth: Border thickness for circles
plt.plot(ranks, proportion_var, 'bo-', 
         markersize=5,          # Size of circle markers
         linewidth=1.5,         # Line thickness
         markerfacecolor='white',  # Circle fill color
         markeredgewidth=1.5,   # Circle border thickness
         label='Proportion of Variance')

# --------------------------
# PLOT FORMATTING
# --------------------------

# Axis labels with bold font
plt.xlabel('Eigenvalue Rank', fontsize=12, fontweight='bold')
plt.ylabel('Proportion of Variance (%)', fontsize=12, fontweight='bold')

# Title with extra padding (space below title)
plt.title('Variance Distribution by Eigenvalue Rank', 
          fontsize=14, pad=15)

# Add semi-transparent grid lines
plt.grid(True, alpha=0.3, linestyle='--')

# Set axis limits:
# X-axis: Show first 20 components (0.5 padding for visual clarity)
# Y-axis: From 0% to 5% above largest variance component
plt.xlim(0.5, 20.5)
plt.ylim(0, proportion_var[0] + 5)

# --------------------------
# COMPONENT ANNOTATIONS
# --------------------------

# Add text labels for first 5 principal components
for i, (rank, var) in enumerate(zip(ranks[:5], proportion_var[:5])):
    # Position text slightly to right (rank + 0.3) and below (var - 2%) data point
    plt.text(rank + 0.3, var - 2, 
             f'PC{rank}\n{var:.1f}%',  # Text content
             ha='left',   # Horizontal alignment: left
             va='top',    # Vertical alignment: top
             fontsize=9)

# Add legend using label from plt.plot()
plt.legend()

# Adjust layout to prevent label cutoff
plt.tight_layout()

# --------------------------
# FILE EXPORT
# --------------------------

# Save as PNG (bitmap format for quick viewing)
plt.savefig('variance_vs_rank.png', 
           bbox_inches='tight',  # Remove extra whitespace
           dpi=300)              # High resolution

# Save as SVG (vector format for publications/editing)
plt.savefig('variance_vs_rank.svg', 
           format='svg', 
           bbox_inches='tight')

# Display plot in interactive window (if running in IDE)
plt.show()
