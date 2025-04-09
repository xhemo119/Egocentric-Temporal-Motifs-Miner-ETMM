import numpy as np
import matplotlib.pyplot as plt

# Zeitachse (t) und drei verschiedene Datensätze (x1, x2, x3)
t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
x1 = [617.6, 651.9, 631.5, 494.1, 613.0, 574.6, 606.5, 654.4, 686.7, 599.8, 604.2, 656.8, 662.8, 661.4, 661.2, 688.9, 589.0, 572.6, 601.0, 571.8, 614.5, 600.9, 621.9, 594.2, 605.6, 633.9, 640.2, 547.8, 614.9, 629.5, 679.8]
x2 = [606.9, 640.5, 628.6, 489.7, 611.6, 564.9, 595.9, 654.6, 683.7, 598.6, 596.5, 645.5, 659.5, 661.6, 650.1, 687.1, 586.2, 569.3, 590.6, 566.3, 611.2, 597.0, 618.1, 583.3, 601.3, 629.7, 634.3, 537.6, 602.9, 625.2, 661.6]
x3 = [596.6, 626.9, 628.4, 483.4, 602.2, 562.3, 585.9, 642.9, 682.1, 596.1, 591.2, 633.1, 645.3, 652.2, 647.1, 686.7, 576.9, 556.6, 580.0, 560.8, 607.6, 587.2, 607.2, 573.6, 590.6, 626.2, 631.4, 534.7, 597.1, 610.2, 654.5]

# Plot-Style (kein LaTeX, Schriftgrößen etc.)
plt.rcParams['text.usetex'] = False
plt.style.use('default')  # Zurücksetzen auf Standard-Design

# Plot der drei Funktionen mit durchgezogenen Linien (nur Farben unterschiedlich)
plt.plot(t, x1, 'k-', linewidth=2, label='ETNS 100-100 (k = 2)')  # Schwarz, durchgezogen
plt.plot(t, x2, 'r-', linewidth=2, label='ETNS 1000-1000 (k = 3)')  # Rot, durchgezogen
plt.plot(t, x3, 'b-', linewidth=2, label='ETNS 10000-10000 (k = 4)')  # Blau, durchgezogen

# Achsenbeschriftungen & Titel
plt.xlabel('t', fontsize=22)
plt.ylabel('x', fontsize=22)
plt.title('Evolution of the third ETNS in all three $k$', fontsize=22, pad=22)

# Y-Achse: Werte mit Prozentzeichen (%) formatieren
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x}%'))

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
plt.ylim(0, 900)

# Layout optimieren und anzeigen
plt.tight_layout()
plt.show()