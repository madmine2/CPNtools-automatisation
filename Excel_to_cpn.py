# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 15:52:45 2023

@author: lison
"""
#pip install tkcalendar

from datetime import datetime
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import numpy as np


def filtrer_et_modifier_cpn():
    date_debut_str = date_debut_var.get()
    date_fin_str = date_fin_var.get()

    # Convertir les dates de type str en objets datetime
    date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d')
    date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d')
    jours_selectionnes = np.array([jours_semaine[i] if jours_vars[i].get() == "1" else "pas selectionné" for i, jours in enumerate(jours_vars)])
    print(jours_selectionnes)

    # Vérifier si au moins un jour de la semaine est sélectionné
    if not any(jours_selectionnes):
        messagebox.showinfo("Avertissement", "Veuillez sélectionner au moins un jour de la semaine.")
        return

    # Filtrer le DataFrame en fonction de la période et des jours sélectionnés
    df_filtre = df_trace[
        (df_trace['Jour'] >= date_debut) &
        (df_trace['Jour'] <= date_fin) &
        df_trace['Jour_de_la_semaine'].isin(jours_selectionnes)
    ]

    # Modifier le contenu du fichier .cpn
    expression_reguliere = r'<initmark id="ID1414975589">.*? version="4\.0\.1">1`(.*?)</text>'
    valeurs_colonne_1 = df_filtre['1`'].tolist()
    valeurs_colonne_1_concatenees = "".join(map(str, valeurs_colonne_1))
    valeurs_colonne_1_modifiees = "\n" + valeurs_colonne_1_concatenees.replace("`(", "`\n(")
    modele_substitution = 'version="4.0.1">1`{}</text>'.format(valeurs_colonne_1_modifiees.replace(", ", ",\n"))
    contenu_cpn_modifie = re.sub(
        r'(<initmark id="ID1414975589">.*? version="4\.0\.1">1`)(.*?)(</text>)',
        lambda match: match.group(1) + valeurs_colonne_1_modifiees.replace(", ", ",\n") + match.group(3),
        cpn_file,
        flags=re.DOTALL
    )

    # Écrire le contenu modifié dans un nouveau fichier .cpn
    with open('new_cpn_data.cpn', 'w') as fichier_cpn_modifie:
        fichier_cpn_modifie.write(contenu_cpn_modifie)

# lecture du fichier excel
excel_file = pd.ExcelFile('dataset.xlsx')
df_trace = excel_file.parse('trace')
df_trace['Jour_de_la_semaine'] = df_trace['Jour'].dt.day_name()
df_trace = df_trace.loc[:, ~df_trace.columns.str.contains('^Unnamed')]

#lecture du fichier .cpn existant
with open('chwapi.cpn', 'r') as fichier:
    cpn_file = fichier.read()

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Choisir une période et des jours de la semaine")

# Création des widgets de calendrier pour la date de début et de fin
label_date_debut = ttk.Label(root, text="Date de début:")
label_date_debut.grid(row=0, column=0, padx=10, pady=10)

date_debut_var = tk.StringVar()
choix_date_debut = DateEntry(root, textvariable=date_debut_var, date_pattern='yyyy-mm-dd', locale='fr_FR')
choix_date_debut.grid(row=0, column=1, padx=10, pady=10)

label_date_fin = ttk.Label(root, text="Date de fin:")
label_date_fin.grid(row=1, column=0, padx=10, pady=10)

date_fin_var = tk.StringVar()
choix_date_fin = DateEntry(root, textvariable=date_fin_var, date_pattern='yyyy-mm-dd', locale='fr_FR')
choix_date_fin.grid(row=1, column=1, padx=10, pady=10)

# Création des cases à cocher pour les jours de la semaine
label_jours = ttk.Label(root, text="Choisir les jours de la semaine:")
label_jours.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

jours_semaine = df_trace['Jour_de_la_semaine'].unique()

jours_vars = [tk.StringVar(value=True) for _ in jours_semaine]

for i, jour in enumerate(jours_semaine):
    chk_jour = ttk.Checkbutton(root, text=jour, variable=jours_vars[i])
    chk_jour.grid(row=i // 2 + 3, column=i % 2, padx=10, pady=5, sticky='w')
# Bouton pour appliquer la filtration et la modification
bouton_appliquer = ttk.Button(root, text="Appliquer", command=filtrer_et_modifier_cpn)
bouton_appliquer.grid(row=len(jours_semaine) // 2 + 4, column=0, columnspan=2, pady=10)

# Lancer l'interface utilisateur
root.mainloop()


#ici le code sans la mini interface pour choisir le jour

# #trier le df en fonction d'un jour de la semaine exemple
# jour='Monday' #à implémenter mieux que ça
# df_trace = df_trace.loc[df_trace['Jour_de_la_semaine'] == 'Monday']




# # remplacer les données du fichier .cpn par les nouvelles données
# expression_reguliere = r'<initmark id="ID1414975589">.*? version="4\.0\.1">1`(.*?)</text>'
# valeurs_colonne_1_concatenees = "".join(map(str, valeurs_colonne_1))
# valeurs_colonne_1_modifiees = "\n" + valeurs_colonne_1_concatenees.replace("`(", "`\n(")
# modele_substitution = 'version="4.0.1">1`{}</text>'.format(valeurs_colonne_1_modifiees.replace(", ", ",\n"))
# contenu_cpn_modifie = re.sub(
#     r'(<initmark id="ID1414975589">.*? version="4\.0\.1">1`)(.*?)(</text>)',
#     lambda match: match.group(1) + valeurs_colonne_1_modifiees.replace(", ", ",\n") + match.group(3),
#     cpn_file,
#     flags=re.DOTALL
# )

# # Écrire le contenu modifié dans le fichier .cpn (un autre pour pas écraser)
# with open('new_cpn_data.cpn', 'w') as fichier_cpn_modifie:
#     fichier_cpn_modifie.write(contenu_cpn_modifie)