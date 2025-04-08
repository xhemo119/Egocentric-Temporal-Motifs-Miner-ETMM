import numpy as np
import matplotlib.pyplot as plt

# Beispielwerte
t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
x = [1.9, 1.3, 1.6, 2.9, 1.9, 1.3, 1.6, 2.9, 1.9, 1.3, 1.6, 2.9, 1.9, 1.3, 1.6, 2.9, 1.9, 1.3, 1.6, 2.9, 1.9, 1.3, 1.6, 2.9, 1.9, 1.3, 1.6, 2.9, 1.9, 1.3, 1.6]

# Standard-Schrift (kein LaTeX)
plt.rcParams['text.usetex'] = False

# Plot
plt.plot(t, x, 'k', linewidth=2)
plt.xlabel('t', fontsize = 22)
plt.ylabel('x', fontsize = 22)
plt.title('ETNS 100', fontsize=22, pad=22)

# Tick-Beschriftungen & Striche (26 pt Schrift, dick & lang)
plt.tick_params(
    axis='both',
    labelsize=22,
    width=1,
    length=6,
    direction='inout'
)


# Achsenlinien (Rahmen) dicker machen
for spine in plt.gca().spines.values():
    spine.set_linewidth(1)

# Achsenbereich: t-Achse beginnt etwas vor 0
plt.xlim(-1, 30)
plt.ylim(0, 7)

# Anzeigen
plt.tight_layout()
plt.show()



