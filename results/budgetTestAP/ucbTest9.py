'''
Created on Nov 26, 2016

@author: Subhojyoti
'''


import math
import random
import numpy

class ucbtest(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
       
    def check(self,set,set1):
        testset=[5,6,7,8,9]
        if len(set1)<5:
            return False
        for i in range(len(set1)):
            #if set[i]!=testset[i] or set1[i]!=testset[i]:
            if set1[i]!=testset[i]:
                return False
        return True
     
    def remArms(self):
        count=0
        for i in range(self.numActions):
            if self.B[i]!=-1 and self.B[i]!=-2:
                count=count+1
        return count   
    
    def upperBound(self, numPlays):
        #print self.timeTake*self.delta_tilda*self.delta_tilda
        #return math.sqrt(abs(math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*numPlays))
        return math.sqrt(max(0,math.log((self.psi*self.numRounds*self.delta_tilda*self.delta_tilda))) / (2*self.weight*numPlays))
    
    def upperBound1(self, numPlays):
        #print self.timeTake*self.delta_tilda*self.delta_tilda
        #return math.sqrt(abs(math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*self.weight*numPlays))
        #return math.sqrt(max(0,math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*self.weight*numPlays))
        return math.sqrt(max(0,math.log((self.psi*self.numRounds*self.delta_tilda*self.delta_tilda))) / (2*self.weight*numPlays))
        #return math.sqrt(max(0,math.log((self.psi*self.numRounds))) / (2*self.weight*numPlays))
    
     
    def rewards(self,choice):
        #return random.gauss(self.means[choice],1)
        #print sum(numpy.random.binomial(1,self.means[choice],200))/200.0
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def ucb1(self,numActions,K,tau):
    
        #Set the environment
        self.max1=999999.0
        self.min1=-999999.0
        
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.ucbs1 = [0] * self.numActions
        self.upbs = [0] * self.numActions
        self.upbs1 = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        self.numRounds = 500
        #self.numRounds = 12000
        self.B = [0] * self.numActions
        #numRounds = 250000
        self.K=K
        self.tau=tau
        self.m=0
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
        
        
        self.delta_tilda=1.0
        #self.delta_tilda1=1.0
        #self.alpha=100.0
        #self.alpha=self.numActions*1.0
        #self.gamma=1.0/self.alpha
        #self.timeTake=self.numActions
        #self.timeTake=1.0
        #self.timeTake=math.floor(self.numRounds*self.gamma)
        #self.psi=math.log(self.numRounds)
        #self.psi=self.numActions*self.numActions*self.timeTake*self.timeTake*self.timeTake
        #self.psi = math.log(self.numRounds)
        self.psi=(self.numActions*self.numActions*self.numRounds*self.numRounds*self.numRounds)
        #self.psi=(self.numActions*self.numActions*self.t*self.t*self.t)
        #self.psi=1.0
        #self.psi=self.numRounds
        #self.psi=math.log(self.numRounds)
        self.weight=1.0
        #self.weight=1.0/10.0
        #self.weight=math.sqrt(self.numRounds)
        #self.gamma=1.0/self.numActions
        #self.p=2.0
        #self.gamma=(self.p+1.0)/(self.p)
        #self.gamma=3.0/2.0
        self.gamma=math.floor(0.5*math.log10(self.numRounds/math.e)/math.log10(2))
        print self.gamma
        #self.weight=self.numActions
        #self.timeTake=self.numActions+math.floor(self.numRounds*self.gamma)
        #self.timeTake=self.gamma*2
        #self.timeTake=math.floor(self.numActions*self.gamma)
        self.timeTake=math.floor(self.numRounds/self.gamma)
        #self.timeTake = math.floor((self.numRounds - self.numActions)/(0.5*math.floor(math.log10(self.numRounds/math.e)/math.log10(2))))
        #t=1
        
        self.takeArmTau=[]
        
        while True:
            
            #take=self.min1
            take=self.max1
            for i in range(self.numActions):
                if self.B[i]==0:
                    #self.func=math.sqrt(1/self.timeTake)
                    #self.ucbs[i]=(self.payoffSums[i] / self.numPlays[i]) + math.sqrt(2 * math.log(self.t + 1) / self.numPlays[i])
                    self.ucbs[i]=abs(self.avgPayOffSums[i]-self.tau) - self.upperBound1(self.numPlays[i])
                    #self.ucbs[i]=self.upperBound1(self.numPlays[i])
                    #self.upbs[i]=self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])
                    #self.upbs1[i]=self.avgPayOffSums[i] + self.upperBound1(self.numPlays[i])
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

            '''
            #action = max(range(len(self.avgPayOffSums)), key=lambda i: self.avgPayOffSums[i])
            take=self.min1
            #take=self.max1
            for i in range(self.numActions):
                #if self.B[i]!=-1:
                    #self.func=math.sqrt(1/self.timeTake)
                    #self.ucbs[i]=-(self.payoffSums[i] / self.numPlays[i]) + math.sqrt(2 * math.log(self.t + 1) / self.numPlays[i])
                    #self.ucbs[i]=self.avgPayOffSums[i] + self.upperBound1(self.numPlays[i])
                    #self.upbs[i]=self.upperBound(self.numPlays[i])
                    if take<self.avgPayOffSums[i]:
                        take=self.avgPayOffSums[i]
                        action=i
            '''
                
            #print "\n\nRound: "+str(self.m)
            
            for i in range(self.numActions):
                if self.B[i]==0:
                    #self.func=math.sqrt(1/self.timeTake)
                    #self.ucbs[i]=(self.payoffSums[i] / self.numPlays[i]) + math.sqrt(2 * math.log(self.t + 1) / self.numPlays[i])
                    self.ucbs[i]=self.avgPayOffSums[i] + self.upperBound1(self.numPlays[i])
                    self.ucbs1[i]=self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])
                    self.upbs[i]=self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])
                    self.upbs1[i]=self.avgPayOffSums[i] + self.upperBound1(self.numPlays[i])
              
            for i in range(self.numActions):
                #print self.upbs[i],self.upbs[action]
                if self.B[i]==0:
                    #if (self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])) < ( self.avgPayOffSums[action] + self.upperBound1(self.numPlays[action])):
                    #if (self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])) > (1 - self.tau)/2:
                    if (self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])) > self.tau + self.upperBound1(self.numPlays[i]):
                        
                        self.B[i]=-1
                        self.takeArmTau.append(i)
                        
                        print "\n\nRound: "+str(self.t)
                        print "B: "+str(self.B)
                        print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))
                        print "AvgP: "+str(self.avgPayOffSums)
                        print "ucbs: "+str(self.ucbs)
                        print "ucbs1: "+str(self.ucbs1)
                        print "upbs: "+str(self.upbs)
                        print "upbs1: "+str(self.upbs1)
                        #print "gamma: "+str(self.gamma) + " timeTake: "+str(self.timeTake)+ " delta_tilde: "+str(self.delta_tilda)+ " t: "+str(self.t)
                        print "delta_tilde: "+str(self.delta_tilda)+ " weight: " +str(self.weight) + " t: "+str(self.t)
                        
                    if (self.avgPayOffSums[i] + self.upperBound1(self.numPlays[i])) < self.tau - self.upperBound1(self.numPlays[i]):

                        self.B[i]=-2
                        #self.takeArmTau.append(i)

                        print "\n\nRound: "+str(self.t)
                        print "B: "+str(self.B)
                        print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))
                        print "AvgP: "+str(self.avgPayOffSums)
                        print "ucbs: "+str(self.ucbs)
                        print "ucbs1: "+str(self.ucbs1)
                        print "upbs: "+str(self.upbs)
                        print "upbs1: "+str(self.upbs1)
                        #print "gamma: "+str(self.gamma) + " timeTake: "+str(self.timeTake)+ " delta_tilde: "+str(self.delta_tilda)+ " t: "+str(self.t)
                        print "delta_tilde: "+str(self.delta_tilda)+ " weight: " +str(self.weight) + " t: "+str(self.t)
                
                #self.timeTake=self.gamma*self.timeTake
                #self.gamma=max(1.0/((self.numRounds)), self.gamma*(1.0/self.alpha))
                #self.gamma=self.gamma*self.gamma
                #self.timeTake= self.timeTake + math.floor(self.timeTake*self.gamma)
                #self.delta_tilda=self.delta_tilda/self.gamma

            if self.t >= self.timeTake:

                print "\n\nRound: "+str(self.m) + " timeTake: "+str(self.timeTake)
                self.delta_tilda=max(self.delta_tilda/2, math.sqrt(math.e/(self.numRounds)) )
                #self.weight=min(self.weight+10,self.numActions*math.sqrt(self.numRounds))
                self.weight = pow(2, self.m)
                #self.delta_tilda=self.delta_tilda/2
                #self.psi=(self.numActions*self.numActions*self.t*self.t*self.t)
                #self.weight = self.weight/2.0
                #self.p=self.p+1.0
                #self.gamma = (self.p+1.0)/(self.p)
                #self.weight = self.weight + 1.0
                #self.weight = self.weight + math.log(self.t)
                #self.timeTake=self.timeTake + math.floor(self.timeTake*self.gamma)
                self.timeTake=2*self.timeTake
                self.m = self.m + 1

            if (self.remArms()==0):
                break
            #self.psi=self.t*self.t
            #self.psi=math.pow(2, self.m)
            #self.weight=min(4,math.pow(2, self.m))
            #self.weight=1.0/math.pow(2, self.m)
            #self.weight = math.pow(2, self.m)
            #self.m=self.m+1
            #self.gamma=self.gamma*2.0
            
            '''   
            print "B: "+str(self.B)
            print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))
            print "AvgP: "+str(self.avgPayOffSums)
            print "ucbs: "+str(self.ucbs)
            print "upbs: "+str(self.upbs)
            print "upbs1: "+str(self.upbs1)
            #print "gamma: "+str(self.gamma) + " timeTake: "+str(self.timeTake)+ " delta_tilde: "+str(self.delta_tilda)+ " t: "+str(self.t)
            print "delta_tilde: "+str(self.delta_tilda)+ " t: "+str(self.t)
            '''
            #if self.t>=self.numRounds or self.remArms()<=self.K:

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
        
        
        maxarm=self.min1
        takeArms=[]
        takeArmsTau=[]
        #takeArmsTau=self.takeArmTau


        take=-1
        for i in range(self.numActions):
            #if self.B[i]==-1:
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

        print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))
        print "Final B: "+str(self.B)
        print "last arm:"+str(arm) + " Set: " + str(finalSet1) + " TSet: " + str(finalSetTau1) + " turn:"+str(turn) + " wrong:"+str(wrong)
        
        
        '''
        while self.t<self.numRounds:

            theReward = self.rewards(arm)
            self.arm_reward[arm]=self.arm_reward[arm]+theReward
            self.numPlays[arm] += 1
            self.payoffSums[arm] += theReward

            self.avgPayOffSums[arm] = self.payoffSums[arm] / self.numPlays[arm]

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if arm == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            self.actionRegret.append(regret)
            
            self.t=self.t+1
        '''
        
        f = open('testFinal/testAugUCB5.txt', 'a')
        for r in range(len(self.maxAction)):
            f.writelines("%s\n" % ', '.join(["%d" % k for k in self.maxAction[r]]))
        f.close()
        
        #action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward

        return cumulativeReward,bestActionCumulativeReward,regret,arm,self.t,finalSet1,finalSetTau1
        

if __name__ == "__main__":
    
    wrong=0
    i=10
    while i<=10:
        turn=0
        for j in range(1000):
            
            random.seed(i+j)
            
            obj=ucbtest()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep,finalSet,finalSetTau=obj.ucb1(i,5,0.5)
            if obj.check(finalSet,finalSetTau)==False:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm) +"\tbset: "+str(finalSet) + "\tbtset: "+str(finalSetTau) + "\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('testFinal/testAugUCBtest5.txt', 'a')
            #f.writelines("arms: %d\tbArm: %d\tbSet: %s\tbtSet: %s\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, finalSet, finalSetTau, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
                