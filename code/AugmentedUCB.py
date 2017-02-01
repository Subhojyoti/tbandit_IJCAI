'''
Created on Jan 23, 2017

@author: Subhojyoti
'''


import math
import random
import numpy
import fileinput

class AugUCB(object):
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
     
    def remArms(self):
        count=0
        for i in range(self.numActions):
            if self.B[i]!=-1 and self.B[i]!=-2:
                count=count+1
        return count   

    def exp_func(self):
        
        #self.psi=math.log(self.numRounds)
        #self.psi=self.numActions*self.numActions*self.timeTake*self.timeTake*self.timeTake
        self.psi = self.numRounds / math.log(self.numActions)
        #self.psi=(self.numActions*self.numActions*self.numRounds)
        #self.psi=(self.numActions*self.numActions*self.numRounds*self.numRounds*self.numRounds)
        #self.psi=(self.numActions*self.numActions*self.t*self.t*self.t)
        #self.psi=1.0
        return self.psi

    def upperBound(self, numPlays):
        #print self.timeTake*self.delta_tilda*self.delta_tilda
        #return math.sqrt(abs(math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*self.rho*numPlays))
        #return math.sqrt(max(0,math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*self.rho*numPlays))
        return math.sqrt(self.rho * math.log((self.exp_func()*self.numRounds*self.delta_tilda*self.delta_tilda)) / (2*numPlays))
        #return math.sqrt(max(0,math.log((self.psi*self.numRounds))) / (2*self.rho*numPlays))



    def upperBoundVar(self, numPlays, arm):
        #print self.timeTake*self.delta_tilda*self.delta_tilda
        #return math.sqrt(abs(math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*self.rho*numPlays))
        #return math.sqrt(max(0,math.log((self.psi*self.timeTake*self.delta_tilda*self.delta_tilda))) / (2*self.rho*numPlays))
        vj=((self.sqPayOffSums[arm]/numPlays) - (self.avgPayOffSums[arm]*self.avgPayOffSums[arm]))
        #print vj
        return math.sqrt(self.rho_v * vj * math.log((self.exp_func()*self.numRounds*self.delta_tilda*self.delta_tilda)) / (4*numPlays) + (self.rho_v* math.log((self.exp_func()*self.numRounds*self.delta_tilda*self.delta_tilda)) / (4*numPlays)))
        #return math.sqrt(self.rho_v * vj * math.log((self.exp_func()*self.numRounds*self.delta_tilda*self.delta_tilda)) / (2*numPlays))
        #return math.sqrt(max(0,math.log((self.psi*self.numRounds))) / (2*self.rho*numPlays))


    def rewards(self,choice):
        return random.gauss(self.means[choice],self.variance[choice])
        #print sum(numpy.random.binomial(1,self.means[choice],200))/200.0
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
     
    def arm_elimination(self):
        
        for i in range(self.numActions):

            #print self.upbs[i],self.upbs[action]
            if self.B[i]==0:
                #if (self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])) < ( self.avgPayOffSums[action] + self.upperBound1(self.numPlays[action])):
                #if (self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])) > (1 - self.tau)/2:
                if (self.avgPayOffSums[i] - self.upperBound(self.numPlays[i])) > self.tau + self.upperBound(self.numPlays[i]):

                    self.B[i]=-1

                    #self.takeArmTau.append(i)
                    print "\n\nRound: "+str(self.t)
                    print "B: "+str(self.B)
                    print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))

                if (self.avgPayOffSums[i] + self.upperBound(self.numPlays[i])) < self.tau - self.upperBound(self.numPlays[i]):

                    self.B[i]=-2

                    print "\n\nRound: "+str(self.t)
                    print "B: "+str(self.B)
                    print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))

    def arm_elimination_variance(self):

        for i in range(self.numActions):

            #print self.upbs[i],self.upbs[action]
            if self.B[i]==0:
                #if (self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])) < ( self.avgPayOffSums[action] + self.upperBound1(self.numPlays[action])):
                #if (self.avgPayOffSums[i] - self.upperBound1(self.numPlays[i])) > (1 - self.tau)/2:
                if (self.avgPayOffSums[i] - self.upperBoundVar(self.numPlays[i],i)) > self.tau + self.upperBoundVar(self.numPlays[i],i):

                    self.B[i]=-11

                    #self.takeArmTau.append(i)
                    print "\n\nRound: "+str(self.t)
                    print "B: "+str(self.B)
                    print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))

                if (self.avgPayOffSums[i] + self.upperBoundVar(self.numPlays[i],i)) < self.tau - self.upperBoundVar(self.numPlays[i],i):

                    self.B[i]=-22

                    #self.takeArmTau.append(i)
                    print "\n\nRound: "+str(self.t)
                    print "B: "+str(self.B)
                    print "numplays: "+str(self.numPlays)+str(sum(self.numPlays))

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

    def augucb(self,numActions,K,tau):
    
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
        self.sqPayOffSums = [0] * self.numActions
        self.numRounds = 10000
        #self.numRounds = 12000
        self.B = [0] * self.numActions
        #numRounds = 250000
        self.K=K
        self.tau=tau
        self.m=0
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-1
        

        #self.means =[0.4 for i in range(self.numActions)]
        #self.variance = [0.5 for i in range(self.numActions)]

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
        self.means[6]=0.65
        self.means[7]=0.9
        self.means[8]=0.9
            
        self.means[self.bestAction]=0.9
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
            self.sqPayOffSums[action] += theReward*theReward
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
        
        
        #self.delta_tilda=self.tau
        self.delta_tilda=1.0
        #self.alpha=100.0
        #self.alpha=self.numActions*1.0
        #self.gamma=1.0/self.alpha
        #self.timeTake=self.numActions
        #self.timeTake=1.0
        #self.timeTake=math.floor(self.numRounds*self.gamma)
        #self.psi=math.log(self.numRounds)
        #self.psi=self.numActions*self.numActions*self.timeTake*self.timeTake*self.timeTake
        #self.psi = math.log(self.numRounds)
        #self.psi=(self.numActions*self.numActions*self.numRounds)
        #self.psi=(self.numActions*self.numActions*self.t*self.t*self.t)
        #self.psi=1.0
        #self.psi=self.numRounds
        #self.psi=math.log(self.numRounds)
        #self.rho=8.0
        #self.rho = [(self.tau*self.tau)/4.0 for i in range(self.numActions)]
        #self.rho = (self.tau*self.tau)/8.0
        #self.rho = 1.0/(8.0*self.tau*self.tau)
        self.rho=1.0/8.0
        self.rho_v=2.0/3.0
        #self.rho=math.sqrt(self.numRounds)
        #self.gamma=1.0/self.numActions
        #self.p=2.0
        #self.gamma=(self.p+1.0)/(self.p)
        #self.gamma=3.0/2.0
        self.gamma=math.floor(0.5*math.log10(self.numRounds/math.e)/math.log10(2))
        #self.rho=self.numActions
        #self.timeTake=self.numActions+math.floor(self.numRounds*self.gamma)
        #self.timeTake=self.gamma*2
        #self.timeTake=math.floor(self.numActions*self.gamma)

        #self.timeTake=math.floor(self.numRounds/self.gamma)
        self.nm=math.ceil(2*math.log(self.exp_func()*self.numRounds*self.delta_tilda*self.delta_tilda)/self.delta_tilda)
        self.timeTake=self.numActions * self.nm
        print self.gamma,self.timeTake


        
        #self.timeTake = math.floor((self.numRounds - self.numActions)/(0.5*math.floor(math.log10(self.numRounds/math.e)/math.log10(2))))
        #t=1
        
        self.takeArmTau=[]
        
        while True:
            
            #take=self.min1
            take=self.max1
            for i in range(self.numActions):
                if self.B[i]==0:

                    self.ucbs[i]=abs(self.avgPayOffSums[i]-self.tau) - self.upperBoundVar(self.numPlays[i],i)

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
            self.sqPayOffSums[action] += theReward*theReward
            self.avgPayOffSums[action]= self.payoffSums[action]/self.numPlays[action]
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            #self.t = self.t + 1
            
            self.actionRegret.append(regret)
            
            self.arm_elimination()
            self.arm_elimination_variance()
            




            if self.t >= self.timeTake and self.m <= self.gamma:

                print "\n\nRound: "+str(self.m) + " timeTake: "+str(self.timeTake)
                self.delta_tilda=self.delta_tilda/2
                self.nm=math.ceil(2*math.log(self.exp_func()*self.numRounds*self.delta_tilda*self.delta_tilda)/self.delta_tilda)
                self.timeTake=self.t + self.remArms()*self.nm
                self.m = self.m + 1

            if (self.remArms()==0):
                break
            if self.t>=self.numRounds:
                break

            

            #if self.t>=self.numRounds or self.remArms()<=self.K:

            takeArmsTau=[]
            for i in range(self.numActions):
                if self.avgPayOffSums[i]>=self.tau:
                    takeArmsTau.append(i)


            if len(takeArmsTau)==0:
                takeArmsTau.append(0)

            self.maxAction.append(takeArmsTau)



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
                #if self.B[i]==-1:
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

        last=self.maxAction[len(self.maxAction)-1]
        index=len(self.maxAction)
        if len(self.maxAction)<self.numRounds:
            for p in range(0,(self.numRounds - index)):
                self.maxAction.append(last)
        
        f = open('testFinal7/testAugUCBV1.txt', 'a')
        for r in range(len(self.maxAction)):
            f.writelines("%s\n" % ', '.join(["%d" % k for k in self.maxAction[r]]))
        f.close()
        
        #action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward

        return cumulativeReward,bestActionCumulativeReward,regret,arm,self.t,finalSet1,finalSetTau1
        

if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(500):
            
            random.seed(i+j)
            
            obj=AugUCB()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep,finalSet,finalSetTau=obj.augucb(i,5,0.5)
            if obj.check(finalSet,finalSetTau)==False:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm) +"\tbset: "+str(finalSet) + "\tbtset: "+str(finalSetTau) + "\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('testFinal7/testAugUCBVtest1.txt', 'a')
            f.writelines("arms: %d\tbArm: %d\tbSet: %s\tbtSet: %s\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, finalSet, finalSetTau, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
                