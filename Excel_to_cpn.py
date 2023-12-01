# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 15:52:45 2023

@author: lison
"""

import pandas as pd
import re

# lecture du fichier excel
excel_file = pd.ExcelFile('dataset.xlsx')
df_trace = excel_file.parse('trace')
df_trace['Jour_de_la_semaine'] = df_trace['Jour'].dt.day_name()
df_trace = df_trace.loc[:, ~df_trace.columns.str.contains('^Unnamed')]
valeurs_colonne_1 = df_trace['1`'].tolist()
print(df_trace[['Jour', 'Jour_de_la_semaine']])

#lecture du fichier .cpn existant
with open('chwapi.cpn', 'r') as fichier:
    cpn_file = fichier.read()
print(cpn_file)

#trier le df en fonction d'un jour de la semaine exemple
jour='Monday' #à implémenter mieux que ça
df_trace = df_trace.loc[df_trace['Jour_de_la_semaine'] == 'Monday']

# remplacer les données du fichier .cpn par les nouvelles données
expression_reguliere = r'<initmark id="ID1414975589">.*? version="4\.0\.1">1`(.*?)</text>'
valeurs_colonne_1_concatenees = "".join(map(str, valeurs_colonne_1))
valeurs_colonne_1_modifiees = "\n" + valeurs_colonne_1_concatenees.replace("`(", "`\n(")
modele_substitution = 'version="4.0.1">1`{}</text>'.format(valeurs_colonne_1_modifiees.replace(", ", ",\n"))
contenu_cpn_modifie = re.sub(
    r'(<initmark id="ID1414975589">.*? version="4\.0\.1">1`)(.*?)(</text>)',
    lambda match: match.group(1) + valeurs_colonne_1_modifiees.replace(", ", ",\n") + match.group(3),
    cpn_file,
    flags=re.DOTALL
)

# Écrire le contenu modifié dans le fichier .cpn (un autre pour pas écraser)
with open('new_cpn_data.cpn', 'w') as fichier_cpn_modifie:
    fichier_cpn_modifie.write(contenu_cpn_modifie)