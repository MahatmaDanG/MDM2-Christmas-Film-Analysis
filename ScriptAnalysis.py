# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:53:13 2023

@author: Mahatma
"""
import matplotlib.pyplot as plt


def FrequencySort(Words,Counts):
    """
    IN:
        Two lists of the same length, n
    OUT:
        One list of length n where each list item is a combination of the input
        items.
    
    Takes a string of unique words along with the frequency to return a list 
    sorted by word frequency.
    
    Uses zip to join two lists and .sort to order them about reverse order
    """
    Paired = list(zip(Words,Counts))
    Paired.sort(key = lambda x: x[1],reverse = True)
    return(Paired)
    
    


def WordCounts(formatted):
    """
    IN:
        A string formatted to have only the required text but can include 
        punctuation and \n's
    OUT:
        The list returned by the FrequencySort function.
    
    Takes the given string, isolates just the letter values to determine the 
    frequency of each word. DOES NOT CHECK FOR REAL WORDS.
    """
    # Formats String
    script = formatted.replace("\n","") # Formats a string to remove \n as the n still functions as a letter, causing problems.
    script += " "
    
    # Seperate the string into words.
    tempword = []
    words = []
    for index,item in enumerate(str(script)):
        if (64 < ord(item.upper()) < 91) or item == "'": # Checks for letter using the ASCII values of uppercase.
            tempword.append(item.upper())
        elif len(tempword) > 0:
            # if len(tempword) == 1 and tempword != "A" and tempword != "I":
            #     print(tempword,index)
            words.append("".join(tempword))
            tempword = []
    TotWords = len(words)
    # Counts the frequency of each word in the string
    unique = set(words)
    counts = []
    for loop in range(len(unique)):
        counts.append(0)
    for word in words:
        for index,item in enumerate(unique):
            if item == word:
                counts[index] += 1
                break
    
    
    Joined = FrequencySort(unique,counts)
    #print(Joined[:10])
    return(Joined,TotWords)
    
                
            

def Analyse(formatted):
    script = formatted.replace("\n","")
    sentence = ""
    divided = []
    for lett in script:
        sentence += lett 
        if lett == "?" or lett == "." or lett == "!":
            divided.append(str(sentence))
            sentence = ""
            break
         
    percent = len(divided)
    y_axis = []
    x_axis = []
    aggreg = 0
    for index,item in enumerate(divided):
        words = item.split(" ")
        ignore = 0
        for item in words:
            if item == "":
                ignore += 1
        print(words,ignore)
        aggreg += len(words)-ignore
        y_axis.append(aggreg)
        x_axis.append(index)#*100/percent)
    return(x_axis,y_axis)#,divided)  
    # lengths = []
    # maximum = 0
    # sums = []
    # for item in divided:
    #     itlen = len(item)
    #     lengths.append(itlen)
    #     if itlen >  maximum:
    #         maximum = itlen
    # for x in range (0,maximum):
    #     sums.append(0)
    #     x_axis.append(x)
    # for item in lengths:
    #     sums[item] += 1
    # return(x_axis,sums)
    
def CallAnalyse(script,axis1):
    formatted,name = script[0],script[1]
    x1_axis,y1_axis = Analyse(formatted)
    #print(strF2)
    x1_axis,y1_axis = Analyse(formatted)
        
    axis1.plot(x1_axis, y1_axis,"r-", marker="x",label = name)

    return(axis1)
    
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i]//2, y[i], ha = 'center',)
        
def StemPlot(Sorted):
    index = 10
    Equal = True
    while Equal == True:
        print(Sorted[index],Sorted[index-1])
        if Sorted[index][1] == Sorted[index-1][1]:
            index += 1
        else:
            Equal = False
            
    x_axis,y_axis = [],[]
    for item in Sorted[:index]:
        x_axis.append(item[0])
        y_axis.append(item[1])
        
    axislabels = {'fontstyle': 'italic'}
    datalabels = {'fontsize' : 0.2}
    plt.bar(x_axis, y_axis, color = "r")
    plt.title('Most Common Words in Home Alone',fontdict = axislabels,pad = 15)
    plt.ylabel('Frequency',fontdict = axislabels)
    plt.xlabel('Word',fontdict = axislabels)
    addlabels(x_axis,y_axis)
    #plt.box(True)
    #plt.legend()
    # fig, ax = plt.subplots()
    # ax.axis("off")
    plt.show()
    
with open("Document.txt","rt") as F:
    strF = F.read()
F.close()
with open("Arthur Christmas.txt","rt") as F2:
    strF2 = F2.read()
F2.close()
with open("Grinch.txt","rt") as F3:
    strF3 = F3.read()
F3.close()

shortened = []
add = True
caps = ""
FirstCap = False
for letter in strF:
    if (64 < ord(letter) < 91 or letter == "?")  and FirstCap == False and add == True:
        cap = letter
        FirstCap = True
    elif FirstCap == True and (64 < ord(letter) < 91 or ord(letter) == 58):
        cap = ""
        if ord(letter) == 58:
            FirstCap = False
    else:
        if FirstCap == True: 
            shortened.append(cap) 
            FirstCap = False
        if letter == "(":
            add = False
        
        if add == True:
            shortened.append(letter)
        if letter == ")":
            add = True
#print(strF)
formatted = "".join(str(e) for e in shortened)
scripts = [[formatted,"Home Alone"],[strF2,"Arthur Christmas"],[strF3,"The Grinch"]]


axis1 = plt.axes()
for item in scripts:
    axis1 = CallAnalyse(item,axis1)
plt.title('Sentence Length distributions for different Christmas Films ')
plt.ylabel('Sentence Length')
plt.xlabel('Sentence no. (as a % of all sentences)')
plt.legend()
plt.show()
#test = ("banana banana banana \n apple apple orange")
#Frequencies = WordCounts(formatted)
#print(Frequencies[:12])
#StemPlot(Frequencies)
# Frequencies1,Tot1 = WordCounts(formatted)
# Frequencies2,Tot2 = WordCounts(strF2)
# Frequencies3,Tot3= WordCounts(strF3)
# for item in Frequencies1:
#     if item[0] == "CHRISTMAS":
#             print(item[0],100*item[1]/Tot1)
#             break
# for item in Frequencies2:
#     if item[0] == "CHRISTMAS":
#             print(item[0],100*item[1]/Tot2)
#             break
# for item in Frequencies3:
#     if item[0] == "CHRISTMAS":
#             print(item[0],100*item[1]/Tot3)
#             print(Tot3)
#             break
#print(Frequencies[:12])
#StemPlot(Frequencies)
# for item in Frequencies:
#     if len(item[0]) == 1:
#         print(item)
#WordCounts(strF2)
#WordCounts(strF3)




# greatest = [0,0]
# for index,item in enumerate(y3_axis):
#     if item >= greatest[0]:
#         greatest = [item,index]
# print(greatest)
# print(divided3[greatest[1]])

# print(strF3)
    

