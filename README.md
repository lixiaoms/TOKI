TOKI
===
deTOKI is a newly developed tool for identification of chromatin topologically associating domains (TAD) in single cells.
Although we use term "TAD" here, we refer to the TAD-like domains in single cells. 
deTOKI decode TAD boundaries that keep chromatin interaction isolated with ultra-sparse Hi-C data (single-cell Hi-C) using NMF (Nonnegative Matrix Factorization).

Installation
---
Please directly clone this github repository on your computer.  
Operating systems: Linux/Unix/Windows, with python3 installed.  
Please install the dependencies: Scikit-learn(>=0.21.2), Pandas(>=1.1.0), Numpy(>=1.19.0). The recommended version is given in parentheses.

Input
---
n × n intra-chromosome contact matrix

Output
---
A list of numbers, which represent the genome location of TAD boundaries.  
For example, if resolution of input matrix is 40kbp, then output [0, 18, 33, 40, 60] means that TAD boundaries are located on 720kbp, 1320kbp, 1600kbp and 2400kbp. 


Usage 
---
`path/to/python3 path/to/TOKI.py [FILE] [OPTIONS]`

    FILE:
    
     The file location of Hi-C contact matrix.
     
    OPTIONS:
    
     -b <kbp resolution of matrix> (default=40)
     
     -o <output dir> (default=./TAD)
     
     -s <TAD mean kbp size min,max> (default=600,1000)
     
     -p <number of cores to use> (default=1)
     
     -h <to print usage>

If running on Windows system, please run "TOKI_windows.py" rather than "TOKI.py".

Demo
---
There is a GM12878 cell#11 chr19 contact matrix file in the folder '/demo'.  
It is easy to run deTOKI on this data by the following command (add '-p 16' if using 16 cores):

`path/to/python3 TOKI.py demo/cell_11 -o cell_11_TAD`

Then the output file 'cell_11_TAD' is expected to be same with the file in '/demo'.  
Reference run time： ~40s (1 core) or ~7s (16 core) in Intel(R) Xeon(R) CPU E5620 @ 2.40GHz,
                     ~17s (1 core) or ~8s (4 core) in Intel(R) Core(TM) i7-9750H @ 2.60GHz.

3D simulated single cell Hi-C
---
We also uploaded the code for generating simulated single-cell Hi-C data. Please refer to fold /simulated_Hi-C.
Basing on the model.xyz data resulted from IMP software, "3D simulated scHi-C.py" can generate simulated scHi-C and ensemble Hi-C data.
                     
Citation
---
Li, X., Zeng, G., Li, A. et al. DeTOKI identifies and characterizes the dynamics of chromatin TAD-like domains in a single cell. Genome Biol 22, 217 (2021). https://doi.org/10.1186/s13059-021-02435-7
