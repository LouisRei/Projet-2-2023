import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm





def simulation(D, l, V_P, V_R):
    '''
    Fonction qui a pour but d'effectuer la simulation correspondant à l'article étudié dans des conditions similaires

    On va itérer sur un nombres de jours qui est égale au nombre de jour pour distribué les doses + 20 jours pour voir l'effet après toute vaccination faite

    ON change dans D le nombre de doses et leur répartition sur les différents jours.

    Le temps de mise en éfficacité du vaccin est plus long que le temps de la maladie.

    On considère qu'il suffit  d'une dose pour atteindre la vaccination maximal possible.

    On ne prend pas en compte la réduction de contagion par le vaccin ( juste le fait qu'il permet de moins attraper la maladie et la maladie dure moins longtemps ).

    Chaque jour on va regarder l'évolution de la protec vaccinale ce qui est plus détaillé que le modele qui prend seulement en compte la protec final (limite du modele dépassé)

    l pourcentage de la pop vac initialement
    m pourcentage de la pop malade initialement

    D = [t, Nd] # t = nombre de jour de l'essai ; Nd = Nombre de dose par jour --) Nd -) [50,500] pour masse, -) [50,250] pour reactive

    Parameters:
    -----------
    parametres: List (ou array)
        Vecteur contenant tous les paramètres nécessaires à la simulation (incidence, efficacité de la vaccination...)

    Outputs:
    --------
    res: array
        Vecteur contenant le nombre final de contaminés, sains, vaccinés...
    '''

    
    # Parametres
    N = 76370  #Nombre total d'habitants en age de la simulation
    E = 1880   #Represente le nombre total d'entreprises
    Sch = 39 # Nombre d'ecoles 
    p_t = 0.1 # Part de la population de chaque groupe en teletravail
    R = 1.6 # 1 personne malade contamine R personnes
    m = 0.13 # 13% de la pop est malade initialement
    
    Vintermediaire = l*N # l est le parametre sur lequel on jour pour faire varier la pop vac initiale
    V_i = Vintermediaire # Part de la population vacciné
    M = m*N

    J = D[0]





    # Initialisation du modèle

    groupes = {i: [0 , 0] for i in range(E+Sch)}
    
    # Diviser l'espace en sous segments pour pouvoir avoir des entreprises / écoles de taille non nul et réparti en taille aléatoirement pour representer au mieux la réalité.

    Pop_groupes = []
    
    for i in range(E+Sch):
        if i<1100:
            Pop_groupes.append(random.randint(3,10))
        elif 1100<=i<1230:
            Pop_groupes.append(random.randint(10,50))
        elif 1230<=i<1310:
            Pop_groupes.append(random.randint(50,100))
        elif 1310<=i<1380:
            Pop_groupes.append(random.randint(100,500))
        elif 1380<=i<1387:
            Pop_groupes.append(random.randint(500,1000))
        elif 1387<=i<1397:
            Pop_groupes.append(random.randint(800,1200))
        elif 1397<=i<1415:
            Pop_groupes.append(9809//18)
        elif 1415<=i<1426:
            Pop_groupes.append(6665//11)
        elif 1426<=i:
            r = (76370 - sum(Pop_groupes[:1426])) // 6

            Pop_groupes.append(1000 + r)

    for i in range(E+Sch):

        groupes[i][0] = Pop_groupes[i]
        

    # order(L)
    

    

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    for i in groupes:
        "Faire en sorte que la répartition des groupes soit toujours la meme (avec fichier annexe, np.random.seed ou autre on s'en blc)"
        

        groupes[i][1] = {i: [False, 0, 0, 0, 0, False, False, 0, False] for i in range(groupes[i][0])} 
        
        

        """ 1) False = leur état de contamination , 
        2)  Puissance de protection vaccinale ( la protection qu'on à),
         3) temps qu'il nous reste à être malade
          4) temps qu'il nous  reste a gagner de la protection vaccinale
        Pour 4) une fois que 2) vaut 1 on arrete de compter
        5) Puissance de reduction du temps de maladie
        6) False = pas de télétravail
        7) False = pas contagieux
        8) Accumulation de dose qu'il va recevoir à la fin : V_Ac
        9) False = pas encore vacciné
        
        """
    for i in groupes:
        for j in range(len(groupes[i][1]) - int(0.1*len(groupes[i][1])), len(groupes[i][1])):
            groupes[i][1][j][5] = True

    # Les gens vacciné au jour 1 sont par hypothèse : à leur protection vaccinale maximale i.e 70% de protection et 73% de reduction de temps de maladie

    b = 0

    while b < V_i:

        g = np.random.randint(E+Sch)
        p = np.random.randint(len(groupes[g][1]))
        
        if groupes[g][1][p][8] == False:

            groupes[g][1][p][1], groupes[g][1][p][4] = V_P, V_R

            groupes[g][1][p][8] = True

            b += 1

    a = 0

    while a < M:
        
        g = np.random.randint(E+Sch)
        p = np.random.randint(len(groupes[g][1]))
        
        if groupes[g][1][p][0] == False:
            groupes[g][1][p][0] = True
            groupes[g][1][p][2] = int(3.7*(1- groupes[g][1][p][4])) + 7
            groupes[g][1][p][6] = True
            a += 1
    

    # Stratégie de vaccination de masse : 100*0.76 à 500*0.76 à faire varier les doses par jour ( pour faire comme dans le modèle )
    W = []
        
    for _ in tqdm(range(J)): # On parcourt les jours et on va modifié les états à chaque jour
        
        Nb_Malade = 0
        # On regarde d'abord la contamination avant d'augmenter l'efficacité du vaccin ( le vaccin met 24h dans notre hypothese a gagner en efficacité )
        
        for i in groupes:
            
            
            for j in range(len(groupes[i][1])):
                
                if groupes[i][1][j][6] == True:

                    for k in range(len(groupes[i][1])):
                            
                        if len(groupes[i][1]) != 1:
                                
                            x = 0.37*R*(1/(len(groupes[i][1])-1))*(1- groupes[i][1][k][1])

                            a = random.random()

                            if x >= a:
                            # Nous considérons les guéris comme intouchables, de plus les malades ne vont pas retomber plus malades qu'avant

                            # On considére que toute personne malade est contagieuse

                                if groupes[i][1][k][0] == False:

                                    groupes[i][1][k][0] = True

                                    groupes[i][1][k][2] = int(3.7*(1- groupes[i][1][k][4])) + 7 
                                    # 3.7 jours est le temps pendant lequel on est contagieux sans vaccination (on arrondi le jour a celui d'au dessus) + 7 le temps de récuperation

                                    if groupes[i][1][k][4] > 0.75:
                                        groupes[i][1][k][4] = 1
                                    else:   
                                        groupes[i][1][k][4] += 0.25 # Quand on a été malade on gagne 35% de reduction de temps de maladie
                                        
                                    if groupes[i][1][k][3] == 0:

                                        groupes[i][1][k][3] = 35 # début de la création de protection à la maladie
                                            
                                        

                                    if groupes[i][1][k][2] <= 7:

                                        groupes[i][1][k][6] = False 


                                            # Quand il reste 7 jours de maladie, c'est de la récup, on est donc plus contagieux
                if groupes[i][1][j][0] == True:  
                     
                    Nb_Malade += 1
                    
                if groupes[i][1][j][0] == True and groupes[i][1][j][2] == 0:

                    groupes[i][1][j][0] = False

                    # Si tu es plus malade et que tu t'es remis alors tu peux redevenir malade

                if groupes[i][1][j][3] == 1:

                    if groupes[i][1][j][1] > 1 - groupes[i][1][j][7]:

                        groupes[i][1][j][1] = 1
                        
                    else:
                        groupes[i][1][j][1] += groupes[i][1][j][7]


                    if groupes[i][1][j][4] > 1 - groupes[i][1][j][7]:

                        groupes[i][1][j][4] = 1
                        
                    else:
                        groupes[i][1][j][4] += groupes[i][1][j][7]
                    
                groupes[i][1][j][7] = 0
            

                if groupes[i][1][j][2] > 0 :
                
                    groupes[i][1][j][2] -= 1

                if groupes[i][1][j][3] > 0 :
                
                    groupes[i][1][j][3] -= 1

            


        c = 0
        while c < D[1]:

            g = np.random.randint(E+Sch)
            p = np.random.randint(len(groupes[g][1]))
            
            if groupes[g][1][p][8] == False:

                a = random.random()

                if a <0.8: # proba que la personne accepte le vaccin

                    groupes[g][1][p][7] += V_P
                    
                    groupes[g][1][p][8] = True

                
                    c += 1
            
        W.append(Nb_Malade)

    # W est la liste contenant en i : le nombre de malade au jour i+1
    return [W]

def simulation_reac(D, l, V_P, V_R):
    '''
    On reprend de manière générale les hypothèses de la simulation initiale en considérant cette fois un modèle de vaccination réactif,

    c'est à dire qu'elle s'effectue suivant un "cluster trigger" qu'on considère ici égal à 1 comme dans la première simulation de l'article.

    Ainsi, chaque jour on considère les nouvelles entreprises sujettes à un plan de vaccination et on les met en place.


    Paramètress:
    -----------
    D: List 
        sous format [Nombre jour, nombre doses max par jour] ([50,250] en réactif)

    l: float
        Pourcentage de la population vaccinée initialement

    V_P: float
        Protection post vaccin/infection

    V_R: float
        Reduction du temps de maladie apres vaccin/infection


    Outputs:
    --------
    V: array
        Vecteur contenant le nombre final de contaminés, sains, vaccinés...
    '''

    
    # Parametres
    N = 76370 #Nombre total d'habitants en age de la simulation
    E = 1880 #Represente le nombre total d'entreprises
    Sch = 39 # Nombre d'ecoles 
    p_t = 0.1 # Part de la population de chaque groupe en teletravail
    R = 1.6 # 1 personne malade contamine R personnes
    m = 0.13 # 13% de la pop est malade initialement
    
    Vintermediaire = l*N # l est le parametre sur lequel on jour pour faire varier la pop vac initiale
    V_i = Vintermediaire # Part de la population vacciné
    M = m*N

    J = D[0]





    # Initialisation du modèle

    groupes = {i: [0 , 0, [False,False]] for i in range(E+Sch)}  #3e parametre = si besoin de campagne de vaccination

    Pop_groupes = []
    
    for i in range(E+Sch):
        if i<1100:
            Pop_groupes.append(random.randint(3,10))
        elif 1100<=i<1230:
            Pop_groupes.append(random.randint(10,50))
        elif 1230<=i<1310:
            Pop_groupes.append(random.randint(50,100))
        elif 1310<=i<1380:
            Pop_groupes.append(random.randint(100,500))
        elif 1380<=i<1387:
            Pop_groupes.append(random.randint(500,1000))
        elif 1387<=i<1397:
            Pop_groupes.append(random.randint(800,1200))
        elif 1397<=i<1415:
            Pop_groupes.append(9809//18)
        elif 1415<=i<1426:
            Pop_groupes.append(6665//11)
        elif 1426<=i:
            r = (76370 - sum(Pop_groupes[:1426])) // 6

            Pop_groupes.append(1000 + r)

    for i in range(E+Sch):

        groupes[i][0] = Pop_groupes[i]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    for i in groupes:
        "Faire en sorte que la répartition des groupes soit toujours la meme (avec fichier annexe, np.random.seed ou autre on s'en blc)"
        

        groupes[i][1] = {i: [False, 0, 0, 0, 0, False, False, 0, False] for i in range(groupes[i][0])} 
        
        

        """ 1) False = leur état de contamination , 
        2)  Puissance de protection vaccinale ( la protection qu'on à),
         3) temps qu'il nous reste à être malade
          4) temps qu'il nous  reste a gagner de la protection vaccinale
        Pour 4) une fois que 2) vaut 1 on arrete de compter
        5) Puissance de reduction du temps de maladie
        6) False = pas de télétravail
        7) False = pas contagieux
        8) Accumulation de dose qu'il va recevoir à la fin : V_Ac
        9) False = pas encore vacciné
        
        """
    for i in groupes:
        for j in range(len(groupes[i][1]) - int(0.1*len(groupes[i][1])), len(groupes[i][1])):
            groupes[i][1][j][5] = True

    # Les gens vacciné au jour 1 sont par hypothèse : à leur protection vaccinale maximale i.e 70% de protection et 73% de reduction de temps de maladie

    b = 0

    while b < V_i:

        g = np.random.randint(E+Sch)
        p = np.random.randint(len(groupes[g][1]))
        
        if groupes[g][1][p][8] == False:

            groupes[g][1][p][1], groupes[g][1][p][4] = V_P, V_R

            groupes[g][1][p][8] = True

            b += 1

    a = 0

    while a < M:
        
        g = np.random.randint(E+Sch)
        p = np.random.randint(len(groupes[g][1]))
        
        if groupes[g][1][p][0] == False:
            groupes[g][1][p][0] = True
            groupes[g][1][p][2] = int(3.7*(1- groupes[g][1][p][4])) + 7
            groupes[g][1][p][6] = True
            a += 1
    X = []
    V = []
    for _ in tqdm(range(J)): # On parcourt les jours et on va modifié les états à chaque jour
        x = 0
        Nb_Malade = 0
        # On regarde d'abord la contamination avant d'augmenter l'efficacité du vaccin ( le vaccin met 24h dans notre hypothese a gagner en efficacité )
        
        for i in groupes:
            
            
            for j in range(len(groupes[i][1])):
                
                if groupes[i][1][j][6] == True:

                    for k in range(len(groupes[i][1])):
                            
                        if len(groupes[i][1]) != 1:
                                
                            x = 0.35*R*(1/(len(groupes[i][1])-1))*(1- groupes[i][1][k][1])

                            a = random.random()

                            if x >= a:                            # Nous considérons les guéris comme intouchables, de plus les malades ne vont pas retomber plus malades qu'avant

                                # On considére que toute personne malade est contagieuse

                                if groupes[i][1][k][0] == False:

                                    groupes[i][1][k][0] = True

                                    if not groupes[i][2][0] and groupes[i][0]>= 20:
                                        groupes[i][2][0] = True
                                        x+= 1

                                    groupes[i][1][k][2] = int(3.7*(1- groupes[i][1][k][4])) + 7 
                                    # 3.7 jours est le temps pendant lequel on est contagieux sans vaccination (on arrondi le jour a celui d'au dessus) + 7 le temps de récuperation

                                    if groupes[i][1][k][4] > 0.75:
                                        groupes[i][1][k][4] = 1
                                    else:   
                                        groupes[i][1][k][4] += 0.25 # Quand on a été malade on gagne 25% de reduction de temps de maladie
                                    
                                    if groupes[i][1][k][3] == 0:

                                        groupes[i][1][k][3] = 35 # début de la création de protection à la maladie

                                    if groupes[i][1][k][2] <= 7:

                                        groupes[i][1][k][6] = False 


                                        # Quand il reste 7 jours de maladie, c'est de la récup, on est donc plus contagieux
                
                if groupes[i][1][j][0] == True:  
                     
                    Nb_Malade += 1
                    
                if groupes[i][1][j][0] == True and groupes[i][1][j][2] == 0:

                    groupes[i][1][j][0] = False

                    # Si tu es plus malade et que tu t'es remis alors tu peux redevenir malade

                if groupes[i][1][j][3] == 1:

                    if groupes[i][1][j][1] > 1 - groupes[i][1][j][7]:

                        groupes[i][1][j][1] = 1
                        
                    else:
                        groupes[i][1][j][1] += groupes[i][1][j][7]


                    if groupes[i][1][j][4] > 1 - groupes[i][1][j][7]:

                        groupes[i][1][j][4] = 1
                        
                    else:
                        groupes[i][1][j][4] += groupes[i][1][j][7]
                    
                groupes[i][1][j][7] = 0
            

                if groupes[i][1][j][2] > 0 :
                
                    groupes[i][1][j][2] -= 1

                if groupes[i][1][j][3] > 0 :
                
                    groupes[i][1][j][3] -= 1

        
        v = [] ; tot_emp = 0
        for e in range(len(groupes)):
            if groupes[e][2][0] and groupes[e][2][1]:
                v.append(e)
                tot_emp += groupes[e][0]
    
        while b < D[0]:
            e = random.choice(v)
            p = random.randint(len(e))
    
            if groupes[g][1][p][8] == False:
    
                a = random.random()
    
                if a <0.8: # proba que la personne accepte le vaccin
    
                    groupes[g][1][p][7] += V_P
                            
                    groupes[g][1][p][8] = True
    
                        
                    b += 1
        for i in range(len(groupes)):
            if groupes[i][2][0] and not groupes[i][2][1]:
                groupes[i][2][1] = True

        V.append(Nb_Malade)
        X.append(x)
    return [V, X] # X étant la liste contenant le nombre de workplace/uni qui ont lancé leur programme de vaccination à l'instant t

# 2.b reproduction

V = simulation_reac([15, 250], 0.1, 0.2, 0.2)[0]


import matplotlib.pyplot as plt

[W] = simulation([15, 250], 0.1, 0.2, 0.2)

w = np.linspace(0, 7, len(W))

plt.figure()

plt.plot(w, W, label = 'Vaccination de masse')
plt.plot(w, V, label = 'Vaccination réactive')
plt.xlabel('Semaines')
plt.ylabel('Nombre de cas')
plt.legend(title = 'Nombre de cas par semaine en fonction de la stratégie')
plt.show()




""" 2.c reproduction

X = simulation_reac([10, 50], 0.1, 0.2, 0.2)[1]


import matplotlib.pyplot as plt


w = np.linspace(0, 50, len(W))

plt.figure()


plt.plot(w, W, label = 'Vaccination reactive')
plt.xlabel('Jours')
plt.ylabel('WP/S  Vaccinated')
plt.legend(title = 'Nombre de cas par semaine en fonction de la stratégie')
plt.show()

"""