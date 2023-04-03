def pop_Generation():
    '''For the generation of 'POP' number of chromosomes.'''
    return [[[1] + [random.randint(1, ROWS) for _ in range(COLS-2)] + [ROWS], [random.randint(0, 1) for _ in range(2)]] for _ in range(POP)]
def checkObstacle(a:tuple,b:tuple):
    '''Decide the obstacle in the way of Robot in a particular cell,according to its movement.'''
    dx,dy=b[0]-a[0],b[1]-a[1]
    if(dx!=0):
        if ((dx>0 and dic[a]['S']==0) or (dx<0 and dic[a]['N']==0)):return 1
    elif(dy!=0) :
        if ((dy>0 and dic[a]['E']==0 ) or (dy<0 and dic[a]['W']==0)):return 1
    return 0

def fitness_Factors(l:list):
    '''For particular chromosome,this would give the number of Turns,PathLength and InfeasibleSteps taken by Robot
       For column first or column wise '0' is used, For row first or row wise '1' is used.
       After Observations:
         Direction = 0 ,Orientation = 0 ===> decide = 0.   Direction = 0 ,Orientation = 1 ===> decide = 1.
         Direction = 1 ,Orientation = 1 ===> decide = 0.   Direction = 1 ,Orientation = 0 ===> decide = 1.
       This Function also provide the path to be followed by Robot, Only when the required or desired chromosome is 
       found. 
    '''
    chr, [Or,Dir] = l
    pathFollwed=[]
    if Flag==1 : #When the solution found,taking the points.
        pathFollwed.append((1,1))
    if ROWS != COLS :
        Or = 0
    decide = Or ^ Dir 
    a,k,turns=(1,1),1,0 
    infeasible=[] #That measures the path length and infeable steps at a same time. 
    for gene in range(0,len(chr)-1):
        if chr[gene+1] != chr[gene] : #Checking for number of turns taken during path following.
            turns+=1
        y=gene+1
        limit=(chr[gene+1]+1) if chr[gene+1] >chr[gene] else (chr[gene+1]-1)
        while k!=limit:
            b = (k, y+decide) if Or == 0 else (y+decide, k)
            infeasible.append(checkObstacle(a,b))# use of variable
            if Flag==1 and b not in ((1,1),(ROWS,COLS)) :
                pathFollwed.append(b)
            a=b
            if chr[gene+1] >chr[gene]:k+=1  
            else :k-=1
        if chr[gene+1] >chr[gene]:k-=1  
        else :k+=1
    LenGth=len(infeasible)
    if ROWS<=COLS:
        infeasible.append(checkObstacle( a,(ROWS,COLS) ))
        LenGth-=1
    if Flag==1: 
        pathFollwed.append((ROWS,COLS))
        pathFollwed.reverse()
        return pathFollwed,turns,LenGth,sum(infeasible)
    return turns,LenGth,sum(infeasible)

def cross_Over(l:list):
    '''ELITISM:
      By taking the fittest parent(First Half of Population) after selection then crossing their values(Single point crossover),
      expected to make more fittest offspring for the search of the ultimate solution.
    '''
    start, cross_point = int(POP/2), random.randint(2, COLS-2)
    end= POP-1 if start%2==1 else POP
    for child in range(start,end,2):
        #child1          Parent1                              Parent2
        l[child][0]    = copy.deepcopy(l[child-start][0][0:cross_point ]  + l[child-start+1][0][cross_point :])
        #child2          Parent2                              Parent1
        l[child+1][0]  = copy.deepcopy(l[child-start+1][0][0:cross_point ]+ l[child-start][0][cross_point :])

def mutation(l:list):
    '''
    Muhtation:
    For each population different mutation index and mutation value and changing the orientation bits of less
    fitness population.
    '''
    for i in range(POP):
        gene,Direction=l[i]
        gene[random.randint(2,COLS-2)] =random.randint(1, ROWS)
        if i >= int(POP/2) :
            Direction[0],Direction[1] = random.randint(0,1),random.randint(0,1)

def Fitness(m:list,l:list):
    '''
    Criteria to Jugde or evaluation of the fittest chromosome, since  value of Number of turn, pathLength
    and Infeasible steps lie in different ranges.So scaling down the value then give fitness value. 
    '''
    T_max,T_min,L_max,L_min,I_max,I_min=m# min of infeasible =0
    I_min=0
    pop_T,pop_L,pop_I=l # turns,length,infeasible steps
    F_t=1 -(pop_T-T_min)/(T_max-T_min)
    F_l=1 -(pop_L-L_min)/(L_max-L_min)
    F_i=1 -(pop_I-I_min)/(I_max-I_min)
    return (100 * W_I * F_i) * ((W_L * F_l) + (W_T * F_t)) / (W_L + W_T)

if __name__ =='__main__':
    from pyamaze import maze, agent
    import random,copy
    import time
    ROWS = 15
    COLS = 15
    POP  = 500
    MAX_TRY= 2000
    W_L,W_T,W_I =2,3,3
    Flag=0
    #Maze Creation:
    m = maze(ROWS, COLS)
    m.CreateMaze(loopPercent=100)
    a = agent(m,shape='square',filled=True,footprints=True)
    dic=m.maze_map 
    start_time = time.time()
    chromosomes=pop_Generation() # Initial Population Genteration.
    #Result Convergening Loop. 
    for generation in range(MAX_TRY):
        Factor=[fitness_Factors(Chr) for Chr in chromosomes] # Turns,Length,Infeasible steps
        min_max=[] #Minmum and Maximum Values of Turns,Length,Infeasible steps
        for i in range(0,3):
            min_max.append( (max(Factor,key=lambda x:x[i])[i]) )
            min_max.append( (min(Factor,key=lambda x:x[i])[i]) )
        Population_fitness=[] 
        for i in range(len(chromosomes)):
            turn,length,infeasible_s = Factor[i]#list comprehensio generator and index 
            fit=Fitness(min_max,Factor[i])#Fitness of each chromosme.
            Population_fitness.append(fit)
            if  infeasible_s==0:# Chromosome Requirement(Solution).
                Flag=1
                path,TuRn,path_length,Infesibility= fitness_Factors(chromosomes[i])
                m.tracePath({a: path},delay=100)
                end_time = time.time()
                print(end_time - start_time)
                print('\033[95m*'*40)
                print(f'\033[95m{chromosomes[i]}\n{path[::-1]}\nTurns = {TuRn}\nPath_Length = {path_length}\nInfesibile_Steps= {Infesibility}')
                print('*'*40)
                m.run()
                break
        if Flag==1 :
            break
        # Parent Selection:
        chromosomes = [x[0] for x in sorted(zip(chromosomes,Population_fitness), key=lambda x: x[1],reverse=True)]
        cross_Over((chromosomes))
        mutation(chromosomes)
        print(f'iter = {generation}')  
    else: 
        print(f'\033[95mSolution does not found.')
