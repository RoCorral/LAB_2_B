"""
@author Rocorral
ID: 80416750
Instructor: David Aguirre
TA: Saha, Manoj Pravakar
Assignment:Lab 2-B - LL,dic,bub,merge
Last Modification: 10/18/2018
Program Purpose: The purpose of this program is to practice and note the
difference in computation times between inserting into a linked list
iterativly and the inserting in to a hashtable datastructure like a 
dictionary. we are provided with a large file and must process the data.
obviously performing iterative computations on a lists with vast amounts
of data can take too much time.
"""

import time

'''
@readfileLL
Takes in a file name as a string and opens the corresponding file to process
each line is parsed into an array those arrays without a user password
pair(length of anything other than 2) are discarded. each password iterated 
through is checked against the nodes in the existing list for duplicates if it is found the 
corresponding node count is increasded by one. if not the password is inserted into
 a linked list as the new head and with head.next pointing to the old head.
'''
def readfileLL(file):
	pws = open(file,'r+',encoding="UTF-8")
	head = Node("",-1,None)
	for line in pws:
		a=line.split()
		if len(a) is not 2:
			pass
			#print("user: ",a[0]," no password")#sort out no passwords
		else:
			temp = head
			found = False
			while temp is not None and found is False:
				if temp.password == a[1]: #compare node password to password parsed from file
					temp.count +=1
					found = True
				if temp.next is None and found is False:
					head=Node(a[1],1,head)
				temp=temp.next	
	return head

'''
@readfileDic
Takes in a file name string and opens the corresponding file to process.
each line is parsed into an array those arrays without a user password
pair(length of anything other than 2) are discarded. passwords are inserted into 
a dictionary as the key and a node as the value. each sucessive password is checked 
against the keys if the key already exists then the count of the node in the value 
is increased by 1. If it does not then it is inserted into the dic and also linked
as the new head with a head.next pointing to the old head of the list for sorting later.
'''

def readfileDic(file):
	pws = open(file,'r+',encoding="UTF-8")
	pwList = {}
	head =None
	for line in pws:
		a=line.split()
		if len(a) is not 2:
			pass
			#print("user: ",a[0]," no password")
		else:#check if the password exists as a key in our dictionary
			if a[1] in pwList: 
				pwList[a[1]].count += 1 #if it does increment the count param of the  Node(key) by one
			else:#create a new node add it to the linked list and add the password to the dictionary as a key and the node as a value
				head=Node(a[1],1,head)
				pwList[head.password] = head
	return head

'''
@bSortLinkList
Takes in the head of a linked list and bubble sorts in acending order the swapping is done by trading data not relinking.
'''
def bSortLinkList(pwList):
	sortd = False
	while sortd is False:
		swap = pwList
		swcount =0 #tracks the number of swaps in a pass
		while swap.next is not None:
			if swap.next.count > swap.count:
				swcount+=1
				tCount = swap.count
				tPw = swap.password
				swap.count = swap.next.count
				swap.password = swap.next.password
				swap.next.count = tCount
				swap.next.password = tPw
			swap =swap.next
		if swcount ==0:
			sortd=True
	return pwList
'''
@mergeSortLinked
takes in the head of a linked list and passes the split list recursivly for sorting
'''
def mergeSortLinked(pwList):
	if pwList.next is None or pwList is None:
		return pwList
	listA, listB =	splitList(pwList)
	a=mergeSortLinked(listA)
	b=mergeSortLinked(listB)
	return mergeTheLists(a,b)

'''
@splitList
called@mergeSortLinked
Takes in a Linked List head and seperates the list into 2 halves that are later passed to mergeTheLists
'''
def splitList(splitThis):
	if splitThis is None or splitThis.next is None:
		splitA = splitThis 
		splitB = None
		return  splitA, splitB
	else:
		mid = splitThis #mid iterates to middle of list
		runner = splitThis.next #runner itterates to end
		while runner.next is not None:#ensures the runner does not excede the list length
			runner =runner.next
			if runner.next is not None:
				mid = mid.next
				runner = runner.next
	splitA = splitThis#first half
	splitB = mid.next#second half
	mid.next = None#breaks link between them
	return splitA, splitB

'''
@mergeTheLists
called @ mergeSortLinked
Takes in Linked List heads from split def and combines them in decending order
'''
def mergeTheLists(leftHalf, rightHalf):
    temp = Node("",-1,None)#empty node to start from
    curr = temp
    while leftHalf and rightHalf:
        if leftHalf.count < rightHalf.count:#merges list in decending order
            curr.next = rightHalf
            rightHalf = rightHalf.next
        else:
            curr.next = leftHalf
            leftHalf = leftHalf.next
        curr = curr.next
    if leftHalf == None:
        curr.next = rightHalf
    elif rightHalf == None:
        curr.next = leftHalf
    return temp.next #returns list after empty node

'''
@printTop20
Takes in a Linked List head and prints the first 20 items
'''
def printTop20(sortedPWlist):
	temp = sortedPWlist
	top20 =0
	print("\n--------The top 20 are--------\n")
	while temp is not None  and top20 <20:
		print(temp.password,temp.count)
		top20+=1
		temp=temp.next
	print("\n------------------------------\n")


'''
@timeAnalyze 
this def simply records times befor and after the call to insertion
and sorting methods so that data can be gathered for the report.
Usefull information is printed from the recordings.
'''
def timeAnalyz(file,itemsinFile):
	if itemsinFile > 30000:#preforms merge sort on those lists greater than 30000 like 100k 1m and 10m
		rfDLTSt = time.time()
		DicL=readfileDic(file)
		rfDLTSp = time.time()

		msLLTSt = time.time()
		SortedDicL =mergeSortLinked(DicL)
		msLLTSp = time.time()

		
		rD = rfDLTSp -rfDLTSt
		mergeS = msLLTSp -msLLTSt
		print("\nThis file with",itemsinFile, "items was to large to run a bubble sort and LL insertion with traversal checks for duplicates in a reasonable time.\nBut other Data points where gathered.\nInsertion into a dictionary took",int(rD*1000)," milliseconds. \nMerge Sorting the resulting list took", int(mergeS*1000),"milliseconds\n")
		printTop20(SortedDicL)	
	else:#performs all insertions and sorting algorythems on linked lis <= 30000 like 20k and 10k
		rfLLTSt = time.time()
		LL = readfileLL(file)
		rfLLTSp = time.time()

		bsLLTSt = time.time()
		SortedLL = bSortLinkList(LL)
		bsLLTSp = time.time()


		rfDLTSt = time.time()
		DicL=readfileDic(file)
		rfDLTSp = time.time()

		msLLTSt = time.time()
		SortedDicL =mergeSortLinked(DicL)
		msLLTSp = time.time()


		rLL = rfLLTSp -rfLLTSt
		rD = rfDLTSp -rfDLTSt
		bubS = bsLLTSp -bsLLTSt
		mergeS = msLLTSp -msLLTSt

		print("\nIn a file with",itemsinFile, "items \nReading the file to a linked list took",int(rLL*1000)," milliseconds. \nInto a dictionary took",int(rD*1000)," milliseconds. \nBubble sorting the resulting list took", int(bubS*1000),"milliseconds. \nMerge Sorting the resulting list took", int(mergeS*1000),"milliseconds\n")
		printTop20(SortedDicL)


#Node Class provided in assignment
class Node(object):
	password = ""
	count = -1
	next = None

	def __init__(self, password, count,next):
		self.password = password
		self.count = count
		self.next = next


#---------Main----------
timeAnalyz("10000-combos.txt",10000)
timeAnalyz("20-thousand-combos.txt",20000)
timeAnalyz("30-thousand-combos.txt",30000)
timeAnalyz("100-thousand-combos.txt",100000) 
timeAnalyz("1-million-combos.txt",1000000)
#timeAnalyz("10-million-combos.txt",10000000)








