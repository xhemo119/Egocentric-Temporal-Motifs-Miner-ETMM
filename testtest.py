import numpy as np
import matplotlib.pyplot as plt


def format_long_labels(labels, k):                                                  # teilt lange Zahlen in mehrere Zeilen auf und schreibt sie untereinander
    formatted_labels = []
    for label in labels:
        split_label = '\n'.join([label[i:i+k] for i in range(0, len(label), k)])
        formatted_labels.append(split_label)
    return formatted_labels


def draw_barChart(S_keys, S_values_list, k, spacing=2, width=0.4, legend_labels=None):
    S_keys_length = np.arange(len(S_keys)) * spacing  # Abstand zwischen Bars vergrößern

    if legend_labels is None:
        legend_labels = [f"Werte {i+1}" for i in range(len(S_values_list))]

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Farben für verschiedene Wertegruppen
    for i, S_values in enumerate(S_values_list):
        plt.bar(S_keys_length + i * (width + 0.1), S_values, align='center', alpha=0.7, width=width, label=legend_labels[i], color=colors[i % len(colors)])

    filtered_S_keys = [key[2:] for key in S_keys]
    print(filtered_S_keys)
    formatted_labels = format_long_labels(filtered_S_keys, k+1)

    plt.xticks(ticks=S_keys_length, labels=formatted_labels, ha='center')

    plt.legend()  # Legende anzeigen
    plt.show()



S_keys = ['123456', '789012', '345678', '901234']
S_values1 = [10, 20, 15, 25]  # Erste Datenreihe
S_values2 = [5, 15, 10, 20]   # Zweite Datenreihe
S_values3 = [8, 12, 18, 22]   # Dritte Datenreihe

draw_barChart(S_keys, [S_values1, S_values2, S_values3], k=3, legend_labels=["Gruppe A", "Gruppe B", "Gruppe C"])







