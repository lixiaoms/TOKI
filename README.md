TOKI

Operating systems: Windows/Linux/Unix, NO software but python3 install required.  
If running on Windows system, please run "TOKI_windows.py" rather than "TOKI.py".

Usage: 

path/to/python3 path/to/TOKI.py (Hi-C contact matrix file) options
    
    Options:
    
     -b <kbp resolution of matrix> (default=40)
     
     -o <output dir> (default=./TAD)
     
     -s <TAD mean kbp size min,max> (default=600,1000)
     
     -p <number of cores to use> (default=1)
     
     -h <to print usage>
    
The required Python packages and recommended version : Scikit-learn(>=0.21.2), Pandas(>=1.1.0), Numpy(>=1.19.0), Multiprocessing.

Demo:  

There is a GM12878 cell#11 chr19 contact matrix file in the folder '/demo'.  
It is easy to run deTOKI on the data by the command (add '-p 16' if using 16 cores):

path/to/python3 TOKI.py demo/cell_11 -o cell_11_TAD

Then the output file 'cell_11_TAD' is expected to be same with the file in '/demo'.  
The number of bins in TAD file represent the predicted TAD boundaries.  
Reference run time： ~40s (1 core) or ~7s (16 core) in Intel(R) Xeon(R) CPU E5620 @ 2.40GHz,
                     ~17s (1 core) or ~8s (4 core) in Intel(R) Core(TM) i7-9750H @ 2.60GHz.
