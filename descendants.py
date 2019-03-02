"""
GEDCOM parser design

Create empty dictionaries of individuals and families
Ask user for a file name and open the gedcom file
Read a line
Skip lines until a FAM or INDI tag is found
    Call functions to process those two types
Print descendant chart when all lines are processed

Processing an Individual
Get pointer string
Make dictionary entry for pointer with ref to Person object
Find name tag and identify parts (surname, given names, suffix)
Find FAMS and FAMC tags; store FAM references for later linkage
Skip other lines

Processing a family
Get pointer string
Make dictionary entry for pointer with ref to Family object
Find HUSB WIFE and CHIL tags
    Add included pointer to Family object
    [Not implemented ] Check for matching references in referenced Person object
        Note conflicting info if found.
Skip other lines

Print info from the collect of Person objects
Read in a person number
Print pedigree chart
"""
"""
Megan Nguyen
CPSC 3400 WQ19
Python Program 2 - Family Tree
I had composed the code you wrote based on my understanding of how the features of
the language I am using can be used to implement the algorithm I had chosen to 
solve the problem I am addressing.
"""

#-----------------------------------------------------------------------
class Event():
    #Store date and place of an event
    #Created when a birth/death of an individual or a marriage of a family is processed
    #-------------------------------------------------------------------

    def __init__(self):
        #Initializes a new empty Event object
        self._date = None
        self._place = None

    def addDate(self, date):
        # Stores the string (date) indicating the date of the event
        self._date = date

    def addPlace(self, place):
        # Stores the string (place) indicating the place of the event
        self._place = place


    def _str_(self):
        #return a string of the date and location of an event
        #Return message "No record of date and location" if there's nothing
        if self._date: #Date is available
            dateString = self._date.rstrip('\n')
        else:
            dateString = ''
        if self._place: #Place is available
            placeString = self._place.rstrip('\n')
        else:
            placeString = ''
    
        if dateString == '' and placeString == '':
            return 'No record of date and location'
        else:
            return dateString + ' ' + placeString

#-----------------------------------------------------------------------
class Person():
    # Stores info about a single person
    # Created when an Individual (INDI) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self,ref):
        # Initializes a new Person object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._asSpouse = []  # use a list to handle multiple families
        self._asChild = None
        self._birth = None
        self._death = None
        
                
    def addName(self, nameString):
        # Extracts name parts from nameString and stores them
        names = line[6:].split('/')  #surname is surrounded by slashes
        self._given = names[0].strip()
        self._surname = names[1]
        self._suffix = names[2].strip()

    def addIsSpouse(self, famRef):
        # Adds the string (famRef) indicating family in which this person
        # is a spouse, to list of any other such families
        self._asSpouse += [famRef]
        
    def addIsChild(self, famRef):
        # Stores the string (famRef) indicating family in which this person
        # is a child
        self._asChild = famRef

    def addBirth(self, birth):
        #Stores the Event birth indicating the birth of this person 
        self._birth = birth
    
    def addDeath(self, death):
        #Stores the Event death indicating the death of this person
        self._death = death

    def printDescendants(self, prefix=''):
        # print info for this person and then call method in Family
        print(prefix + self.__str__())
        # recursion stops when self is not a spouse
        for fam in self._asSpouse:
            families[fam].printFamily(self._id,prefix)

    def printAncestors(self, prefix=''):
        #print info for this person and their person's ancestors
        #on both mother and father side in a tree structure with 
        #number indicating their generation away from this person
        gen = len(prefix)       #the number of space in a prefix will tell us how many generations away from the original person
        if self._asChild:        #if this person is a child of any family
            fam = families[self._asChild]
            if fam._husband:    #if this person's parent family has a husband (father)
                persons[fam._husband].printAncestors(prefix + ' ') #recusively call to look for the father ancestor
            print(prefix + str(gen) + ' ' + self.__str__())
            if fam._wife:       #if this person's parent family has a wife (mother)
                persons[fam._wife].printAncestors(prefix + ' ') #recusively call to look for the mother ancestor
        else: #otherwise just print his info
            print(prefix + str(gen) + ' ' + self.__str__())

    def isDescendant (self, personID):
        #test to see if string(personID) exist in this person's family
        #extension of family in later generations and return True if found
        found = False
        if self._id == personID:  #base case: if personId is this person id
            found = True
        else:
            for fam in self._asSpouse: #for each family this person participated in as a spouse
                found = families[fam].findMember(personID) #call findMember function in family to look for personId
                if found: break #as soon as personId is found, break out of loop and return
        return found

    def printCousins(self, n=1):
        #call helper function to return a list of cousin id 
        # within a degree n of relation and output their info
        #print "No cousin" if no cousin is found
        #by default, function will look for first cousin
        solutions = self.get_all_cousins(n) #call helper function
        if solutions: #if solution is not empty
            for cousinId in solutions: #print each cousin info
                print(persons[cousinId].name())
        else: #If no cousin is found, print message for no cousin
            print ('No Cousin')

    def get_all_cousins(self, n):
        #Use recursion and helper function to return a list of 
        #cousin id within a degree n of relation
        if n>0 and n == 1:  #base case, look for the first cousin
            return self.get_1st_cousins()
        else: #look for other degree of cousin
            if self._asChild: #make sure self is a child of a family
                parent_fam = self._asChild #id of a family that self is a child of
                n_cousins = [] #list of cousinId
                if families[parent_fam]._husband: #if the father of self exist
                    dadId = families[parent_fam]._husband #id of self's father
                    n_cousin_parent = persons[dadId].get_all_cousins(n-1) #recusively look for a list of father's cousinId with 1 degree less than child's cousin degree
                    for cousin_parent in n_cousin_parent: #each id of dad cousin
                        if persons[cousin_parent]._asSpouse: #check if dad cousin has a spouse family
	                        for cousin_parent_fam in persons[cousin_parent]._asSpouse: #for every spouse family in dad cousin 
		                        if families[cousin_parent_fam]._children:#check if that family has any children
			                        for cousinId in families[cousin_parent_fam]._children: #those children are n-cousin to self
				                        n_cousins += [cousinId]#add cousinId to a list of cousin
                
                if families[parent_fam]._wife: #if the mother of self exist
                    momId = families[parent_fam]._wife #id of self's mother
                    n_cousin_parent = persons[momId].get_all_cousins(n-1)#recusively look for a list of mother's cousinId with 1 degree less than child's cousin degree
                    for cousin_parent in n_cousin_parent:#each id of mom cousin
                        if persons[cousin_parent]._asSpouse: #check if mom cousin has a spouse family
	                        for cousin_parent_fam in persons[cousin_parent]._asSpouse: #for every spouse family in mom cousin 
		                        if families[cousin_parent_fam]._children:#check if that family has any children
			                        for cousinId in families[cousin_parent_fam]._children: #those children are n-cousin to self
				                        n_cousins += [cousinId]#add cousinId to a list of cousin

                return n_cousins.copy() #return a copy of a list of self n-cousin

    def get_1st_cousins(self):   
        #return a list of first cousin id on both father and mother side
        cousins = []
        if self._asChild: #make sure self is a child of a family
            parent_fam = self._asChild #id of a family that self is a child of
            if families[parent_fam]._husband: #if the father of self exist
                dadId = families[parent_fam]._husband #id of self's father
                if persons[dadId]._asChild: #make sure father is a child of a family
                    grandparent_fam = persons[dadId]._asChild #id of grandparent family
                    if families[grandparent_fam]._children: #if grandparend family has any child
                        for relativeId in families[grandparent_fam]._children: #for every child in grandparend family
                            if relativeId != dadId and persons[relativeId]._asSpouse: #check that the child (relative) is not mom/dad and they has a spouse
                                for relative_fam in persons[relativeId]._asSpouse: #for every spouse family in relative 
                                    if families[relative_fam]._children:#check if that family has any children
                                        for cousinId in families[relative_fam]._children: #those children are 1st cousin to self
                                            cousins += [cousinId]#add cousinId to a list of cousin
            
            if families[parent_fam]._wife: #if the mother of self exist
                momId = families[parent_fam]._wife#id of self's mother
                if persons[momId]._asChild:#make sure mother is a child of a family
                    grandparent_fam = persons[momId]._asChild#id of grandparent family
                    if families[grandparent_fam]._children:#if grandparend family has any child
                        for relativeId in families[grandparent_fam]._children: #for every child in grand parend family
                            if relativeId != momId and persons[relativeId]._asSpouse: #check that the child (relative) is not mom/dad and they has a spouse
                                for relative_fam in persons[relativeId]._asSpouse:#for every spouse family in relative 
                                    if families[relative_fam]._children:#check if that family has any children
                                        for cousinId in families[relative_fam]._children:#those children are 1st cousin to self
                                            cousins += [cousinId]#add cousinId to a list of cousin
        return cousins.copy()

    def __str__(self):
        #return a string of person info including full name and suffix
        #birth and death info, children and spouse id
        if self._asChild: # make sure value is not None
            childString = ' asChild: ' + self._asChild
        else: childString = ''
        if self._asSpouse != []: # make sure _asSpouse list is not empty
            spouseString = ' asSpouse: ' + str(self._asSpouse)
        else: spouseString = ''

        if self._birth: #make sure birth info is available
            birthString = ' n: ' + self._birth._str_()
        else: birthString = ''
        if self._death: #make sure death info is available
            deathString = ' d: ' + self._death._str_()
        else: deathString = ''

        return self._given + ' ' + self._surname.upper()\
               + ' ' + self._suffix +birthString + deathString + childString + spouseString

    def name(self):
        #return a string of person full name and suffix
        return self._given + ' ' + self._surname.upper()\
               + ' ' + self._suffix  

 
#-----------------------------------------------------------------------
                    
class Family():
    # Stores info about a family
    # Created when an Family (FAM) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self, ref):
        # Initializes a new Family object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._husband = None
        self._wife = None
        self._children = []
        self._marriage = None
        self._divorce = None

    def addHusband(self, personRef):
        # Stores the string (personRef) indicating the husband in this family
        self._husband = personRef

    def addWife(self, personRef):
        # Stores the string (personRef) indicating the wife in this family
        self._wife = personRef

    def addChild(self, personRef):
        # Adds the string (personRef) indicating a new child to the list
        self._children += [personRef]
    
    def addMarriage(self, marriage):
        #Add event (marriage) indicating the marriage of this family
        self._marriage = marriage

    def addDivorce(self, divorce):
        #Add event (divorce) indicating the divorce of this family
        self._divorce = divorce

    def printFamily(self, firstSpouse, prefix):
        # Used by printDecendants in Person to print spouse
        # and recursively invole printDescendants on children
        if prefix != '': prefix = prefix[:-2]+'  '
        if self._husband == firstSpouse:
            if self._wife:  # make sure value is not None
                print(prefix+ '+' +str(persons[self._wife]))
        else:
            if self._husband:  # make sure value is not None
                print(prefix+ '+' +str(persons[self._husband]))
        for child in self._children:
             persons[child].printDescendants(prefix+'|--')

    def findMember(self, personID):
        #Helper function of isDescendants() to verify if 
        #a given personId belong to this family or its
        #extended family in later generations and return 
        #result of search
        found = False #initially search is false
        if self._children: #make sure that this family has children
            for child in self._children: #look through each children in the family
                if personID == child:
                    found = True    #search is true if child id = personId
                else:   #otherwise look for personId in child's children
                    found = persons[child].isDescendant(personID)
                if found: break #as soon as personId is found, return result for search
        return found

    def __str__(self):
        #Return a string of family info including husband and wife id
        #Their marriage and divorce record (if any), and a list of children id
        if self._husband: # make sure value is not None
            husbString = ' Husband: ' + self._husband
        else: husbString = ''
        if self._wife: # make sure value is not None
            wifeString = ' Wife: ' + self._wife
        else: wifeString = ''
        if self._children != []: childrenString = ' Children: ' + str(self._children)
        else: childrenString = ''
        if self._marriage: #make sure marriage event is not None
            marriageString = ' Married: ' + self._marriage._str_()
        else: marriageString = ''
        if self._divorce: #make sure divorce even is not None
            divorceString = ' Divorced: ' + self._divorce._str_()
        else: divorceString = ''
        return husbString + wifeString + marriageString + divorceString + childrenString


#-----------------------------------------------------------------------
 
def getPointer(line):
    # A helper function used in multiple places in the next two functions
    # Depends on the syntax of pointers in certain GEDCOM elements
    # Returns the string of the pointer without surrounding '@'s or trailing
    return line[8:].split('@')[0]
        
def processPerson(newPerson):
    #Read from a file line and line and process 
    #a person info including name, spouse family,
    #parent family, birth and death record
    global line
    line = f.readline()
    while line[0] != '0': # process all lines until next 0-level
        tag = line[2:6]  # substring where tags are found in 0-level elements
        tag = tag.rstrip('\n')
        tag = tag.strip(' ')
        if tag == 'NAME':
            newPerson.addName(line[7:])
        elif tag == 'FAMS':
            newPerson.addIsSpouse(getPointer(line))
        elif tag == 'FAMC':
            newPerson.addIsChild(getPointer(line))
        
        #process Event starts here:
        if tag == 'BIRT':
            birth = Event() #create an event for Birth
            line = f.readline() #go to next line to read record for Birth
            while line[0] == '2': #process until level of information change (0: person, 1: birth, death, name, 2: date and location of event)
                detail = line[2:6] #substring for tag
                if detail == 'DATE':
                    birth.addDate(line[7:])
                elif detail == 'PLAC':
                    birth.addPlace(line[7:])
                line = f.readline() #read the next line
            newPerson.addBirth(birth) #add birth record to person record

        elif tag == 'DEAT': 
            death = Event() #create an event for Death
            line = f.readline() #go to next line to read record for Death
            while line[0] == '2': #process until level of information change
                detail = line[2:6] #substring for tag
                if detail == 'DATE':
                    death.addDate(line[7:])
                elif detail == 'PLAC':
                    death.addPlace(line[7:])
                line = f.readline() #read the next line
            newPerson.addDeath(death) #add death record to person record
        else: #if tag is neither BIRTH or DEAT, then read the next line,
            line = f.readline() #this will prevent event handling from reading 1 extra line

def processFamily(newFamily):
    #Read from a file line by line and process a
    #family info including husband,wife, and children id
    #and marriage record
    global line
    line = f.readline()
    while line[0] != '0':  # process all lines until next 0-level
        tag = line[2:6] #substring for tag
        tag = tag.rstrip('\n') #strip newline character at the end in the case of DIV
        tag = tag.strip(' ') #strip space

        if tag == 'HUSB':
            newFamily.addHusband(getPointer(line))
        elif tag == 'WIFE':
            newFamily.addWife(getPointer(line))
        elif tag == 'CHIL':
            newFamily.addChild(getPointer(line))
        
        #Marriage and divorce event handling starts here
        if tag == 'MARR':
            marriage = Event() #Create an event for Marriage
            line = f.readline() #Go to the next line to read record for marriage
            while line[0] == '2': #Process until level of information change
                detail = line[2:6] #substring for tag
                if detail == 'DATE':
                    marriage.addDate(line[7:])
                elif detail == 'PLAC':
                    marriage.addPlace(line[7:])
                line = f.readline() #read the next line
            newFamily.addMarriage(marriage)#add marriage record to family record
        
        elif tag == 'DIV':
            divorce = Event() #Create an event for Divorce
            line = f.readline() #Go to the next line to read record for divorce
            while line[0] == '2': #Process until level of information change
                detail = line[2:6] #substring for tag
                if detail == 'DATE':
                    divorce.addDate(line[7:])
                elif detail == 'PLAC':
                    divorce.addPlace(line[7:])
                line = f.readline() #read the next line
            newFamily.addDivorce(divorce)#add divorce record to family record
        
        else: #if tag is neither MARR or DIV, then read the next line
            line = f.readline() #this will prevent event handling from reading 1 extra line


## Main program starts here

persons = {}  # to save references to all of the Person objects
families = {} # to save references to all of the Family objects

filename = "Kennedy.ged"  # Set a default name for the file to be processed

### Uncomment the next line to make the program interactive
filename = input("Type the name of the GEDCOM file:")

f = open (filename)
line = f.readline()
while line != '':  # end loop when file is empty
    fields = line.strip().split(' ')
    # print(fields)
    if line[0] == '0' and len(fields) > 2:
        # print(fields)
        if (fields[2] == "INDI"): 
            ref = fields[1].strip('@')
            persons[ref] = Person(ref)  ## store ref to new Person
            processPerson(persons[ref])
        elif (fields[2] == "FAM"):
            ref = fields[1].strip('@')
            families[ref] = Family(ref) ## store ref to new Family
            processFamily(families[ref])      
        else:    # 0-level line, but F11ot of interest -- skip it
            line = f.readline()
    else:    # skip lines until next F11andidate 0-level line
        line = f.readline()

import GEDtest
GEDtest.runtests(persons,families)