
Name - Satish Kumar
Email ID - skumar34@uncc.edu 

For Execution in cloudera VM
============================

Step 1: To do Initial Setup
	$ sudo su hdfs
	$ hadoop fs -mkdir /user/cloudera
	$ hadoop fs -chown cloudera /user/cloudera
	$ exit
	$ sudo su cloudera
	$ hadoop fs -mkdir /user/cloudera/linreg /user/cloudera/linreg/input

Step 2. Put all the input files into the new input directory
	
        $ hadoop fs -put input/* /user/cloudera/linreg/input

Step 3. Execute the source code

For input file: yxlin.csv 

spark-submit linreg.py /user/cloudera/linreg/input/yxlin.csv > yxlin.output


For input file: yxlin2.csv

spark-submit linreg.py /user/cloudera/linreg/input/yxlin2.csv > yxlin2.output


Step 4. Delete the input file to place different input file

        $ hadoop fs -rm -r /user/cloudera/linreg
		
For Execution in DSBA Cluster:-
===============================

Step 1: Copy the code file and input files into dsba-cluster
		Eg: pscp C:/Users/Satish/Desktop/input/yxlin.csv <username>@dsba-hadoop.uncc.edu:/users/<username>/.
			pscp C:/Users/Satish/Desktop/input/yxlin2.csv <username>@dsba-hadoop.uncc.edu:/users/<username>/.
			pscp C:/Users/Satish/Desktop/input/linreg.py <username>@dsba-hadoop.uncc.edu:/users/<username>/.
			pscp C:/Users/Satish/Desktop/input/linreg-gd.py <username>@dsba-hadoop.uncc.edu:/users/<username>/.
			
Step 2: Login to DSBA cluster
            ssh -X <username>@dsba-hadoop.uncc.edu
			
Step 3: Copy the input files into hadoop filesystem
		Eg: hadoop fs -put <input file> /user/<username>/
			hadoop fs -put yxlin.csv /user/<username>/
			hadoop fs -put yxlin2.csv /user/<username>/
Step 4: Execute the code using spark-submit and at the same time copy the output to some file
		Eg: spark-submit <code file> <input file> > output.out
			spark-submit linreg.py yxlin.csv > yxlin.out
			spark-submit linreg.py yxlin2.csv > yxlin2.out
Step 5: Check the output values
		Eg: cat yxlin.out
		    cat yxlin2.out

==================================================

GRADIENT DECENT APPROACH:-
=========================

Note:-
To implement this approach, I have calculated X, Y from the given input file. 
I have applied the beta formula for the Gradient Decent approach. In the command line we are passing the value of alpha and number of iterations.
For implementing the autoconvergence logic, I am comparing the two lists, one from the previous iteration and second in the current iteration.
I am rounding off the beta value upto four digits after the decimal point. Please look into the code for implementation details. Also please find the 
below steps for the program execution in cloudera VM and DSBA cluster and the corresponding results.  

For input file 1:-
-----------------
For cloudera:-
spark-submit linreg-gd.py /user/cloudera/linreg/input/yxlin.csv 0.01 100 > yxlingd.output

For DSBA Cluster:-
spark-submit linreg-gd.py yxlin.csv 0.01 100 > yxlingd.out
			
OUTPUT:-

beta vale converged in iteration number :  59
Converged beta value are : 
0.5231
2.0544

For input file 2:-
------------------
For cloudera:-
spark-submit linreg-gd.py /user/cloudera/linreg/input/yxlin2.csv 0.001 200 > yxlin2gd.output

For DSBA Cluster:-
spark-submit linreg-gd.py yxlin2.csv 0.001 100 > yxlin2gd.out

OUTPUT:-

beta vale converged in iteration number :  50
Converged beta value are : 
0.5109
1.9951


