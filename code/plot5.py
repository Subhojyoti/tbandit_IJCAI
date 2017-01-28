'''
Created on Jan 26, 2017

@author: Subhojyoti
'''

from matplotlib import pyplot as plt
import numpy
import fileinput

def column(A, j):
    return [A[i][j] for i in range(len(A))]

def transpose(A):
    return [column(A, j) for j in range(len(A[0]))]

def calc1(timestep,test,data,wrongArr):

    i=0

    while i < timestep:
        wrong=0
        if len(data[i])==len(test):

            for j in range(len(test)):
                if data[i][j]!=test[j]:
                    wrong=1
                    break
            #print data[i],test,wrong
        else:
            wrong=1
        wrongArr[i]=wrongArr[i] + wrong
        i=i+1
        #wrongArr.append(wrong)

    #print wrongArr
    return  wrongArr

def calc(timestep,N,test,data,wrongArr):
    for i in range(0,timestep):
        #for i in range(len(data)):
        print i
        wrong=0.0
        while i < timestep*N:
            #if len(data[i])==len(test):
                #print data[i],test
            take=0.0
            for j in range(len(data[i])):
                #print j,len(data[i]),data[i]
                for k in range(len(test)):
                    if data[i][j]!=test[k]:
                        take=take+1.0

            #wrong=(take*len(data[i]))/(len(data[i])-take)
            wrong=wrong+take/len(data[i])

            i=i+timestep
        wrongArr.append(wrong)

    #print wrongArr
    return  wrongArr

def func_print(filename,wrongArr,xs):
    
    
    f = open(filename, 'w')
    
    for r in range(len(xs)):
        #if (xs[r])%10==0 or xs[r]==500:
        f.writelines(str(xs[r])+"\t"+str(wrongArr[r])+"\n")
    f.close()
        

#def regretWeightsGraph(filename,filename1,filename2,filename3,filename4,filename5):
#def regretWeightsGraph(filename,filename1):
#def regretWeightsGraph(filename,filename1,filename2):
def regretWeightsGraph(filename):

    timestep=10000
    N=500.0
    test=[5,6,7,8,9]
    wrongArr=[0 for i in range(timestep)]
    wrongArr1=[]
    wrongArr2=[]
    wrongArr3=[]
    wrongArr4=[]
    wrongArr5=[]




    data=[]
    '''
    data1=[]
    data2=[]
    '''
    count=0
    j=0

    for line in fileinput.input([filename]):
        #print line
        try:
            line1 = [line.split(", ") or line.split("\n") ]
            #print numpy.shape(line1)
            take=[]
            for i in range(len(line1[0])):
                take.append(int(line1[0][i]))
            data.append(take)
            prev_data=[]
            prev_data.append(take)
            count=count+1
            if count==timestep:
                #print wrongArr
                wrongArr = calc1(timestep,test,data,wrongArr)
                count=0
                data=[]
                j=j+1
                print j
        except ValueError,e:

            print prev_data,count
            data.append(prev_data)
            data.append(prev_data)
            count=count+1
            print e

    '''
    count=0
    for line in fileinput.input([filename1]):
        #print line
        line1 = [line.split(", ") or line.split("\n") ]
        #print numpy.shape(line1)
        take=[]
        for i in range(len(line1[0])):
            take.append(int(line1[0][i]))
        data1.append(take)
        count=count+1
        #if count==15000*50:
            #fileinput.input.close()
            #break
        #print take

    count=0
    for line in fileinput.input([filename2]):
        #print line
        line1 = [line.split(", ") or line.split("\n") ]
        #print numpy.shape(line1)
        take=[]
        for i in range(len(line1[0])):
            take.append(int(line1[0][i]))
        data2.append(take)
        count=count+1
        #if count==15000*50:
            #fileinput.input.close()
            #break
        #print take
    '''

    '''
    with open(filename, 'r') as infile:
        lines = infile.readlines()
        #print lines

    with open(filename1, 'r') as infile:
        lines1 = infile.readlines()

    with open(filename2, 'r') as infile:
        lines2 = infile.readlines()

    with open(filename3, 'r') as infile:
        lines3 = infile.readlines()

    with open(filename4, 'r') as infile:
        lines4 = infile.readlines()
    
    with open(filename5, 'r') as infile:
        lines5 = infile.readlines()
    '''

    '''
    #lines = [[eval(x.split(", ")[1]) for x in line.split('\n')] for line in lines]
    lines = [[x.split(", ") for x in line.split("\n")] for line in lines]
    #print lines[10][0]

    data=[[] for i in range(len(lines))]
    for i in range(len(lines)):
        for j in range(len(lines[i][0])):
            data[i].append(int(lines[i][0][j]))

    #print data

    lines1 = [[x.split(", ") for x in line.split("\n")] for line in lines1]
    #print lines[10][0]

    data1=[[] for i in range(len(lines1))]
    for i in range(len(lines1)):
        for j in range(len(lines1[i][0])):
            data1[i].append(int(lines1[i][0][j]))

    #print len(data1)

    lines2 = [[x.split(", ") for x in line.split("\n")] for line in lines2]
    #print lines[10][0]

    data2=[[] for i in range(len(lines2))]
    for i in range(len(lines2)):
        for j in range(len(lines2[i][0])):
            data2[i].append(int(lines2[i][0][j]))

    lines3 = [[x.split(", ") for x in line.split("\n")] for line in lines3]
    #print lines[10][0]

    data3=[[] for i in range(len(lines3))]
    for i in range(len(lines3)):
        for j in range(len(lines3[i][0])):
            data3[i].append(int(lines3[i][0][j]))

    lines4 = [[x.split(", ") for x in line.split("\n")] for line in lines4]
    #print lines[10][0]

    data4=[[] for i in range(len(lines4))]
    for i in range(len(lines4)):
        for j in range(len(lines4[i][0])):
            data4[i].append(int(lines4[i][0][j]))
     
    lines5 = [[x.split(", ") for x in line.split("\n")] for line in lines5]
           
    data5=[[] for i in range(len(lines5))]
    for i in range(len(lines5)):
        for j in range(len(lines5[i][0])):
            data5[i].append(int(lines5[i][0][j]))
    '''


    print numpy.shape(data)
    #print numpy.shape(data1)

    #wrongArr = calc1(timestep,N,test,data,wrongArr)
    print wrongArr

    '''
    wrongArr1 = calc1(timestep,N,test,data1,wrongArr1)
    wrongArr2 = calc1(timestep,N,test,data2,wrongArr2)
    wrongArr3 = calc(timestep,N,test,data3,wrongArr3)
    wrongArr4 = calc(timestep,N,test,data4,wrongArr4)
    wrongArr5 = calc(timestep,N,test,data5,wrongArr5)
    '''
    
    for i in range(0,timestep):
        wrongArr[i]=(wrongArr[i]/N)*100.0

        '''
        wrongArr1[i]=(wrongArr1[i]/N)*100.0
        wrongArr2[i]=(wrongArr2[i]/N)*100.0
        wrongArr3[i]=(wrongArr3[i]/N)*100.0
        wrongArr4[i]=(wrongArr4[i]/N)*100.0
        wrongArr5[i]=(wrongArr5[i]/N)*100.0
        '''
    
    #xs=[i for i in range(0,500)]
    xs = range(1,timestep+1)
    
    func_print("testFinal5/SR1.txt",wrongArr,xs)

    '''
    func_print("testFinal4/AugUCB.txt",wrongArr1,xs)
    func_print("testFinal4/UCBEM1.txt",wrongArr2,xs)
    func_print("budgetTestGR/UCBE_1_4.txt",wrongArr3,xs)
    func_print("budgetTestGR/UCBE_256.txt",wrongArr4,xs)
    func_print("budgetTestGR/UA.txt",wrongArr5,xs)
    '''
    
    ax1 = plt.subplot(111)
    plt.ylabel('Error percentage',fontsize=18)
    plt.xlabel('time',fontsize=18)
    ax1.plot(xs, wrongArr,label="APT")
    '''
    ax1.plot(xs, wrongArr1,label="AugUCB")
    ax1.plot(xs, wrongArr2,label="UCBE(1)")
    ax1.plot(xs, wrongArr3,label="UCBE(1/4)")
    ax1.plot(xs, wrongArr4,label="UCBE(256)")
    ax1.plot(xs, wrongArr5,label="UA")
    '''
    #ax1.plot(xs, regret3,'r--',label="ClusUCB(p=K/5)[No Error Margin]")
    #ax1.plot(xs, regret4,label="MOSS")
    #ax1.plot(xs, new,label="Clus-UCB(D=8,w=4)")
    #ax1.plot(xs, regret7,label="MedElim(0.1,0.1)")

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
           ncol=2, mode="expand", borderaxespad=0.)
    
    plt.show()


if __name__ == "__main__":
    #regretWeightsGraph('ucbTest1/testRN110UCB_2m_0.47.txt','ucbTest1/testR1_2m_0.47.txt','ucbTest/testRNUCB1_new.txt', "Regret of UCB\n10 actions, 1 million rounds")
    #regretWeightsGraph('ucbTest1/testRNUCB_new.txt','ucbTest1/testR_new.txt','ucbTest1/testRNUCB1_new.txt', "Regret of UCB\n10 actions, 1 million rounds")

    #regretWeightsGraph('expt7/clUCB20_200.txt','expt7/clUCB05.txt','expt7/MOSS20_200.txt', )
    #regretWeightsGraph('testFinal4/testAPT1.txt','testFinal4/testAugUCB1.txt', 'testFinal2/testUCBEM1.txt', 'testFinal2/testUCBEM2_1_4.txt', 'testFinal2/testUCBEM3_256.txt','testFinal2/testUA1.txt' )
    #regretWeightsGraph('testFinal4/testAPT3.txt','testFinal4/testAugUCBV1.txt')
    #regretWeightsGraph('testFinal1/testAPT1.txt','testFinal1/testAugUCBV1.txt','testFinal4/testUCBEM1.txt')
    #regretWeightsGraph('testExp/testCLUCB500_final11.txt','testExp/testR_new500_1.txt','testExp/testMedElim500_2.txt', "Regret of UCB\n10 actions, 1 million rounds")
    regretWeightsGraph('testFinal5/testSR1.txt')