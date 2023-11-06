Ivan Mikić RA44/2020 11.11.2022
Domaći zadatak: Programiranje Simplex Metode 

Za pokretanje programa je potreban python sa ekstenzijom numpy.
Za zadatak je bio korišćen python 3.10.8
U programu su iskomentarisani svi delovi i upisane su test funkcije primera
sa vežbi koje vraćaju dobre rezultate.
Program ispisuje šta se odvija u algoritmu sve do rešenja.
Test funkcije se mogu menjati samo promenom 0 u 1 na if funkciji u kojoj se nalaze. 

Specifikacije:
Smatrano je da je ulaz u funkciju simplex(np.array A,np.array b,np.array c,int d) koji
pretpostavlja: 

	Ax <= b (matrica A sa koeficientima ispred svih
 	promenjivih u nejednakostima i vektor b sa rezultatima)

	y = cx (vektor c sa koeficientima ispred promenjivih u
	funkciji koju optimizujemo)

	Ako je d == 1 smatramo da se traži minimum
	Ako je d == 0 smatramo da se traži maksimum (standardno)

Postoji provera ulaznih parametara gde b i c moraju imati jednu dimenziju i 
gleda se da li se oni slazu sa matricom A.

Funkcija vraća vrednosti [y x1 x2 x3 ... xn] gde idu redom prvo promenjive iz
funkcije koju optimizujemo pa dodatne promenjive.

Kreirana je i funkcija prettyprint za razumniji ispis.
