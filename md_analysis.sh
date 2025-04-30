#!/bin/bash

# Script to analyze Gromacs trajectory
# Author: Dr Saurabh Sharma, PhD

# --- Define Variables ---
tpr="step5_1.tpr"
xtc="step5_1.xtc"
fit_xtc="step5_1_fit.xtc"
center_xtc="step5_1_center.xtc"
index_file="index.ndx"
output_dir="analysis"
ligand_name="UNK"  # Default ligand name - CHANGE THIS IF NEEDED

# --- Print working directory ---
echo "Current working directory: $(pwd)"

# --- Create output directory if it doesn't exist ---
mkdir -p "$output_dir"

# --- Check if essential files exist ---
if [ ! -f "$tpr" ] || [ ! -f "$xtc" ] || [ ! -f "$index_file" ]; then
  echo "Error: Essential files (TPR, XTC, or index) are missing."
  exit 1
fi

# --- Trajectory Preprocessing ---
echo "Trajectory Preprocessing..."

# Recentering (Protein)
gmx trjconv -s "$tpr" -f "$xtc" -o "$output_dir/$center_xtc" -center -pbc mol -ur compact << EOF
1
0
EOF

# --- Check if center_xtc was created ---
if [ ! -f "$output_dir/$center_xtc" ]; then
    echo "Error: $center_xtc was not created in $output_dir. Check the recentering step."
    exit 1
fi

# Rotational and Translational Fitting (Backbone)
gmx trjconv -s "$tpr" -f "$output_dir/$center_xtc" -o "$output_dir/$fit_xtc" -fit rot+trans << EOF
4
0
EOF

# --- RMSD Analysis ---
echo "RMSD Analysis..."

# RMSD (Backbone)
gmx rms -s "$tpr" -f "$output_dir/$fit_xtc" -o "$output_dir/rmsd.xvg" -n "$index_file" -tu ns << EOF
4
4
EOF

# Calculate RMSD for the ligand
gmx rms -s "$tpr" -f "$output_dir/$fit_xtc" -o "$output_dir/rmsd-ligand.xvg" -n "$index_file" -tu ns << EOF
4
13
EOF

# --- RMSF Analysis ---
echo "RMSF Analysis..."

# RMSF (C-alpha) - Residue level
gmx rmsf -s "$tpr" -f "$output_dir/$fit_xtc" -o "$output_dir/rmsf.xvg" -n "$index_file" -res << EOF
3
EOF

# --- Radius of Gyration (Rg) ---
echo "Radius of Gyration..."
gmx gyrate -s "$tpr" -f "$output_dir/$fit_xtc" -o "$output_dir/gyrate.xvg" -n "$index_file" << EOF
1
EOF

# --- Solvent Accessible Surface Area (SASA) ---
echo "SASA Calculation..."
gmx sasa -s "$tpr" -f "$output_dir/$fit_xtc" -o "$output_dir/area.xvg" -n "$index_file" -tu ns << EOF
1
EOF

# --- Covariance Analysis and PCA ---
echo "Covariance Analysis and PCA..."

# Covariance Analysis (C-alpha)
gmx covar -f "$output_dir/$fit_xtc" -s "$tpr" -n "$index_file" -ascii "$output_dir/covar.dat" -v "$output_dir/eigenvect.trr" -o "$output_dir/eigenval.xvg" -xpm "$output_dir/covara.xpm" -xpma "$output_dir/dynamic_covar.xpm" -tu ns << EOF
3
3
EOF

gmx xpm2ps -f "$output_dir/covara.xpm" -o "$output_dir/covara.eps" -do "$output_dir/covar.m2p" -rainbow red
gmx xpm2ps -f "$output_dir/dynamic_covar.xpm"  -o "$output_dir/dynamic_covar.eps" -rainbow red

# Principal Component Analysis (C-alpha)
gmx principal -f "$output_dir/$fit_xtc" -s "$tpr" -n "$index_file" -a1 "$output_dir/paxis.xvg" -a2 "$output_dir/paxis2.xvg" -a3 "$output_dir/paxis3.xvg" -om "$output_dir/moi.xvg" << EOF
3
EOF

# Essential Dynamics (PCA Projection)
gmx anaeig -v "$output_dir/eigenvect.trr" -f "$output_dir/$fit_xtc" -s "$tpr" -first 1 -last 2 -proj "$output_dir/proj_eig.xvg" -2d "$output_dir/2d_proj.xvg" -n "$index_file" -tu ns << EOF
3
3
EOF

gmx sham -f "$output_dir/2d_proj.xvg" -ls "$output_dir/gibbs.xpm" -notime
gmx xpm2ps -f "$output_dir/gibbs.xpm"  -o "$output_dir/gibbs.eps" -rainbow red
gmx xpm2ps -f "$output_dir/entropy.xpm"  -o "$output_dir/entropy.eps" -rainbow red
gmx xpm2ps -f "$output_dir/enthalpy.xpm"  -o "$output_dir/enthalpy.eps" -rainbow red

# --- Clustering (Optional) ---
echo "Clustering..."
gmx cluster -f "$output_dir/$fit_xtc" -s "$tpr" -n "$index_file" -g "$output_dir/cluster.log" -cutoff 0.14 << EOF
4
EOF

echo "Analysis complete.  Output files are in the '$output_dir' directory."

exit 0
