import HW2_partA
import re



def tokenize(s):
	retValue = re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z0-9_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)
	return retValue


def arrtoken(a):
	inbracket = 0
	temparr = []
	newarr = []
	openposition = []
	closeposition = []
	stoken = tokenize(a)

	# replace item in closed arrays by _ 
	# traverse through later and remove them 
	for i,v in enumerate(stoken):

		if v == '{':
			openposition.append(i)
			inbracket +=1
			temparr = []
			stoken[i] = '_'

		if v == '}':
			closeposition.append(i)
			inbracket -= 1
			newarr.append(temparr)
			stoken[i] = '_'

		if inbracket == 1:
			if v != '{' and v != '}':
				temparr.append(v)
				stoken[i] = '_'


	# append built array to open bracket position
	for pos, item in enumerate(openposition):
		stoken[item] = newarr[pos]

	#then remove leftover key
	while '_' in stoken:
		stoken.remove('_')

	return stoken

#<init> <incr> <final> <code array> 
#push iteration on the stak, then call interpreter to run another function
def doFor():
	opFunction = HW2_partA.opPop()
	opFinal = int(HW2_partA.opPop())
	opIncrement = HW2_partA.opPop()
	opInitial = HW2_partA.opPop()

	i = opInitial
	while i < opFinal + 1:
		HW2_partA.opPush(i)
		interpreter(opFunction)
		i += opIncrement

#convert to array, then put current array value onstack, then call code array 
def doForAll():
	opFunction = HW2_partA.opPop()
	opArr = HW2_partA.opPop()
	for i in opArr:
		HW2_partA.opPush(int(i))
		interpreter(opFunction)


def arrMaker(s):
	s = HW2_partA.cleanOuterBracket(s)
	s = s.split(" ")
	return s



def interpreter(ops):
	for i in ops:


		if isinstance(i, list):
			HW2_partA.opPush(i)
		elif i.isdigit():
			HW2_partA.opPush(int(i))
		elif i[0] == "/":
			HW2_partA.opPush(i)
		elif i.isalpha() and HW2_partA.lookup(i):
			HW2_partA.opPush(HW2_partA.lookup(i))
		elif i == "def":
			HW2_partA.psDef()
		elif i == "add":
			HW2_partA.add()
		elif i == "sub":
			HW2_partA.sub()
		elif i == "mul":
			HW2_partA.mul()
		elif i == "div":
			HW2_partA.div()
		elif i == "mod":
			HW2_partA.mod()
		elif i == "get":
			HW2_partA.get()
		elif i == "dup":
			HW2_partA.dup()
		elif i == "exch":
			HW2_partA.exch()
		elif i == "clear":
			HW2_partA.clear()
		elif i == "stack":
			HW2_partA.stack()
		elif i == "copy":
			HW2_partA.copy()
		elif i == "roll":
			HW2_partA.roll()
		elif i == "dict":
			HW2_partA.dict()
		elif i == "begin":
			HW2_partA.begin()
		elif i == "end":
			HW2_partA.end()
		elif i == "define": # needs to modify original function
			HW2_partA.define()
		elif i == "lookup": # needs to modify original function   
			HW2_partA.lookup()
		elif i[0] == "[": #handle post script array 
			HW2_partA.opPush(arrMaker(i))
		elif i == "forall": 
			doForAll()
		elif i == "length": 
			HW2_partA.length()
		elif i == "get":
			HW2_partA.get()
		elif i == "for": # 
			doFor()
		
	


def testFor():
	s = "1 1 5 {2 mul} for"
	interpreter(arrtoken(s))
	testsol = [2, 4, 6, 8, 10]

	for i in reversed(testsol):
		if HW2_partA.opPop() == i :
			return True
	return False

def testForAll():
	s = "[1 2 3 4] {2 mul} forall"
	interpreter(arrtoken(s))
	testsol = [2, 4, 6, 8]

	for i in reversed(testsol):
		if HW2_partA.opPop() == i :
			return True
	return False

def testInterpreter():
	s = "/x 1 2 add 3 add 2 mul 3 div def"
	interpreter(arrtoken(s))
	if int(HW2_partA.lookup('x')) == 4:
		return True
	else:
		return False


def partBTest():
	testFor()
	testForAll()
	testInterpreter()


partBTest()