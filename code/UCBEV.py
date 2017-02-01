'''
Created on Jan 25, 2017

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput

class ucbE(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def check(self,set1):
        testset=[5,6,7,8,9]
        if len(set1)<5 or len(set1)>5:
            return False
        for i in range(len(set1)):
            #if set[i]!=testset[i] or set1[i]!=testset[i]:
            if set1[i]!=testset[i]:
                return False
        return True
    
    def upperBound(self, step, numPlays,arm):
        #self.a= 2 * math.log(step + 1)
        self.c=1.0
        #self.c=1.0/4.0
        #self.c=pow(4,4)*1.0
        #self.a= self.c*self.numRounds/self.H1
        vj=((self.sqPayOffSums[arm]/numPlays) - (self.avgPayOffSums[arm]*self.avgPayOffSums[arm]))
        self.a=self.c*(8.0/9.0)*(self.numRounds-2*self.numActions)/self.H1
        val=math.sqrt((2*self.a*vj)/numPlays)+((7.0*self.a)/((3.0*numPlays)-1))
        return val
    
     
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
        
    def ucbE(self,numActions,tau):
    
        #Set the environment
        self.numActions=numActions

        self.min=-999999.0

        self.payoffSums = [0] * self.numActions
        self.sqPayOffSums = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [-1*self.min] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 3000000
        self.numRounds = 10000
        #numRounds = 250000

        self.tau=tau
        
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-1

        #self.means =[0.4 for i in range(self.numActions)]
        #self.variance=[0.5 for i in range(self.numActions)]

        self.means=[]
        self.variance=[]
        self.readenv()

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
        '''
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

        print self.means
        print self.variance

        # initialize empirical sums
        t=1
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        self.maxAction=[]

        sum1=0.0
        for i in range(0,self.numActions):
            if i != self.bestAction and (self.means[self.bestAction]!=self.means[i]):
                #print self.variance[i] + (self.means[self.bestAction]-self.means[i])
                val1=math.pow(math.sqrt(self.variance[i])+math.sqrt(self.variance[i] + (16.0/3.0)*abs(self.tau-self.means[i])),2)
                val2=math.pow(abs(self.tau - self.means[i]),2)

                #print val1,val2
                sum1=sum1+(val1/val2)
        self.H1=sum1
        
        for i in range(self.numActions):
            theReward = self.rewards(i)
            #self.numPlays[i]=self.numPlays[i]+1

            action=i
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.sqPayOffSums[action] += theReward*theReward
            
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


            t = t + 1
            
        #t = numActions

        
            
        
        #t=1
        while True:
            ucbs = [abs(self.avgPayOffSums[i] - self.tau) - self.upperBound(t, self.numPlays[i],i) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            action = min(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.sqPayOffSums[action] += theReward*theReward
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

        action = takeArmsTau
        
        f = open('testFinal7/testUCBEMV11.txt', 'a')
        for r in range(len(self.maxAction)):
            f.writelines("%s\n" % ', '.join(["%d" % k for k in self.maxAction[r]]))
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(500):
            
            random.seed(i+j)
            
            obj=ucbE()
            cumulativeReward,bestActionCumulativeReward,regret,finalSetTau,timestep=obj.ucbE(i,0.5)
            if obj.check(finalSetTau)==False:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(finalSetTau)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('testFinal7/testUCBEMVinfo11.txt', 'a')
            f.writelines("arms: %d\tbArms: %s\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, finalSetTau, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
        
