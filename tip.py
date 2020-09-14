import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Cria as variáveis do problema
foodRating = ctrl.Antecedent(np.arange(0, 11, 1), 'foodRating')
serviceRating = ctrl.Antecedent(np.arange(0, 11, 1), 'serviceRating')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# Cria automaticamente o mapeamento entre valores nítidos e difusos
# usando uma função de pertinência padrão (triângulo)
foodRating.automf(names=['péssima', 'comível', 'deliciosa'])


# Cria as funções de pertinência usando tipos variados
serviceRating['ruim'] = fuzz.trimf(serviceRating.universe, [0, 0, 5])
serviceRating['aceitável'] = fuzz.gaussmf(serviceRating.universe, 5, 2)
serviceRating['excelente'] = fuzz.gaussmf(serviceRating.universe, 10,3)

tip['baixa'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['média'] = fuzz.trapmf(tip.universe, [0, 13,15, 25])
tip['alta'] = fuzz.trimf(tip.universe, [15, 25, 25])

rule1 = ctrl.Rule(serviceRating['excelente'] | foodRating['deliciosa'], tip['alta'])
rule2 = ctrl.Rule(serviceRating['aceitável'], tip['média'])
rule3 = ctrl.Rule(serviceRating['ruim'] & foodRating['péssima'], tip['baixa'])

tip_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tip_simulador = ctrl.ControlSystemSimulation(tip_ctrl)

# Entrando com alguns valores para qualidade da foodRating e do serviço
tip_simulador.input['foodRating'] = 3.5
tip_simulador.input['serviceRating'] = 9.4

# Computando o resultado
tip_simulador.compute()
print(tip_simulador.output['tip'])