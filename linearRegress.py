from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
U=[1,50,100,150,200,300,450]
#V=[0,0.0182639999593448/1641,0.03401170201777859/2365,0.05032578200007265/2565,0.058042711959387816/2571,11150.190899383026/2665,47920.624717783016/2543] #tempi coda gemma
#V=[6,40675/2565,76101/2665,112797/2543] #latenza gemma server
V=[5.4,8.4,11.94,16.221,20.8,29.184,45.224] #gemma tempo di risposta ccust
#V=[591/109,13396/1641,27473/2365,40494/2565,52086/2571,64614/2665,64565/2543]  #Tempo di inferenza
result = linregress(U, V)
print(result.intercept, result.intercept_stderr)
# --- Fitting lineare (grado 1) ---
coeffs1 = np.polyfit(U, V, 1)  # [slope, intercept]
poly1 = np.poly1d(coeffs1)

print("Fitting lineare con numpy.polyfit:")
print(poly1)  # stampa y = m*x + q

# --- Fitting polinomiale (grado 2 e 3 come esempio) ---
coeffs2 = np.polyfit(U, V, 2)
coeffs3 = np.polyfit(U, V, 3)

poly2 = np.poly1d(coeffs2)
poly3 = np.poly1d(coeffs3)

# --- Plot ---
U_smooth = np.linspace(min(U), max(U), 500)

plt.scatter(U, V, color="black", label="Dati")
plt.plot(U_smooth, poly1(U_smooth), "r--", label="Lineare (grado 1)")
plt.plot(U_smooth, poly2(U_smooth), "b-", label="Polinomiale grado 2")
plt.plot(U_smooth, poly3(U_smooth), "g-", label="Polinomiale grado 3")
plt.xlabel("U")
plt.ylabel("V")
plt.legend()
plt.show()