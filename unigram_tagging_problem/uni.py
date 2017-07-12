
trainFile=open("gene.train1","r")
trainData={}
probablity=[]
string="the cat saw the man" #the test data
totalD=0
totalN=0
totalV=0

def C(count,total):
    P=count/float(total)
    return P

def emission(string,tag):
    global trainData
    if tag=="D":
        e=C(trainData[string][0],totalD)
        tagFound="D"
    elif tag=="N":
        e=C(trainData[string][1],totalN)
        tagFound="N"
    elif tag=="V":
        e=C(trainData[string][2],totalV)
        tagFound="V"
    return e,tagFound


for line in trainFile.readlines():
    if line!="\n":
        line=line[:-1].split()
        if line[1]=="D":
            trainData[line[0]]=trainData.get(line[0],[0,0,0])
            trainData[line[0]][0]=trainData[line[0]][0]+1
        elif line[1]=="N":
            trainData[line[0]]=trainData.get(line[0],[0,0,0])
            trainData[line[0]][1]=trainData[line[0]][1]+1
        elif line[1]=="V":
            trainData[line[0]]=trainData.get(line[0],[0,0,0])
            trainData[line[0]][2]=trainData[line[0]][2]+1
for data in trainData:
    totalD=totalD+trainData[data][0]
    totalN=totalN+trainData[data][1]
    totalV=totalV+trainData[data][2]
for X in string.split():
    print X
    if X not in trainData:
        X="_RARE_"
    for S in ["D","N","V"]:
        probablity.append(emission(X,S))
    print max(probablity)
    del probablity[0:len(probablity)]

