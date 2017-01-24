'''
Created on Nov 16, 2016

@author: Subhojyoti
'''

import math
import random
import numpy

class ucbE(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    
    def upperBound(self, step, numPlays):
        #self.a= 2 * math.log(step + 1)
        #self.c=1.0/4.0
        self.c=pow(4,4)*1.0
        #self.a= self.c*self.numRounds/self.H1
        self.a=self.c*(self.numRounds-self.numActions)/self.H1
        return math.sqrt( self.a/ numPlays)
    
     
    def rewards(self,choice):
        #return random.gauss(self.means[choice],1)
        #print sum(numpy.random.binomial(1,self.means[choice],200))/200.0
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def ucbE(self,numActions,tau):
    
        #Set the environment
        self.numActions=numActions

        self.min=-999999.0

        self.payoffSums = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [-1*self.min] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 3000000
        self.numRounds = 500
        #numRounds = 250000

        self.tau=tau
        
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-1
        
        #biases = [1.0 / k for k in range(5,5+numActions)]
        #means = [0.5 + b for b in biases]
        self.means =[0.0 for i in range(self.numActions)]
        
        '''
        i=(1*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.05
            i=i+1
        
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.03
            i=i+1
        '''
        '''
        i=(1*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.06
            i=i+1
        
        
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.07
            i=i+1
        
        self.means[self.bestAction]=0.1
        '''

        j=0
        for i in range(0,4):
            self.means[i]=0.2+0.05*j
            j=j+1

        #self.means[3]=0.35
        self.means[4]=0.45
        self.means[5]=0.55

        j=0
        for i in range(6,10):
            self.means[i]=0.6+0.05*j
            j=j+1

        
        # initialize empirical sums
        t=1
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        self.maxAction=[]

        sum1=0.0
        for i in range(self.numActions):
            if i != self.bestAction:
                sum1=sum1+1/math.pow((self.means[self.bestAction]-self.means[i]),2)
        self.H1=sum1
        
        #t=1
        while True:
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            action = random.randint(0,9)
            #action = min(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.avgPayOffSums[action] = self.payoffSums[action]/self.numPlays[action]
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)

            takeArmsTau=[]
            for i in range(self.numActions):
                if self.avgPayOffSums[i]>=self.tau:
                    takeArmsTau.append(i)

            if len(takeArmsTau)==0:
                takeArmsTau.append(0)
            self.maxAction.append(takeArmsTau)


            if t>=self.numRounds:
                break
            
            t = t + 1
            
            #print t
            '''
            if t%100000==0:
                print t
            '''
            
    
        #action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward
        #print self.numPlays
        action = takeArmsTau
        
        f = open('testFinal/testUA1.txt', 'a')
        for r in range(len(self.maxAction)):
            f.writelines("%s\n" % ', '.join(["%d" % k for k in self.maxAction[r]]))
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    i=10
    while i<=10:
        turn=0
        for j in range(1000):
            
            random.seed(i+j)
            
            obj=ucbE()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.ucbE(i,0.5)
            if arm!=i-1:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong"+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('testFinal/testUAinfo1.txt', 'a')
            f.writelines("arms: %d\tbArms: %s\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
        