import random 

#------getting list of articles of a set of offers---------
def get_offers(i):
    global list_bids
    return list_bids[i]
#-------conflicts function(for one chromosome)---------
def conflictGraph(temp_bids):
    #global bids
    #global nbB
    conflict={}
    for i in range(len(temp_bids)-1):
        conflict[i]=[]
        for j in range(len(temp_bids)-1):
            if  i!=j and set(temp_bids[i])-set(temp_bids[j])!=temp_bids[i] :
                conflict[i].append(j)
                    
    return conflict

#-------conflicts function used in mutation(for one chromosome)---------
def conflictGraph2():
    global list_bids
    global nbB
    conflict={}
    for i in range(nbB):
        conflict[i]=[]
        for j in range(nbB):
            if  i!=j and len(set(list_bids[i])-set(list_bids[j]))!=len(list_bids[i]) :
                conflict[i].append(j)
                    
    return conflict


#-------verify conflicts function(for one chromosome)---------
def conflictVerification(chromosome):
    global nbB
    global list_bids
    global conflicts
    index_bids=[]
    temp_bids=[]
    for i in range(len(chromosome)):
        if chromosome[i]==1:
            index_bids.append(i)
    
    for i in range(len(index_bids)):
        for j in range(i+1,len(index_bids)):
            if index_bids[j] in conflicts[index_bids[i]]:
                return True
        
    return False
    '''
    for i in index_bids:
        temp_bids.append(list_bids[i])
    conflict=conflictGraph(temp_bids)
    if not len(conflict): 
        return False
    else: 
        return True
    '''


#-------fitness function---------
def fitness(chromosome):
    fitness_value = 0
    global bids
    for i in range(len(chromosome)):
        if (chromosome[i]==1):
            fitness_value=fitness_value+bids[i]
    return fitness_value

#-------------chromosome class---------------
class individual:
    def __init__(self,chromosome,fitness,generation):
        self.chromosome=chromosome
        self.fitness = fitness
        #self.score=score
        self.generation = generation
    def __repr__(self):
        return '{' + self.chromosome + ', ' + str(self.fitness)  +','+ str(self.generation) + '}'

#-------score function---------
def score(chromosome):
    global conflicts
    nbconflict=0

    for i in range(len(chromosome)):
        if chromosome[i]==1:
            #nbconflict=nbconflict+len(conflicts[i])
            break
    if nbconflict==0:
        cscore=0
    else :
        #cscore=1/nbconflict
        cscore=0
        
    return cscore

    
#-------chromosome creation function---------
def create_chromosome():
    chromosome=[]

    #randomn=random.randint(0,1499)

    for i in range(1500) :
        chromosome.append(random.randint(0,1))
    
    new_chrom=unconflict(chromosome)
    '''for i in range(1500):
        if i==bit :
            chromosome.append(1)
        else :
            chromosome.append(0)'''
    
        
    fitness_value = fitness(new_chrom)
    #score_value= score(chromosome)
    
    generation=1
    objet=individual(new_chrom,fitness_value,generation)
    
    return objet

#----------------Initialize Population Function------------------
def Init_population(nbp):
    #global nbp
    global bids
    temp_bids=bids.copy()
    population=[]
    indices=[]
    #print('init POP')
    #population.sort(key=lambda x: x.fitness,reverse=True)
    '''for i in range(nbp):
        max_value=max(temp_bids)
        max_index = bids.index(max_value)
        max_index_fake=temp_bids.index(max_value)
        indices.append(max_index)
        temp_bids.pop(max_index_fake)'''

    #while conflict_state: #conflictVerification(population):
    for i in range(nbp):
        population.append(create_chromosome())
    '''conflict_state=False
        for element in population:
            if(conflictVerification(element.chromosome)):
                population=[]
                conflict_state=True
                break '''        
    return population    
                
#--------------------------Selection Function---------------------
    
#-------------------------Crossover Function----------------------
def crossover(Parent1, Parent2, crossover_point):
    child1 = []
    child2 = []
    children = []

    '''for i in range (crossover_point):
        child1.append(Parent1[i])
        child2.append(Parent2[i])
    
    for i in range (crossover_point, len(Parent1)):
        child1.append(Parent2[i])
        child2.append(Parent1[i])'''

    bits1=showbits(Parent1)
    bits2=showbits(Parent2)

    for i in range(1500):
        child2.append(0)
        if i in bits1 or i in bits2 :
            child1.append(1)
        else :
            child1.append(0)
    
    children.append(child1)
    children.append(child2)

    if not(conflictVerification(child1)) :
        return children
    else: 
        children[0]=unconflict(children[0])
        return children


#-------------------------Mutation Function-----------------------
def unconflict(child):
    #sans mutation rate 
    global conflicts
    global nbB
    global list_bids
    index_bids=[]
    temp_bids=[]
    childm = child
    rand=random.randint(1,len(childm))
    for i in range(rand,len(childm)):
        if childm[i]==1:
            for j in conflicts[i]:
                childm[j]=0
    
    for i in range(rand-1,-1,-1):
        if childm[i]==1:
            for j in conflicts[i]:
                childm[j]=0
    return childm


def mutation2(child, mutation_rate):
    #avec mutation rate
    childm = child
    probability = random.randint(0,100)
    if (probability >= mutation_rate):
        mutation_gene = random.randint(0,len(child)-1)
        childm[mutation_gene] = (1 - childm[mutation_gene])
    return childm


def mutation3(child) :
    childm=child.copy()
    for i in range(10) :
        randomnumber=random.randint(0,nbB-1)
        childm[randomnumber]=1
        if(conflictVerification(childm)):
            childm[randomnumber]=0

        return childm
    

#-------------------------best chromosomes-----------------------
def best_chromosomes(population,nbparents):
    best_parents=[]
    population.sort(key=lambda x: x.fitness,reverse=True)
    for i in range(nbparents):
        best_parents.append(population[i])
    return best_parents

#-----------------------update GBest--------------------------
def updateGBest(population):
    global Gbest
    for element in population:
            #print('looking for new Gbest')
            if(not conflictVerification(element.chromosome)):
                if(Gbest.fitness<element.fitness):
                    Gbest=element
                    break
                    
    #print(Gbest.fitness)

#-------------------------Choosing parents-----------------------
def chooseParents(population,i):
    global nbparents
    best_match=random.randint(0,nbparents)
    nb_conflit=1500
    
    for j in range(0,nbparents):
        if i!=j :
            index_bids=[]
            for k in range(0,len(population[j].chromosome)):
                if(population[j].chromosome[k]==1):
                    index_bids.append(k)

            #print('CONFLICTS',conflicts[i])
            #print('INDICES',index_bids)
            temp=len(set(conflicts[i]).intersection(index_bids))
            #print(temp,' for j=',j)
            if temp<nb_conflit:
                #print('i :',i," j : ",j)
                best_match=j
                nb_conflit=temp
                if nb_conflit== 0 :
                    break
    
    return population[best_match]

#-------------------------show 1s-----------------------
def showbits(chromosome):
    index_bids=[]
    for i in range(len(chromosome)):
        if chromosome[i]==1:
            index_bids.append(i)
    
    return index_bids

#-------------------------GA Updating generations-----------------------
def UpdatePopulation(population,nbp):
    global crossover_point
    global generation 
    global nbB
    global Gbest
    updateGBest(population)
    while(generation < nbgenerations+1):
        total_children=[]
        new_population=[]
        best_parents=[]
        children=[]
        for i in range(0,nbparents,1):
            #selectioner les parents 
            parent1=population[i]
            parent2=chooseParents(population,i)
            #Appliquer le crossover
            children=crossover(parent1.chromosome,parent2.chromosome,crossover_point)
            
            #Appliquer la mutation au 1er offspring
            child1=mutation3(children[0])
            ch1=individual(child1,fitness(child1),generation)
            total_children.append(ch1)
            
            #print('fitness  1:',ch1.fitness)
            #print(conflictVerification(ch1.chromosome))
            

            #Appliquer la mutation au 2ème offspring
            #child2=mutation(children[1])
            #ch2=individual(children[1],fitness(children[1]),score(children[1]),generation)
            #total_children.append(ch2)
            #print(showbits(ch2.chromosome))
            #print('fitness 2 :',ch2.fitness)
            #print(conflictVerification(ch2.chromosome))
            

        best_parents=best_chromosomes(population,nbparents)
        reste=nbp-len(total_children)
        new_population=new_population+total_children

        for i in range(reste):
            new_population.append(best_parents[i])

        new_population.sort(key=lambda x: x.fitness,reverse=True)

        population=new_population

        generation=generation+1

        updateGBest(population)

        print('--------------------------------------------------------------')
        print('best valid offer at generation:',generation-1,':')
        print('fitness = ',Gbest.fitness,'generation =',Gbest.generation)
        print(showbits(Gbest.chromosome))

    print('GBest chromosome : ',Gbest.chromosome)



#------------------------------MAIN-------------------------------

import time
generation=1
nbgenerations=20
nbparents=100
nbp=120
nbB=1500
crossover_point = random.randint(1,9)
population=[]
list_bids=[]
f = open("in510.txt", "r")
line=f.readline()
bids=[]
for l in range(1500):
    line=f.readline()
    x=line.split('.')
    bid=int(x[0])
    
    bids.append(bid)
    
    y=x[1]
    articles=y.split(' ')

    #print(bid)
    #print(articles)
    new_art=[]
    for element in articles :
        new_art.append(element.strip())

    list_bids.append(new_art)

#generating conflictGraph
conflicts=conflictGraph2()

#generate the Gbest
Gbest_list=[0]*1499
Gbest_list.append(1)
Gbest=individual(Gbest_list,fitness(Gbest_list),1)
print("1st gbest : ",Gbest.fitness)


print("finished conflictGraph")
start_time = time.time()
population=Init_population(nbp)
UpdatePopulation(population,nbp)
end_time=time.time()
print('execution time:',end_time - start_time)



#########################################################################
