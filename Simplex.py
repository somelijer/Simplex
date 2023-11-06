#Ivan Mikic RA44/2020 11.11.2022

import numpy as np
import warnings

#ovo radimo da ne bi izlazio warning za deljenje sa nulom, moze se obrisati
warnings.filterwarnings(action='ignore', category=RuntimeWarning)


def simplex_iteration(simplex_tabela):
    #---------------------------------------------------
    #PRIMENA ALGORITMA
    #Namestili smo da uvek imamo problem trazenja maksimuma tako da
    #nam je cilj da imamo u donjoj vrsti sve pozitivne vrednosti.
    #Iz te vrste uzmemo najnegativniji element(ako postoji) i to proglasavamo
    #pivot kolonom

    #vrednost da obelezi kraj algoritma
    stop = 0

    #TRAZENJE PIVOT KOLONE
    rowsST,colsST = simplex_tabela.shape


    min = simplex_tabela[rowsST-1,0]
    pivotCol=0
    for i in range(1,colsST):
        if(simplex_tabela[rowsST-1,i] < min):
            min = simplex_tabela[rowsST-1,i]
            pivotCol = i

    print("Minimalni negativni u poslednjoj vrsti: ",min,"Pivot Kolona: ",pivotCol,"\n")

    #TRAZENJE PIVOT VRSTE
    #Delimo kolonu 0 tj kolonu slobodnih clanova sa pivot kolonom i uzimamo najmanji
    #POZITIVNI kolicnik
    #ako nema pozitivnih algoritam zaustavljamo
    #uzimamo u obzir da ne treba poslednju vrstu uzimati u obzir

    pivotRow = -1
    minpoz = -1
    for i in range (rowsST - 1):
        #ako je pozitivan
        if(simplex_tabela[i,0] / simplex_tabela[i,pivotCol] > 0):
            
            #ako je manji od trenutnog kandidata
            if(simplex_tabela[i,0] / simplex_tabela[i,pivotCol] < minpoz):
                minpoz = simplex_tabela[i,0] / simplex_tabela[i,pivotCol]
                pivotRow = i

            #ako je prvi kandidat
            if(minpoz == -1):
                minpoz = simplex_tabela[i,0] / simplex_tabela[i,pivotCol]
                pivotRow = i

            if(1):
                print(simplex_tabela[i,0]," / ",simplex_tabela[i,pivotCol]," = ",simplex_tabela[i,0] / simplex_tabela[i,pivotCol])
        
        
        else:
            if(1):
                print(simplex_tabela[i,0]," / ",simplex_tabela[i,pivotCol]," = ",simplex_tabela[i,0] / simplex_tabela[i,pivotCol],"  <--Ne dolazi u obzir")
            


    if(pivotRow == -1):
        print("Nema pozitivnih clanova u kolicniku pivot reda i reda slobodnih clanova\n")
        stop = 1
        print(simplex_tabela)
        return simplex_tabela,stop,np.array([0,0])
    else:
        print("Minimalni pozitvni je: ",minpoz," Pivot vrsta: ",pivotRow,"\n")
    
    
    #pamtimo pivotski clan da mu ne pregazimo vrednost u ovoj iteraciji
    pivotClan = simplex_tabela[pivotRow,pivotCol]
    print("Pivotski clan je: ",pivotClan,"\n")

    #VRSENJE TRANSFORMACIJE TABELE
    
    

    simplex_tabela = simplex_tabela.astype(float)

    #prvo sve ostale elemente da ne izgubimo vrednosti prve iteracije
    for i in range(rowsST):
        for j in range(colsST):

            if(i != pivotRow and j != pivotCol):
                simplex_tabela[i,j] = simplex_tabela[i,j] - simplex_tabela[i,pivotCol] * simplex_tabela[pivotRow,j] / pivotClan
    
    #pivotski clan
    simplex_tabela[pivotRow,pivotCol] = 1 / simplex_tabela[pivotRow,pivotCol]

    #pivotska kolono -ek/ep
    for i in range(rowsST):
        if(i != pivotRow):
            simplex_tabela[i,pivotCol] = -simplex_tabela[i,pivotCol] / pivotClan

    #pivotska vrsta ev/ep
    for j in range(colsST):
        if(j != pivotCol):
            simplex_tabela[pivotRow,j] = simplex_tabela[pivotRow,j] / pivotClan



    

            

    print("Izvrsena transformacija:\n",simplex_tabela)

    promena = np.array([0,0])
    promena[0] = pivotCol
    promena[1] = colsST + pivotRow
    #print("Promena clanova:",promena) 





    return simplex_tabela,stop,promena
        






def simplex(A,b,c,minimum = 0):

    #OSNOVNE PROVERE ULAZNIH VREDNOSTI
    #ako je problem trazenja minimuma mnozimo funkciju koju optimizujemo sa -1 da dobijemo problem maksimuma
    #i dobijamo negativne vrednosti promenjivih iz kriterijuma optimalnosti na kraju
    #takodje treba izvrsiti y = cx => y - cx = 0 pa mnozimo sa -1 ako trazimo max

    if(minimum == 0):
        c = c * -1

    #provera dimenzija matrice

    if(b.ndim != 1 or c.ndim != 1):
        print("Lose dimenzije matrica!")
        #print("b dimensions: ",b.ndim,"c dimensions",c.ndim)
        return None

    
    rowsA,colsA = A.shape
    colsB = b.shape[0]  #broj ogranicenja
    colsC = c.shape[0]  #broj prom iz fje opt

    if(colsA != colsC or rowsA != colsB):
        print("Lose dimenzije matrica!")
        #print(colsA,colsC,rowsA,colsB)
        return None

    if(1):
        print("Matrice su dobrih dimenzija")
        print("Matrixes:")
        print("A:")
        print(A,"\n")
        print("b:")
        print(b,"\n")
        print("c:")
        print(c,"\n")
        print("POCETAK ALGORITMA: \n\n")

    #---------------------------------------------------
    #PRAVLJENJE SIMPLEKS TABELE

    b = b.reshape(colsB,1)
    #print("Kolona slobodnih clanova:\n",b,"\n")
    

    c = np.insert(c,0,0)
    c = c.reshape(1,colsC+1)
    #print("Donja vrsta:\n",c,"\n")

    simplex_tabela = np.concatenate((b,A),axis=1)
    simplex_tabela = np.concatenate((simplex_tabela,c),axis=0)
    print("Simplex tabela:\n",simplex_tabela,"\n")



    #---------------------------------------------------
    #PRIMENA ALGORITMA
   
    rowsST,colsST = simplex_tabela.shape

    #stvaramo pomocnu strukturu za memorisanja gde se nalazi koji element prilikom pivotinga
    # u lokatoru broj 0 predstavlja y a ostali brojevi prvo promenjive iz opt. jednacine pa pomocne redom kako su upisani
    lokator = np.array(range(rowsST + colsST - 1))
    #print("Lokator",lokator)
    promena = np.array([0,0])
    


    #dokle god nemamo uslov da zaustavimo iteracije ponavjace se algoritam
    stop = 0
    while(stop == 0):

        #provera da li su sve vrednosti pozitivne tj. kraj algoritma
        for i in range(colsST):

            #ako ima makar jedna vrednost koja je negativna primenjujemo algoritam
            if(simplex_tabela[rowsST-1,i] < 0):
                
                
                simplex_tabela,stop,promena = simplex_iteration(simplex_tabela)
                #print(simplex_tabela,stop)

                #zamenjujemo dve promenjive iz pivota
                if(promena[0] == 0 and promena[1] == 0):
                    pass
                else:
                    temp = lokator[promena[0]]
                    lokator[promena[0]] = lokator[promena[1]]
                    lokator[promena[1]] = temp
                    #print(lokator) 

                #ako imamo uslov za zaustavljanje iz deljenja pivot i slobodne kolone
                if(stop == 1):
                    print("Algoritam zavrsen\n")
                break

        else:
            #ako imamo uslov za zaustavljanje iz pozitivnih clanova u poslednjoj vrsti
            stop = 1
            print("Pozitivni su svi clanovi u poslednjoj vrsti")
            print("Algoritam zavrsen\n")


    resenja = np.array(range(rowsST + colsST - 1))
    resenja = resenja.astype(float)

    
    #y na mestu 0
    resenja[0] = simplex_tabela[rowsST-1,0]
    if(minimum == 1):
        resenja[0] *= -1

    #upisemo sta je 0
    for i in range(1,colsST):
        resenja[lokator[i]] = 0

    #upisemo nenula vrednosti
    j = 0
    for i in range(colsST,rowsST + colsST - 1):
        resenja[lokator[i]] = simplex_tabela[j,0]
        j = j+1
        








    if(minimum == 1):
        #implementiraj vracanje vrednosti koje su negativne
        pass

    #povratna vrednost
    return resenja.round(2)





def prettyprint(res):
    print("y = ",res[0])

    for i in range(1,res.shape[0]):
        print("x[",i,"] = ",res[i])





def main():

    res = None
    #PRIMER SA VEZBI, ZA TESTIRANJE SAMO PROMENITI 0 U 1
    if(1):
        # y = 2x[1] - x[2]
        
        c = np.array([2,-1])

        # -3x[1] +2x[2] <= 2
        # 2x[1] -4x[2] <= 3
        # 1x[1] +1x[2] <= 6

        A = np.array([
            [-3,2],
            [2,-4],
            [1,1]
            ])

        b = np.array([2,3,6])
        res = simplex(A,b,c,0)

    #PRIMER SA VEZBI, ZA TESTIRANJE SAMO PROMENITI 0 U 1
    if(0):
        # y = -2x[1] + 3x[2]
        
        c = np.array([-2,3])

        # 1x[1] +1x[2] <= 4
        # 1x[1] -1x[2] <= 6

        A = np.array([
            [1,1],
            [1,-1]
            ])

        b = np.array([4,6])
        res = simplex(A,b,c,1)

    #PRIMER SA VEZBI, ZA TESTIRANJE SAMO PROMENITI 0 U 1
    if(0):
        # y = 60x[1] + 30x[2] + 20x[3]
        
        c = np.array([60,30,20])

        # 8x[1] +6x[2] +1x[3] <= 48
        # 4x[1] +2x[2] +1.5x[3] <= 20
        # 2x[1] +1.5x[2] +0.5x[3] <= 8
        # 1x[3] <= 5

        A = np.array([
            [8,6,1],
            [4,2,1.5],
            [2,1.5,0.5],
            [0,0,1]
            ])

        b = np.array([48,20,8,5])
        res = simplex(A,b,c,0)

    #PRIMER SA VEZBI, ZA TESTIRANJE SAMO PROMENITI 0 U 1
    if(0):
        # y = 1x[1] - 1x[2] + 4x[3]
        
        c = np.array([1,-1,4])

        # 1x[1] -1x[2] +1x[3] <= 3
        # -1x[1] +1x[2] +1x[3] <= 1

        A = np.array([
            [1,-1,1],
            [-1,1,1]
            ])

        b = np.array([3,1])
        res = simplex(A,b,c,1)

    #PRIMER ZA TESTIRANJE IZLAZA AKO JE DELJENJE SLOBODNE I PIVOT KOLONE SVUDA NEGATIVNO
    if(0):
        # y = 2x[1] - x[2]
        
        c = np.array([2,-1])

        # -3x[1] +2x[2] <= 2
        # 2x[1] -4x[2] <= 3
        # -1x[1] +1x[2] <= 6

        A = np.array([
            [-3,2],
            [2,-4],
            [-1,1]
            ])

        b = np.array([2,3,6])
        res = simplex(A,b,c,0)

    if(0):
        # y = 2x[1] - x[2]
        
        c = np.array([2,-1,5,6,7])

        # -3x[1] +2x[2] <= 2
        # 2x[1] -4x[2] <= 3
        # -1x[1] +1x[2] <= 6

        A = np.array([
            [-3,2,4,-6,8],
            [2,-4,-1,0,67],
            [-1,1,45,625,-5],
            [23,45,7,-89,-420],
            [23,567,2,-654,90]
            ])

        b = np.array([2,3,6,90,45])
        res = simplex(A,b,c,0)


    prettyprint(res)
    #print(res)




if __name__ == "__main__":
    main() 