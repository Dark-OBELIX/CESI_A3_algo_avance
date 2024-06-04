import numpy as np
import matplotlib.pyplot as plt

xmax = 100
x = np.arange(0, xmax)

# Les contraintes
y1 = 100 - x
y2 = (5 - 10*x)/20 
y3 = np.minimum(50, 0*x + 80) 

ymax = 100 

# Tracer les graphiques
plt.plot(x, y1, color='red', label='Contrainte de production')
plt.plot(x, y2, color='blue', label='Contrainte de coût')
plt.plot(x, y3, color='green', label='Contrainte de composition')

plt.fill_between(x, y1, ymax, color='lightgrey')
plt.fill_between(x, y2, y3, color='lightgrey')

plt.ylim(0, ymax)
plt.xlim(0, xmax)

plt.xlabel('Quantité de bonbons produits (kg)')
plt.ylabel('Quantité des ingrédients (kg)')
plt.legend()
plt.title('Problème d\'optimisation')

plt.gcf().set_size_inches(18, 10)
plt.show()
