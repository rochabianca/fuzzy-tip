import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

foodRating = ctrl.Antecedent(np.arange(0, 11, 1), 'foodRating')
serviceRating = ctrl.Antecedent(np.arange(0, 11, 1), 'serviceRating')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

foodRating.automf(names=['horrível', 'ok', 'deliciosa'])

serviceRating['ruim'] = fuzz.trimf(serviceRating.universe, [0, 0, 5])
serviceRating['aceitável'] = fuzz.gaussmf(serviceRating.universe, 5, 2)
serviceRating['excelente'] = fuzz.gaussmf(serviceRating.universe, 10,3)

tip['baixa'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['média'] = fuzz.trapmf(tip.universe, [0, 13,15, 25])
tip['alta'] = fuzz.trimf(tip.universe, [15, 25, 25])

rule1 = ctrl.Rule(serviceRating['excelente'] | foodRating['deliciosa'], tip['alta'])
rule2 = ctrl.Rule(serviceRating['aceitável'], tip['média'])
rule3 = ctrl.Rule(serviceRating['ruim'] & foodRating['horrível'], tip['baixa'])

tip_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tip_simulador = ctrl.ControlSystemSimulation(tip_ctrl)

print('Qual a nota da comida? (0-10)')
tip_simulador.input['foodRating'] = int(input())
print('Qual a nota do serviço? (0-10)')
tip_simulador.input['serviceRating'] = int(input())
print('Qual o valor da conta?
totalPrice = int(input())

tip_simulador.compute()
tipPercent = round(tip_simulador.output['tip'])
tipValue = totalPrice*tipPercent/100
print('Sua gorgeta é: ' + str(tipPercent)+ '%, ou R$'+ str(tipValue))