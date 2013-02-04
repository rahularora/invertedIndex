import urllib
import re
import matplotlib.pyplot as plt
import math
import sys

tokens = {}
tokenSet = set()
occurrences = 0.0
    
def readFile(fileName):
    """Reads a file and generate a string"""
    fileurl = "http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/file"+fileName+".txt"
    try:
        sock = urllib.urlopen(fileurl)
        fileContent = sock.read()
        sock.close()
    except:
        print "File at " + fileurl + " not found"
    
    return fileContent
    
    
def generateToken(fileContent,fileName,flag):
    """ Reads a file and add to tokens data-structure 
        tokens is of the form { word, {filename, {p1,p2,p3,p4} }}
    """
 
    fileContent = fileContent.lower()
    tokenList = fileContent.split()
    i=1
    
    for word in tokenList:
        if re.search('^[a-zA-Z]+', word):
            if(flag):
                files = {}
                positions = set()
                if word in tokens:
                    files = tokens[word]    
                
                    if fileName in files:         
                        positions = files[fileName]
            
                positions.add(i)
                files[fileName]=positions 
                tokens[word] = files
                i = i+1        
            else:
                tokenSet.add(word)
                
    return
    
                
def traverseDataSet():
    """ Helper function to traverse all files"""
    for i in range(0,40):
        if(i<10):
            fileName = "0" + str(i)
        else:
            fileName =  str(i)

        fileContent = readFile(fileName)
        generateToken(fileContent, fileName,1)
        
    return


def displayWebData():
    """ Display tokens data-structure as stated by Prof
        for e.g. 7 ability 11:1 14:1 17:1 19:1 38:1 [5]
        <<token_no>> <<token>> <<filename>>:<<No of occurrences>> <<filename>>:<<No of occurrences>> <<filename>>:<<No of occurrences>>
    """
    i = 1
    for key in sorted(tokens.iterkeys()):
        print "%d %s" %(i,key),
        tempDict = tokens[key]
        count = 0
        for key1 in sorted(tempDict.iterkeys()):
            print " %s : %s " %(key1, len(tempDict[key1])),
            count = count + 1
        print "[[%s]]" %count
        i = i+1 
    
    return
 
def calculateIDF(word):
    """ Calculate idf using the word """
    if word in tokens:
        tempDict = tokens[word]
        df = 0
        for fileName in tempDict:
            df = df + 1
    
    return math.log10(40/df)
            
            
def calculateQueryWeight(queryList):
    
    temp = {}
    for word in queryList:
        if word in temp:
            temp[word] = temp[word] + 1
        else:
            temp[word] = 1
    # temp = t(f,q)
    
    for word in temp:
        temp[word] = 1 + math.log10(temp[word]) # temp = w(t,q)
        idf = calculateIDF(word)
        temp[word] = temp[word] * idf
        
    #Now temp = weight = w(t,q) * idf
        
    return temp

def calculateDocWeight(queryWeight,fileName):
    temp = {}
    weight = {}
    normalize = 0
    for word in queryWeight:
        temp[word] = len(tokens[word][fileName])
    
        if temp[word]:
            temp[word] = 1 + math.log10(temp[word]) # temp = w(t,q)
        else:
            temp[word] = 0 
        weight[word] = temp[word]    
        normalize = normalize + math.pow(temp[word], 2)
    
    normalize = math.sqrt(normalize)
    
    sumProduct = 0
    for word in queryWeight:
        temp[word] = temp[word]/normalize
        temp[word] = temp[word] * queryWeight[word]
        sumProduct = sumProduct + temp[word]
    
    return sumProduct
        

def testOutput(totalFiles,queryList,flag):
    
    if flag:
        queryWeight = calculateQueryWeight(queryList) 
#        print queryWeight
        print "The search query is located at file(s):"
        cosineScore = {}
        for fileName in totalFiles:
            docWeight = calculateDocWeight(queryWeight,fileName) 
            cosineScore[fileName] = docWeight

        for w in sorted(cosineScore, key=cosineScore.get, reverse=True):
            print "FileName : " + w + " tf.idf score : "+ str(cosineScore[w])
    
    else:
        word = queryList[0]
        tempDict = tokens[word]
        idf=calculateIDF(word)
        for fileName in totalFiles:
            for pos in tempDict[fileName]:
                tf = len(tempDict[fileName])
                print str(tf) + " , ",
                print str(idf) + " , ",
                tfidf = (1 + math.log10(tf))*idf
                print str(tfidf)
            
                print fileName + " , " + str(pos)
                
                fileContent = readFile(fileName)
                tokenList = fileContent.split()
                tknList = []
                for tkn in tokenList:
                    if re.search('^[a-zA-Z]+', tkn):
                        tknList.append(tkn)
                        
                for i in range(pos-6,pos+5):
                    print str(tknList[i]) + " ",
                print "\n"
    
    return

def diffFiles(queryList):
    
    fileSet = set()
    for i in range(0,40):
        if(i<10):
            fileName = "0" + str(i)
        else:
            fileName =  str(i)
        fileSet.add(fileName)
            
    for word in queryList:
        if word in tokens:
            tempDict = tokens[word]
            tempSet = set()
            for fileName in tempDict:
                tempSet.add(fileName)
                
        else:
            return set()
        
        fileSet = fileSet.intersection(tempSet)        
        
    return fileSet

def searchTerm(queryList,flag):
    stopList = Q3()
    
    finalQueryList = []
    
    if flag:
        for word in queryList:
            if not(word in stopList):
                finalQueryList.append(word)
        queryList = finalQueryList 
        
    #else it is a single search query
        
    totalFiles = diffFiles(queryList)
    if not totalFiles:
        print "The search query is not found in the given documents."
        return
    
    testOutput(totalFiles,queryList,flag)
    return

def generateWordFreq(flag):
    totalWordOccurrences = 0
    
    #Total occurrences of a word in all files
    #Form  { word, total occurrences}
    wordFreq = {} 
    
    if(flag):
        #Total files in which a word can be found
        #Form  { word, total files}
        fileFreq = {}
    
    for key in tokens:
        count = 0
        filecount = 0
        tempDict = tokens[key]
        for key1 in tempDict:
            count = count + len(tempDict[key1])
            filecount = filecount + 1
        wordFreq[key] = count
        if(flag):
            fileFreq[key] = filecount
        totalWordOccurrences = totalWordOccurrences + count
        
    if(flag):
        return (fileFreq)
    else:
        return (wordFreq,totalWordOccurrences)
    
def generateWordRank():
    wordFreq,totalWordOccurrences = generateWordFreq(0)
    
    wordRank = []
    for key in wordFreq:
        wordRank.append(wordFreq[key])
    
    wordRank.sort()
    
    rank = len(wordRank)
    logRank = []
    logFreq = []
    for freq in wordRank:
        logRank.append(math.log10(rank))
        logFreq.append(math.log10(freq))
        rank = rank-1
    
    return (logRank,logFreq)

def plotZipfLaw():
    logRank,logFreq = generateWordRank()
    plt.plot(logRank, logFreq, 'ro')
    plt.xlabel('log x : x is rank of a word in the frequency table')
    plt.ylabel('log y : y  is the total number of the word occurrences')
    plt.show()
    
def Q1b():
    wordFreq,totalWordOccurrences = generateWordFreq(0)
    count,i = 0,0
    flags = [0,0,0,0]
    
    for key, value in sorted(wordFreq.iteritems(), key=lambda (k,v): (v,k)):
        #print "%s: %s" % (key, value)
        count = count + value
        #print "%s  %s" %(i,count)
        if(count>totalWordOccurrences/4 and not flags[0]):
            flags[0] = i
        elif(count>totalWordOccurrences/2 and not flags[1]):
            flags[1] = i
        elif(count>3*totalWordOccurrences/4 and not flags[2]):
            flags[2] = i
        elif(count==totalWordOccurrences and not flags[3]):
            flags[3] = i+1
        i = i + 1
        
    print "1/4 : " + str(flags[3]-flags[2])
    print "1/2 : " + str(flags[2]-flags[1])
    print "3/4 : " + str(flags[1]-flags[0])
    
    
def Q2helper(num1,num2):
    
    global tokenSet
    global occurrences
    for i in range(num1,num2):
        if(i<10):
            fileName = "0" + str(i)
        else:
            fileName =  str(i)

        fileContent = readFile(fileName)
        generateToken(fileContent, fileName,0)
        occurrences += Q2helper1(fileContent)

    return (occurrences,len(tokenSet))
    
def Q2helper1(fileContent):
    count = 0
    fileContent = fileContent.lower()
    tokenList = fileContent.split()
    for word in tokenList:
        if re.search('^[a-zA-Z]+', word):
            count = count + 1
            
    return count
    
def Q2():
    
    yAxis,xAxis = [],[]
    
    for i in range(0,4):
        x,y = Q2helper(10*(i),10*(i+1))
        
        xAxis.append(math.log10(x))
        yAxis.append(math.log10(y))
    
    print xAxis
    print yAxis
   
    plt.plot(xAxis, yAxis, "ro")
    plt.xlabel('log x : x is Text size')
    plt.ylabel('log y : y is number of distinct vocabulary elements present in the text')
    plt.show()
    
    return

def Q3():
    fileFreq = generateWordFreq(1)
    
    stopList = set()
    for key in fileFreq:
        if fileFreq[key] > 26:
            stopList.add(key)
        
    return stopList
    #set(['and', 'is', 'it', 'an', 'as', 'are', 'have', 'in', 'their', 'said', 
    #'from', 'for', 'also', 'by', 'to', 'other', 'which', 'new', 'has', 'was', 
    #'more', 'be', 'we', 'that', 'but', 'they', 'not', 'with', 'than', 'a', 'on', 
    #'these', 'of', 'could', 'this', 'so', 'can', 'at', 'the', 'or', 'first']) 
        
def main():

    traverseDataSet()
     
    if len(sys.argv) == 1:
        while(1):
            searchQuery = raw_input("\nEnter a search query : ")
            searchQuery = searchQuery.lower()
            if re.match("zzz",searchQuery):
                print "Found ZZZ. Exiting"
                exit(0)
        
            searchQueryList = searchQuery.split()
            if len(searchQueryList) > 1:
                searchTerm(searchQueryList,1)
            else:
                searchTerm(searchQueryList,0)
    else:
        for argv in sys.argv:
            if re.match("displaywebdata",argv):
                displayWebData()
            elif re.match("A1a",argv):
                plotZipfLaw()
            elif re.match("A1b",argv):
                Q1b() 
            elif re.match("A2",argv):
                Q2()
            elif re.match("A3",argv):
                stopList = Q3()
                for key in stopList:
                    print key + ",",
            elif re.match("B1a",argv):
                fileFreq = generateWordFreq(1)
                for key in sorted(fileFreq.iterkeys()):
                    print "%s %d" %(key,fileFreq[key])
                
                
if __name__ == "__main__":
    main()