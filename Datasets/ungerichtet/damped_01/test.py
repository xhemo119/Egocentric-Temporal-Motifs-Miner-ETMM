import numpy as np

def log_einzeln(x, alpha=0.7):
    x = float(x)
    log_wert = alpha * np.log(x + 1)
    result = np.exp(log_wert) - 1
    return str(round(min(result, x), 2))



ergebnis = log_einzeln(1, alpha=0.7)
print(ergebnis)