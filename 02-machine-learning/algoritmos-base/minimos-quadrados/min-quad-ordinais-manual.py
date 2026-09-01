
def minimos_quadrados(x_values, y_values):
    n = len(x_values)

    # calculando os coeficientes da equação linear usando a fórmula dos minimos quadrados
    # A = coeficiente angular B = coeficiente linear

    a = (n * sum(x * y for x, y in zip(x_values, y_values)) - sum(x_values) * sum(y_values)) / (n * sum(x ** 2 for x in x_values) - sum(x_values) ** 2)

    b = (sum(y_values) - a * sum(x_values)) / n

    return a, b 

# equacao original = 3x + 2
x_values = [0, 1, 2, 3]
y_values = [2, 5, 8, 11]

a, b = minimos_quadrados(x_values, y_values)
print(f'A equação da reta de regressão linear é: y = {a:.1f}x + {b:.1f}')

# equacao original = 3x + 2 + ruído
x_values = [0, 1, 2, 3]
y_values = [1, 6, 6, 12]

a, b = minimos_quadrados(x_values, y_values)
print(f'A equação da reta de regressão linear é: y = {a:.1f}x + {b:.1f}')