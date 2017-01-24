'''
Created on Nov 14, 2016

@author: Subhojyoti
'''

import math
import random
import numpy

class APT(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
       
    def check(self,set,set1):
        testset=[5,6,7,8,9]
        for i in range(len(set1)):
            #if set[i]!=testset[i] or set1[i]!=testset[i]:
            if set1[i]!=testset[i]:
                return False
        return True
    
    def upperBound(self, arm, numPlays):
        #print self.timeTake*self.delta_tilda*self.delta_tilda
        #return math.sqrt(abs(math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*numPlays))
        hat_delta= abs(self.avgPayOffSums[arm]-self.tau) + self.epsilon
        return (math.sqrt(numPlays)*hat_delta)
    
    
    def rewards(self,choice):
        #return random.gauss(self.means[choice],1)
        #print sum(numpy.random.binomial(1,self.means[choice],200))/200.0
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def apt(self,numActions,K,tau,epsilon):
    
        #Set the environment
        self.max1=999999.0
        self.min1=-999999.0
        
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        #self.upbs = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        self.numRounds = 500
        #self.numRounds = 12000
        #self.B = [0] * self.numActions
        #numRounds = 250000
        self.K=K
        self.tau=tau
        self.epsilon=epsilon
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
        for i in range(0,5):
            self.means[i]=0.45
        
        for i in range(5,21):
            self.means[i]=0.4
        
        for i in range(21,30):
            self.means[i]=0.38
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
        '''
        self.means[6]=0.65
        self.means[7]=0.9
        self.means[8]=0.9
            
        self.means[self.bestAction]=0.9
        '''
        
        print self.means
        
        # initialize empirical sums
        self.t=1
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        self.maxAction=[]
        
        for i in range(self.numActions):
            theReward = self.rewards(i)
            #self.numPlays[i]=self.numPlays[i]+1
            
            action=i
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.avgPayOffSums[action]= self.payoffSums[action]/self.numPlays[action]
            
            
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

            self.t = self.t + 1
            
        #t = numActions
        
        #t=1
        while True:
            
            take=self.max1
            for i in range(self.numActions):
                
                self.ucbs[i]=self.upperBound(i,self.numPlays[i])
                #self.upbs[i]=self.upperBound(self.numPlays[i])
                if take>self.ucbs[i]:
                    take=self.ucbs[i]
                    action=i
                #count=count+1
                    
            #action = max(range(len(self.ucbs)), key=lambda i: self.ucbs[i])
            
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.avgPayOffSums[action]= self.payoffSums[action]/self.numPlays[action]
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            #action = max(range(len(self.avgPayOffSums)), key=lambda i: self.avgPayOffSums[i])

            takeArmsTau=[]
            for i in range(self.numActions):
                if self.avgPayOffSums[i]>=self.tau:
                    takeArmsTau.append(i)
            if len(takeArmsTau)==0:
                takeArmsTau.append(0)

            self.maxAction.append(takeArmsTau)


            if self.t>=self.numRounds:
                break
            
            self.t = self.t + 1
            
            #print t
            '''
            if t%100000==0:
                print t
            '''
        
        maxarm=self.min1
        takeArms=[]
        takeArmsTau=[]
        take=-1
        for i in range(self.numActions):
            
                takeArms.append(self.avgPayOffSums[i])
                if maxarm<self.avgPayOffSums[i]:
                    maxarm=self.avgPayOffSums[i]
                    take=i
                if self.avgPayOffSums[i]>=self.tau:
                    takeArmsTau.append(i)
        arm=take

        takeArms=sorted(takeArms,reverse=True)
        finalSet=[]
        print takeArms
        for j in range(0,len(takeArms)):
            for i in range(0,self.numActions):
                if self.avgPayOffSums[i] == takeArms[j] and i not in finalSet and len(finalSet)<self.K:
                    finalSet.append(i)
        

        #print "last arm:"+str(arm) + " turn:"+str(turn) + " wrong:"+str(wrong)
        
        finalSet1=sorted(finalSet)
        finalSetTau1=sorted(takeArmsTau)
        print "numplays: "+str(self.numPlays)
        #print "Final B: "+str(self.B)
        print "last arm:"+str(arm) + " Set: " + str(finalSet1) + " TSet: " + str(finalSetTau1) + " turn:"+str(turn) + " wrong:"+str(wrong)    
        
        #action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward
        
        f = open('testFinal/testAPT2.txt', 'a')
        for r in range(len(self.maxAction)):
            f.writelines("%s\n" % ', '.join(["%d" % k for k in self.maxAction[r]]))
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,arm,self.t,finalSet1,finalSetTau1
        

if __name__ == "__main__":
    
    wrong=0
    i=10
    while i<=10:
        turn=0
        for j in range(1000):
            
            random.seed(i+j)
            
            obj=APT()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep,finalSet,finalSetTau=obj.apt(i,5,0.5,0.0)
            if obj.check(finalSet,finalSetTau)==False:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm) +"\tbset: "+str(finalSet) + "\tbtset: "+str(finalSetTau) + "\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('testFinal/testAPTinfo2.txt', 'a')
            f.writelines("arms: %d\tbArm: %d\tbSet: %s\tbtSet: %s\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, finalSet, finalSetTau, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
                