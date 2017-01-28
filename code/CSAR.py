'''
Created on Dec 28, 2016

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput

class SR(object):
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

    def rewards(self,choice):
        return random.gauss(self.means[choice],self.variance[choice])
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0

    def readenv(self):
        data=[]
        filename="env/GR.txt"
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

    def sr(self,numActions,tau):

        #Set the environment
        self.numActions=numActions

        self.min=-999999.0

        self.payoffSums = [0] * self.numActions
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


        self.means=[]
        self.variance=[]
        self.readenv()

        #self.means =[0.4 for i in range(self.numActions)]
        #self.variance=[0.5 for i in range(self.numActions)]

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
        for i in range(1,self.numActions+1):
            sum1=sum1+(1.0/i)
        self.logK=0.5+sum1

        self.B = [0 for i in range(self.numActions)]
        #self.epoch=1
        self.nk_1=0


        #self.rounds=self.nk-self.nk_1
        flagBreak=False
        for self.epoch in range(0,self.numActions):

            self.nk=int(math.ceil( (self.numRounds - self.numActions)/(self.logK*(self.numActions+1-(self.epoch)))))
            self.rounds=self.nk-self.nk_1
            #print "Rounds: "+ str(self.rounds)


            for arm in range(0,self.numActions):
                for times in range(0,self.rounds):

                    if self.B[arm]!=-1:
                        action=arm

                        theReward = self.rewards(action)
                        #print theReward,action
                        self.arm_reward[action]=self.arm_reward[action]+theReward
                        self.numPlays[action] += 1
                        self.payoffSums[action] += theReward
                        #self.avgPayOffSums[action] = abs((self.payoffSums[action]/self.numPlays[action])-self.tau)
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
                            if self.B[i]!=-1:
                                if self.avgPayOffSums[i]>=self.tau:
                                    takeArmsTau.append(i)

                        if len(takeArmsTau)==0:
                            takeArmsTau.append(0)
                        self.maxAction.append(takeArmsTau)


                        if t>=self.numRounds:
                            flagBreak=True
                            break

                        t = t + 1


            if flagBreak==True:
                break



            #Arm elimination
            min1=999999
            flag=False
            for i in range(self.numActions):
                if self.B[i]!=-1:
                    if self.avgPayOffSums[i]<self.tau:
                        if self.avgPayOffSums[i]<min1:
                            min1=self.avgPayOffSums[i]
                            take=i
                            flag=True

            if flag==True:
                self.B[take]=-1


            self.nk_1=self.nk

            #print self.avgPayOffSums
            #print self.numPlays,sum(self.numPlays),len(self.maxAction)
            #print self.B



        if len(self.maxAction)<self.numRounds:
            current=len(self.maxAction)
            action=self.maxAction[current-1]
            for p in range(current,(self.numRounds)):
                self.maxAction.append(action)

        #print len(self.maxAction)

        #action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward

        action = takeArmsTau

        f = open('testFinal5/testSR1.txt', 'a')
        for r in range(len(self.maxAction)):
            if r<self.numRounds:
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

            obj=SR()
            cumulativeReward,bestActionCumulativeReward,regret,finalSetTau,timestep=obj.sr(i,0.5)
            if obj.check(finalSetTau)==False:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(finalSetTau)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('testFinal5/testSRinfo1.txt', 'a')
            f.writelines("arms: %d\tbArms: %s\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, finalSetTau, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()

            turn=turn+1
        i=i+1
