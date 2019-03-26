#Submitted by
#Prerna Singh(50249100)
#Shivani Thakur(50249137)

import itertools

#loads the dataset from the given text file and generates the gene data
def template1_input(rules, query):
    template1_param3 = set()
    template1 = query.replace('"','').strip()
    template1 = template1.split("[")
    template1_part1 = template1[0].split(",")
    template1_param1 = template1_part1[0].upper()
    template1_param2 = template1_part1[1].strip().upper()
    template1_part2 = template1[1].split(",")
    length = len(template1_part2)
    for i in range(0,length):
        if i==length-1:
            val = template1_part2[i].strip()
            template1_param3.add(val[1:len(val)-2].upper())
        else:
            val = template1_part2[i]
            template1_param3.add(val[1:len(val)-1].upper())
    return template1_result(rules, template1_param1, template1_param2, template1_param3)
    
def template1_result(rules, template1_param1, template1_param2, template1_param3):
    temp_result = set()
    for rule in rules:
        head = (rule[0])
        body =(rule[1])
        if template1_param1 == "RULE":
            #for rule it can be head or body, it can either be in head or body
            if template1_param2 == "ANY" and len(template1_param3 & (head | body)) > 0:
                temp_result.add(str(head) + "==>" + str(body))  
            elif template1_param2 == "1" and len(template1_param3 & (head | body)) == 1:
                    temp_result.add(str(head) + "==>" + str(body))
            elif template1_param2 == "NONE" and len(template1_param3 & (head | body)) == 0:
                temp_result.add(str(head) + "==>" + str(body))
        elif template1_param1 == "HEAD":
            if template1_param2 == "ANY" and len(template1_param3 & head) > 0:
                temp_result.add(str(head) + "==>" + str(body))
            elif template1_param2 == "1" and len(template1_param3 & head) == 1:
                temp_result.add(str(head) + "==>" + str(body))
            elif template1_param2 == "NONE" and len(template1_param3 & head) == 0:
                temp_result.add(str(head) + "==>" + str(body))
        elif template1_param1 == "BODY":
            if template1_param2 == "ANY" and len(template1_param3 & body) > 0:
                temp_result.add(str(head) + "==>" + str(body))  
            elif template1_param2 == "NONE" and len(template1_param3 & body) == 0:
                temp_result.add(str(head) + "==>" + str(body))
            elif template1_param2 == "1" and len(template1_param3 & body) == 1:
                temp_result.add(str(head) + "==>" + str(body))
    return temp_result
    
def template2_input(rules, query):
    #RULE|HEAD|BODY#SIZE
    template2 = query.replace('"','')
    template2 = template2.split(',')
    template2_param1 = template2[0].strip().upper()
    template2_param2 = int(template2[1].strip()[0:1])
    results = template2_result(rules, template2_param1, template2_param2)
    return results

def template2_result(rules, template2_param1, template2_param2):
    temp_result = set()
    for rule in rules:
        head = (rule[0])
        body =(rule[1])
        if template2_param1 == "RULE":
            if(len(head | body) >= template2_param2):
                temp_result.add(str(head) + "==>" + str(body))
        if template2_param1 == "HEAD":
            if(len(head) >= template2_param2):
                temp_result.add(str(head) + "==>" + str(body))
        if template2_param1 == "BODY":
            if(len(body) >= template2_param2):
                temp_result.add(str(head) + "==>" + str(body))
    return temp_result

def createQueryResults(rules, templateType1, templateType2, templateRule1, templateRule2):
    temp_result1 = set()
    temp_result2 = set()
    length = 0
    if templateType1 == 1:
        temp_result1 = template1_input(rules, templateRule1)
    elif templateType1 == 2:
        temp_result1 = template2_input(rules, templateRule1)
    if templateType2 == 1:
        temp_result2 = template1_input(rules, templateRule2)
    elif templateType2 == 2:
        temp_result2 = template2_input(rules, templateRule2)
    return temp_result1, temp_result2

def createTemplates(query, operator):
    template_rule_1 = str()
    template_rule_2 = str()
    querystr = query.strip().upper().replace('"','')
    template3 = querystr.split(operator)
    templateType1 = int(template3[0][0:1])
    template3_part2_str = template3[1]
    #it will give rule 2 type
    templateType2 = int(template3_part2_str[0:1])
    if templateType1 == 1:
        #split the template3_part2_str string using ]
        idx = template3_part2_str.index(",")
        template_rules_str = template3_part2_str[idx+1:]
        template_rules_arr = template_rules_str.split("]")
        template_rule_1 = template_rules_arr[0] + "]"
        template_rule_2_str = template_rules_arr[1]
        idx = template_rule_2_str.index(",")
        if templateType2 == 1:
            template_rule_2 = template_rule_2_str[idx+1:] + "]"
        else:
            template_rule_2 = template_rule_2_str[idx+1:]
    if templateType1 == 2:
        idx = template3_part2_str.index(",")
        template_rules_str = template3_part2_str[idx+1:].strip()
        template_rule_1 = template_rules_str[0:7].strip()
        template_rule_2 = template_rules_str[8:].strip()
        if templateType2 == 1:
            template_rule_2 = template_rule_2 + "]"
    return templateType1, templateType2, template_rule_1, template_rule_2

def template3_input(rules, query):
    #1or1,RULE1,RULE2
    #find first whether the input query contains OR or AND
    querystr = query.strip().upper()
    template_rule_1 = str()
    template_rule_2 = str()
    templateType1 = 0
    templateType1 = 0
    if "OR" in  querystr:
        templateType1, templateType2, template_rule_1, template_rule_2 = createTemplates(query, "OR")
        temp_result1, temp_result2 = createQueryResults(rules, templateType1, templateType2, template_rule_1, template_rule_2)
        resultSet = temp_result1.union(temp_result2) 
    elif "AND" in querystr:
        templateType1, templateType2, template_rule_1, template_rule_2 = createTemplates(query, "AND")
        temp_result1, temp_result2 = createQueryResults(rules, templateType1, templateType2, template_rule_1, template_rule_2)
        resultSet = temp_result1.intersection(temp_result2)
    return resultSet

def loadDataSet():
    fileName = "/Users/shivanithakur/Documents/SEMESTER3/datamining/associationruletestdata.txt"
    #G1_UP/DOWN G2_Down/Up........Disease
    gene_data = []
    delimiter = "\t"
    with open(fileName, "r") as file:
        lines = file.readlines()
        for line in lines:
            patient_data = line.strip().split(delimiter)
            patient_gene_data = []
            for i, data in enumerate(patient_data):
                if i == len(patient_data)-1:
                    data.upper()
                    patient_gene_data.append(data)
                else:
                    patient_gene_data.append("G"+str(i+1)+"_"+data.upper())
            gene_data.append(patient_gene_data)
    return gene_data


#creates 1-length candidate itemsets from the database
def createC1(dataSet):
    C1 = []
    for tran in dataSet:
        for item in tran:
            if not [item] in C1:
                C1.append([item])
    return list(map(frozenset,C1))

#joins item sets to create larger length-size supersets
def joinSet(itemSet, length):
    resultSet = set()
    for i in itemSet:
        for j in itemSet:
            if(len(i.union(j))==length):
                resultSet.add(i.union(j))
    return resultSet

#creates length m subsets(smaller) from a given subset
def findSubsets(S,m):
    return set(itertools.combinations(S, m))
               

#removes itemsets from candidate itemsets whose all subsets are not frequent itemsets.
#this filters the larger size itemsets which are infrequent.
def prunedSet(Ck,length, LPrev):
    prunedCk = Ck
    #iterate LPrev to generate simple sets 
    for c in Ck.copy():     
        resultSubset = findSubsets(c,length)
        resMasterSet = set()
        for temp in resultSubset:
            resMasterSet.add(frozenset(temp))
        if (len(resMasterSet.intersection(LPrev))!=len(resMasterSet)):
            prunedCk.remove(c)
    return prunedCk

#iterates the dataset to identify the frequent item sets 
#and creates a dictionary for mapping the item set to its support in the dataset
def createSupportData(Lk, dataSet, minSupppot):
    supportCount = dict()
    for transaction in dataSet:
        for k in Lk:
            if (k.issubset(transaction)):
                if not k in supportCount:
                    supportCount[k] = 1
                else:
                    supportCount[k]+=1
    numOfRecords = float(len(dataSet))
    retItems = []
    freqItemsetsCount = dict()
    for item in supportCount:
        support = supportCount[item]/numOfRecords
        if support >= minSupppot:
            retItems.append(item)
        freqItemsetsCount[item] = support
    return retItems, freqItemsetsCount

#apriori algorithm to generate frequent item sets
def apriori(data, minSupport):
    C1 = createC1(data)
    #change the created dataset into set form
    dataSet = list(map(set, data))
    L1, freqItemsetsCount = createSupportData(C1, dataSet, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = joinSet(L[k-2], k)
        temp_Lk = prunedSet(Ck, k-1,L[k-2])
        Lk, tempSupport = createSupportData(temp_Lk,dataSet, minSupport) 
        freqItemsetsCount.update(tempSupport)
        L.append(Lk)
        k += 1
    return L, freqItemsetsCount

#generates association rules from frequent item sets
def generateAsscoiationRules(L, suppData, minconf = 0.7):
    rule_list = []
    for k in range (1, len(L)):
        itemSet = L[k]
        for item in itemSet:
            H1 = [frozenset([i]) for i in item]
            if(k==1):
                checkConf(item, H1,rule_list, suppData, minconf)  
            else:
                createRules(item, H1, rule_list, suppData, minconf)            
    return rule_list

#filters the rules that support the minimum confidence criteria
def checkConf(item, H1,rule_list, suppData, minconf = 0.7):
    consequents = []
    for i in H1:
        conf = suppData[item]/suppData[item-i]
        if conf>=minconf:
            rule_list.append((item-i, i, conf))
        consequents.append(i)
    return consequents
        
#recursive function to create association rules from a given frequent itemset
def createRules(item, H, rule_list, suppdata, minconf = 0.7):
    k = len(item)
    m = len(H[0])
    if k>m+1:
        Hk1 = joinSet(H, m+1)
        Hm1 = list(prunedSet(Hk1, m, H))
        Hm1 = checkConf(item, Hm1, rule_list, suppData)
        for temp in Hm1:
            conf = suppData[item]/suppData[item-temp]
            if conf>=minconf:
                rule_list.append((item-temp, temp, conf))
        if(len(Hm1)>1):
            createRules(item, Hm1, rule_list, suppdata, minconf)

def printResults(queryResults):
    if len(queryResults)==0:
        print("No matching rules found for the given query")
    else:
        i = 1
        for item in queryResults:
            print("RULE ::", i , "-->", item)
            i += 1
        

dataSet = loadDataSet()
#input for support and confidence from the user 
minsup = float(input("Enter minimum support -> 0.0 to 1.0"))
minconf = float(input("Enter minimum confidence -> 0.0 to 1.0"))
L,suppData = apriori(dataSet, minsup)
rules = set(generateAsscoiationRules(L, suppData, minconf))
k = 'A'
while k=='A':
    query = input("Association Rules Generated for given support and confidence. Enter the query now or Q to exit")
    if query == "Q":
        k = 'Q'
    else:
        templateRule = query[query.index('(')+1:query.index(')')]
        queryResults = set()
        if "template1" in query:
            queryResults = template1_input(rules, templateRule)
        elif "template2" in query:
            queryResults = template2_input(rules, templateRule)
        elif "template3" in query:
            queryResults = template3_input(rules, templateRule)
        else:
            print("Invalid template found")
        printResults(queryResults)