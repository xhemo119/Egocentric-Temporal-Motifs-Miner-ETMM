import numpy as np
import matplotlib.pyplot as plt

# Zeitachse (t) und drei verschiedene Datensätze (x1, x2, x3)
t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
x1 = [817, 911, 846, 764, 817, 911, 846, 764, 817, 911, 846, 764, 817, 911, 846, 764, 817, 911, 846, 764, 817, 911, 846, 764, 817, 911, 846, 764, 817, 911, 846]
x2 = [688, 777, 721, 643, 688, 777, 721, 643, 688, 777, 721, 643, 688, 777, 721, 643, 688, 777, 721, 643, 688, 777, 721, 643, 688, 777, 721, 643, 688, 777, 721]
x3 = [571, 653, 606, 536, 571, 653, 606, 536, 571, 653, 606, 536, 571, 653, 606, 536, 571, 653, 606, 536, 571, 653, 606, 536, 571, 653, 606, 536, 571, 653, 606]

# Plot-Style (kein LaTeX, Schriftgrößen etc.)
plt.rcParams['text.usetex'] = False
plt.style.use('default')  # Zurücksetzen auf Standard-Design

# Plot der drei Funktionen mit durchgezogenen Linien (nur Farben unterschiedlich)
plt.plot(t, x1, 'k-', linewidth=2, label='ETNS 001-001-...')  # Schwarz, durchgezogen
plt.plot(t, x2, 'r-', linewidth=2, label='ETNS 0001-0001-...')  # Rot, durchgezogen
plt.plot(t, x3, 'b-', linewidth=2, label='ETNS 00001-00001-...')  # Blau, durchgezogen

# Achsenbeschriftungen & Titel
plt.xlabel('t', fontsize=22)
plt.ylabel('x', fontsize=22)
plt.title('Evolution of the second ETNS in all three $k$', fontsize=22, pad=22)

# Y-Achse: Werte mit Prozentzeichen (%) formatieren
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x}%'))

# Tick-Einstellungen (Größe, Richtung)
plt.tick_params(axis='both', labelsize=22, width=1, length=6, direction='inout')

# Legende (professionell platziert, ohne Rahmen, große Schrift)
plt.legend(
    fontsize=18,
    frameon=True,           # Rahmen AN (Kasten)
    loc='upper right',      # Position: oben rechts
    edgecolor='lightgray',      # Farbe des Rahmens
    facecolor='white',      # Hintergrundfarbe
    framealpha=1            # Keine Transparenz
)

# Achsen-Rahmen dicker machen
for spine in plt.gca().spines.values():
    spine.set_linewidth(1)

# Achsenlimits
plt.xlim(-1, 31)
plt.ylim(0, 1400)

# Layout optimieren und anzeigen
plt.tight_layout()
plt.show()