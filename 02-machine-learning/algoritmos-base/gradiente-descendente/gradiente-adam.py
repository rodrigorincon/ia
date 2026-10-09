from matplotlib import pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler

prova1 = [34.623659624517, 30.2867107682261, 35.8474087699387, 60.1825993862098, 79.0327360507101, 45.0832774766834, 61.1066645368477, 75.0247455673889, 76.0987867022626, 84.4328199612004, 95.8615550709357, 75.0136583895825, 82.3070533739948, 69.3645887597094, 39.5383391436722, 53.9710521485623, 69.0701440628303, 67.9468554771162, 70.6615095549944, 76.978783727475, 67.3720275457088, 89.6767757507208, 50.534788289883, 34.2120609778679, 77.9240914545704, 62.2710136700463, 80.1901807509566, 93.114388797442, 61.830206023126, 38.7858037967942, 61.379289447425, 85.4045193941165, 52.1079797319398, 52.0454047683183, 40.2368937354511, 54.6351055542482, 33.9155001090689, 64.1769888749449, 74.7892529594154, 34.1836400264419, 83.9023936624916, 51.5477202690618, 94.4433677691785, 82.3687537571392, 51.0477517712887, 62.2226757612019, 77.1930349260136, 97.7715992800023, 62.0730637966765, 91.5649744980744, 79.9448179406693, 99.2725269292572, 90.5467141139985, 34.5245138532001, 50.2864961189907, 49.5866772163203, 97.6456339600777, 32.5772001680931, 74.248691367216, 71.7964620586338, 75.3956114656803, 35.2861128152619, 56.2538174971162, 30.058822446698, 44.6682617248089, 66.5608944724295, 40.4575509837516, 49.0725632190884, 80.27957401467, 66.7467185694404, 32.7228330406032, 64.0393204150601, 72.3464942257992, 60.4578857391896, 58.840956217268, 99.8278577969213, 47.2642691084817, 50.4581598028599, 60.4555562927153, 82.2266615778557, 88.9138964166533, 94.834506724302, 67.3192574691753, 57.2387063156986, 80.3667560017127, 68.4685217859111, 42.0754545384731, 75.4777020053391, 78.6354243489802, 52.3480039879411, 94.0943311251679, 90.4485509709636, 55.4821611406959, 74.4926924184304, 89.8458067072098, 83.4891627449824, 42.2617008099817, 99.3150088051039, 55.340017560037, 74.7758930009277]
prova2 = [78.0246928153624, 43.894997524001, 72.9021980270836, 86.3085520954683, 75.3443764369103, 56.3163717815305, 96.5114258848962, 46.5540135411654, 87.420569719268, 43.5333933107211, 38.2252780579509, 30.6032632342801, 76.481963302356, 97.7186919618861, 76.0368108511588, 89.2073501375021, 52.7404697301677, 46.6785741067313, 92.9271378936483, 47.5759636497553, 42.8384383202918, 65.7993659274524, 48.8558115276421, 44.2095285986629, 68.9723599933059, 69.9544579544759, 44.8216289321835, 38.8006703371321, 50.2561078924462, 64.9956809553958, 72.807887313171, 57.0519839762712, 63.1276237688172, 69.4328601204522, 71.1677480218488, 52.2138858806112, 98.8694357422061, 80.9080605867082, 41.5734152282443, 75.2377203360134, 56.3080462160533, 46.8562902634998, 65.5689216055905, 40.6182551597062, 45.82270145776, 52.0609919483668, 70.4582000018096, 86.7278223300282, 96.7688241241398, 88.696292545466, 74.1631193504376, 60.9990309984499, 43.3906018065003, 60.3963424583717, 49.8045388132306, 59.8089509945327, 68.861572724206, 95.5985476138788, 69.8245712265719, 78.4535622451505, 85.7599366733162, 47.0205139472342, 39.2614725105802, 49.5929738672369, 66.4500861455891, 41.0920980793697, 97.5351854890994, 51.8832118207397, 92.1160608134408, 60.9913940274099, 43.3071730643006, 78.0316880201823, 96.227592967614, 73.0949980975804, 75.8584483127904, 72.3692519338389, 88.4758649955978, 75.8098595298246, 42.5084094357222, 42.7198785371646, 69.8037888983547, 45.6943068025075, 66.5893531774792, 59.5142819801296, 90.9601478974695, 85.5943071045201, 78.8447860014804, 90.4245389975396, 96.6474271688564, 60.7695052560259, 77.1591050907389, 87.508791764847, 35.5707034722887, 84.8451368493014, 45.3582836109166, 48.3802857972818, 87.1038509402546, 68.7754094720662, 64.9319380069486, 89.5298128951328]
aprovado = [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]

###### FUNÇÕES PARA O MODELO DE REGRESSAO LOGISTICA

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def maxima_verossimilhanca(w, X, y):
    n = len(X)
    
    sigmoid_res = sigmoid(X @ w.T) # X @ w.T é o produto matricial entre X e W transposta (pesos)
    # Evita log(0) adicionando uma pequena constante de estabilidade (eps)
    eps = 1e-15
    sigmoid_res = np.clip(sigmoid_res, eps, 1 - eps)
    
    logit = np.log(sigmoid_res)
    parte1 = np.multiply(-y, logit) # -y * log(ŷ)
    parte2 = np.multiply(1 - y, np.log(1 - sigmoid_res)) # (1 - y) * log(1 - ŷ)

    somatorio = np.sum(parte1 - parte2)
    return somatorio / n

# beta1: taxa de decaimento para o 1º momento (média móvel dos gradientes)
# beta2: taxa de decaimento para o 2º momento (média móvel dos gradientes ao quadrado)
def gradiente_descendente_adam(w, X, y, tx_aprendizado=0.01, num_epocas=1000, beta1=0.9, beta2=0.999):
    epsilon = 1e-8 # evita divisão por zero

    # array para armazenar o resultado do custo em cada época para visualizarmos depois ele descendo o gradiente
    custo_por_epoca = np.zeros(num_epocas)

    # Inicialização dos momentos m (1º momento) e v (2º momento) com zeros
    m = np.zeros_like(w)
    v = np.zeros_like(w)

    for step in range(1, num_epocas + 1):
        # Cálculo da derivada da função de custo (até aqui tudo igual ao normal)
        sigmoid_res = sigmoid(X @ w.T)
        derivada_custo = np.sum((sigmoid_res - y) * X, axis=0)

        # Atualização dos momentos (m e v) - AQUI COMEÇA AS MUDANÇAS
        m = beta1 * m + (1 - beta1) * derivada_custo
        v = beta2 * v + (1 - beta2) * (derivada_custo ** 2)

        # Correção de viés (Bias Correction). Ao passar das rodadas vai dividindo por valores maiores (tendendo a 1)
        m_chapeu = m / (1 - beta1 ** step)
        v_chapeu = v / (1 - beta2 ** step)

        # Atualização dos pesos com a regra do Adam (troca a derivada pelo m_chapeu e a divisão pela quantidade de dados por v_chapeu)
        w = w - (tx_aprendizado / (np.sqrt(v_chapeu) + epsilon)) * m_chapeu

        # 5. Cálculo do custo da época
        custo_por_epoca[step - 1] = maxima_verossimilhanca(w, X, y)
    
    return w[0], custo_por_epoca

###### PREPARA OS DADOS

X = [prova1, prova2]
y = [aprovado]
num_vars_independentes = len(X)

X = np.array(X).T 
y = np.array(y).T

# Padronização dos dados (z-score)
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Guarda média e desvio padrão para uso no predict
media = scaler.mean_
desvio = scaler.scale_

# Adiciona a coluna de 1s para o intercepto (bias)
X = np.hstack([np.ones((X.shape[0], 1)), X])

###### COMEÇA A REGRESSAO COM ADAM

# Inicia os pesos com valores aleatórios
w = np.random.rand(1, num_vars_independentes + 1)

# Parâmetros de treino
tx_aprendizado = 0.1  # Com Adam, podemos usar uma taxa maior que o SGD padrão
total_iteracoes = 1000

# Executa o treino com Adam
pesos, lista_custos = gradiente_descendente_adam(w, X, y, tx_aprendizado, total_iteracoes, beta1=0.9, beta2=0.999)

# Plotando a curva de custo
fig, ax = plt.subplots()  
ax.plot(np.arange(total_iteracoes), lista_custos, 'b-', label='Adam')  
ax.set_xlabel('Iterações')  
ax.set_ylabel('Custo')  
ax.set_title('Erro vs. Iteracaoes - Adam')
plt.show()

print('\n\npesos: ', pesos,'\n\n')

###### FAZ PREDIÇÕES PARA NOVOS VALORES
threshold = 0.5

def predict(pesos, X_novo, media, desvio):
    # Padronização usando os parâmetros salvos do conjunto de treino
    X_padronizado = (X_novo - media) / desvio
    # Adiciona bias
    X_padronizado = np.insert(X_padronizado, 0, 1, axis=1)
    return sigmoid(X_padronizado @ pesos.T)

# Teste 1
estudante1 = np.array([[45, 85]])
resposta = predict(pesos, estudante1, media, desvio)
print('Probabilidade de aprovação do estudante 1: ', resposta)
print('O estudante 1 foi aprovado? ', resposta >= threshold)

# Teste 2
estudante2 = np.array([[90, 90]])
resposta = predict(pesos, estudante2, media, desvio)
print('Probabilidade de aprovação do estudante 2: ', resposta)
print('O estudante 2 foi aprovado? ', resposta >= threshold)