'''
Created on Nov 14, 2016

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput

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
        if len(set1)<5 or len(set1)>5:
            return False
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
        return random.gauss(self.means[choice],self.variance[choice])
        #print sum(numpy.random.binomial(1,self.means[choice],200))/200.0
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0

    def readenv(self):
        data=[]
        filename="env/GP.txt"
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
        self.numRounds = 10000
        #self.numRounds = 12000
        #self.B = [0] * self.numActions
        #numRounds = 250000
        self.K=K
        self.tau=tau
        self.epsilon=epsilon
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-1


        self.means =[]
        self.variance=[]
        self.readenv()

        '''
        self.means =[0.4 for i in range(self.numActions)]
        self.variance=[0.5 for i in range(self.numActions)]

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

        '''
        j=0
        for i in range(0,4):
            self.means[i]=0.4-pow(0.2,i+1)
            j=j+1
            
        #self.means[3]=0.35
        self.means[4]=0.45
        self.means[5]=0.55
        
        j=1
        for i in range(6,10):
            self.means[i]=0.6+pow(0.2,5-(j))
            j=j+1
        '''

        '''
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




        for i in range(10, self.numActions):
            self.variance[i]=numpy.random.uniform(0.4,0.45)
        for i in range(10, self.numActions):
            self.means[i]=numpy.random.uniform(0.38,0.42)

        f = open('env/GR.txt', 'w')
        f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.means])))
        f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.variance])))
        f.close()
        '''

        print self.means
        print self.variance

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

        f = open('testFinal7/testAPT1.txt', 'a')
        for r in range(len(self.maxAction)):
            f.writelines("%s\n" % ', '.join(["%d" % k for k in self.maxAction[r]]))
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,arm,self.t,finalSet1,finalSetTau1
        

if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(500):
            
            random.seed(i+j)
            
            obj=APT()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep,finalSet,finalSetTau=obj.apt(i,5,0.5,0.01)
            if obj.check(finalSet,finalSetTau)==False:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm) +"\tbset: "+str(finalSet) + "\tbtset: "+str(finalSetTau) + "\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('testFinal7/testAPTinfo1.txt', 'a')
            f.writelines("arms: %d\tbArm: %d\tbSet: %s\tbtSet: %s\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, finalSet, finalSetTau, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
                