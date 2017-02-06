'''
Created on Jan 27, 2016

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput

class CreateEnvironment(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    


    def readenv(self):
        data=[]
        filename="env/AP.txt"
        for line in fileinput.input([filename]):

            try:
                line1 = [line.split(", ") or line.split("\n") ]
                #print numpy.shape(line1)
                #print line1
                take=[]
                for i in range(len(line1[0])):
                    take.append(float(line1[0][i]))
                #print take
                data.append(take)
            except ValueError,e:
                print e
        #print data
        self.means=(data[0])
        self.variance=(data[1])

    def create(self,numActions):
    
        #Set the environment

        self.numActions=numActions

        '''
        self.means =[]
        self.variance=[]
        self.readenv()
        '''

        self.means =[0.4 for i in range(self.numActions)]
        self.variance=[0.5 for i in range(self.numActions)]

        '''
        #AP
        j=0
        for i in range(0,4):
            self.means[i]=0.2+0.05*j
            j=j+1

        #self.means[3]=0.35
        self.means[4]=0.45
        self.means[5]=0.55
        self.variance[5]=0.6

        j=0
        for i in range(6,10):
            self.means[i]=0.6+0.05*j
            self.variance[i]=0.6
            j=j+1
        '''

        #GP
        j=0
        for i in range(0,4):
            self.means[i]=0.4-pow(0.2,i+1)
            j=j+1
            
        #self.means[3]=0.35
        self.means[4]=0.45
        self.means[5]=0.55
        self.variance[5]=0.6

        j=1
        for i in range(6,10):
            self.means[i]=0.6+pow(0.2,5-(j))
            self.variance[i]=0.6
            j=j+1

        '''
        #4GR
        for i in range(0,3):
            self.means[i]=0.1

        j=0
        for i in range(3,7):
            self.means[i]=0.35+(0.1*j)
            j=j+1

        for i in range(7,10):
            self.means[i]=0.9
            self.variance[i]=0.6

        self.means[4]=0.45
        self.variance[5]=0.6
        self.variance[6]=0.6
        '''



        for i in range(10, self.numActions):
            self.variance[i]=numpy.random.uniform(0.3,0.4)
        for i in range(10, self.numActions):
            self.means[i]=numpy.random.uniform(0.4,0.4)

        f = open('env/GP.txt', 'w')
        f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.means])))
        f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.variance])))
        f.close()


        print self.means
        print self.variance




        

if __name__ == "__main__":

        numActions=100
        obj=CreateEnvironment()
        obj.create(numActions)

                