# linreg-gd.py
#
# Standalone Python/Spark program to perform linear regression.
# Performs linear regression by computing the summation form of the
# closed form expression for the ordinary least squares estimate of beta.
# 
# TODO: Write this.
# 
# Takes the yx file as input, where on each line y is the first element 
# and the remaining elements constitute the x.
#
# Usage: spark-submit linreg.py <inputdatafile>
# Example usage: spark-submit linreg.py yxlin.csv
#
#

'''
Name - Satish Kumar
Email ID - skumar34@uncc.edu 

'''


import sys
import numpy as np

from pyspark import SparkContext

# Function to get the Matrix Y
def Get_Y(val):
    return [val[0]]

 
# Function to get the Matrix X
def Get_X(val):
    val[0]=1.0
    return [val]


if __name__ == "__main__":
	
    if len(sys.argv) !=4:
        print >> sys.stderr, "Usage: linreg <datafile> <step size> <iterations>"
        exit(-1)    

    sc = SparkContext(appName="LinearRegression")
    
    # Read the input file
    inputData = sc.textFile(sys.argv[1])
    inputLines = inputData.map(lambda eachLine: eachLine.split(','))
    firstline = inputLines.first()
    length = len(firstline)

    Y = np.asmatrix(inputLines.map(lambda line: ('Y_Val', Get_Y(line))).reduceByKey(lambda x1,x2: x1+x2).map(lambda line:line[1]).collect()[0]).astype(float).T
    X = np.asmatrix(inputLines.map(lambda line: ('X_Val', Get_X(line))).reduceByKey(lambda x1,x2: x1+x2).map(lambda line:line[1]).collect()[0]).astype(float)
    
    ###### Gradient Decent APPROACH ######
    num_of_itr= int(sys.argv[3])
    alpha_val = float(sys.argv[2])
    
    ## Initialize beta
    betaInit = [[[0.001]] * 1 for x in range(length)]

    # converting beta to matrix
    Initial_beta_matrix = []
    for value in betaInit:
        Initial_beta_matrix.append(value[0][0])
    n = 0

    while(n < num_of_itr):
        if n == 0:
            last_itr_beta = Initial_beta_matrix
              
        beta_val = np.matrix(last_itr_beta).T
        X_beta = np.dot(X,np.matrix(beta_val))
        Y_sub_X_beta = np.subtract(Y, X_beta)

        first_factor = np.dot(X.T, Y_sub_X_beta)
        second_factor = np.multiply(alpha_val , first_factor)
      
        new_beta_val = np.add(beta_val, second_factor)
        
        curr_itr_beta = []
        for value in new_beta_val.tolist():
            curr_itr_beta.append(round(value[0], 4))
        
        print "beta value after iternation number : " , str(n+1)
        for coeff in curr_itr_beta:      
            print coeff

        # For autoconvergence, break the loop once beta converges
        if (cmp(last_itr_beta, curr_itr_beta) == 0):
		print "beta vale converged in iteration number : ", str(n+1)
		print "Converged beta value are : "
		for coeff in curr_itr_beta:      
			print coeff
                break
        
        last_itr_beta = curr_itr_beta
        n = n + 1
    
    sc.stop()

