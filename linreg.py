# linreg.py
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

# Function to find X * X_Transpose
def valueForKeyA(line):
    
    line[0]=1.0
    X_array = np.array(line).astype('float')
    X_matrix = np.asmatrix(X_array)
    X = np.asmatrix(X_array).T
    X_Xtrans = np.dot(X,X.T)

    return X_Xtrans

# Function to find X * Y
def valueForKeyB(line):
    Y = float(line[0])
    line[0] = 1.0
    X_array = np.array(line).astype('float')
    X = np.asmatrix(X_array).T
    X_Y = np.multiply(X,Y)
    
    return X_Y

if __name__ == "__main__":
  if len(sys.argv) !=2:
    print >> sys.stderr, "Usage: linreg <datafile>"
    exit(-1)

  sc = SparkContext(appName="LinearRegression")

  # Input yx file has y_i as the first element of each line 
  # and the remaining elements constitute x_i
  
  # Read the input file
  inputData = sc.textFile(sys.argv[1])
  inputLines = inputData.map(lambda eachLine: eachLine.split(','))
  
  # Calculate A as matrix for X.X_Transpose. We Calculate (X * X_Transpose) for each line and add them by using reduceBYKey
  # map(lambda line: ("KeyA",valueForKeyA(line))) --> For calculating X * X_Transpose for each line
  # reduceByKey(lambda x1,x2: np.add(x1,x2)) --> For adding all the values for KeyA
  # map(lambda line: line[1]) --> Getting the combined value for keyA
    
  A_Tranf = inputLines.map(lambda line: ("KeyA",valueForKeyA(line))).reduceByKey(lambda x1,x2: np.add(x1,x2)).map(lambda line: line[1])
  A_Act = A_Tranf.collect()[0]
  A = np.asmatrix(A_Act)

  # Calculate B as matrix for X.Y. We Calculate (X * Y) for each line and add them by using reduceBYKey
  # map(lambda line: ("KeyB",valueForKeyB(line))) --> For calculating X * Y for each line
  # reduceByKey(lambda x1,x2: np.add(x1,x2)) --> For adding all the values for KeyB
  # map(lambda line: line[1]) --> Getting the combined value for KeyB

  B_Tranf = inputLines.map(lambda line: ("KeyB",valueForKeyB(line))).reduceByKey(lambda x1,x2: np.add(x1,x2)).map(lambda line: line[1])
  B_Act = B_Tranf.collect()[0]
  B = np.asmatrix(B_Act)
  
  
  # Multiply A_Inverese with B to get the beta coefficients
  betaCoeff = np.dot(np.linalg.inv(A),B)
  
  # Display betaCoeffList
  betaCoeffList = np.array(betaCoeff).tolist()
  print betaCoeffList
  

  # print the linear regression coefficients in desired output format
  print "beta values: "
  for coeff in betaCoeffList:
      print coeff[0]

  sc.stop()
