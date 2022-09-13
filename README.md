# Gnowee_CASMO_SIM <br />
WORK IN PROGRESS: <br />
This python framework allows Gnowee to communicate with the Studsvik Codes: CASMO-4 and SIMULATE-3. <br />
<br />
To use this framework, user shall update the run_on_cluster function on 'functions.py' for compatibility with their cluster's interface. <br />
<br />
'Obj_Func.py' shall be edited to designate user's objective function to achieve design goals. This python code initializes the function inputs and then calls the functions from 'functions.py' in order to update the mock input file with Gnowee's selected design vector. After evaluation on the cluster, this code extracts data from the CASMO-4/SIMULATE-3 output files to calculate the fitness value and report it back to Gnowee. <br />
<br />
'run_Gnowee_multi.py' is used to select which objective function will be utilized (specifically the CASMO-4 or SIMULATE-3 function from 'Obj_Func.py'). The user will then decide on the variable input list for the specific optimization function. Examples are provided in 'run_Gnowee_multi.py' for lattice arrangement optimization, cycle01 loading pattern optimization, and for axial loading optimization of fresh fuel bundles for refueling. <br />
<br />
For more information regarding Gnowee, please refer to the original code at https://github.com/SlaybaughLab/Gnowee
