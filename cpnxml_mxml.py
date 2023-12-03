import csv
import os
import xml.etree.ElementTree as ET
from lxml import etree
    
def read_cpnxml_file(fichier_cpnxml):
    # Lire la première partie (nombre ou autre donnée)
    """with open(cpnxml_path, 'r') as fichier:
        premiere_ligne = fichier.readline().strip()
        print(f"Première ligne : {premiere_ligne}")
        # Lire le reste du fichier comme un document XML
        #contenu_xml = fichier.read()"""
    # Ouvrir le fichier en mode lecture
    with open(fichier_cpnxml, 'r') as fichier:
        # Lire la première ligne (qui n'est pas XML)
        premiere_ligne = fichier.readline().strip()
        
        # Lire le reste du fichier comme un document XML
        contenu_xml = fichier.read()

    return premiere_ligne, contenu_xml

def write_mxml_file(fichier_mxml, input_folder):

    with open(fichier_mxml, 'w') as fichier:
        #déclaration du fichier XML
        fichier.write('<?xml version="1.0" encoding="UTF-8" ?> \n')
        fichier.write('<WorkflowLog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://is.tm.tue.nl/research/processmining/SAMXML.xsd" description="CPN Tools simulation log"> \n')
        fichier.write('    <Source program="CPN Tools simulation"/>\n ')
        fichier.write('    <Process id="DEFAULT" description="Simulated process"> \n')
        # Parcourir tous les fichiers dans le dossier
        for filename in os.listdir(input_folder):
            if filename.endswith(".cpnxml"):
                cpnxml_path = os.path.join(input_folder, filename)
                id, xml = read_cpnxml_file(cpnxml_path)

                fichier.write(f'        <ProcessInstance id="{id}" description="Simulated process instance"> n')
                fichier.write(f'{xml} \n')
                fichier.write('		</ProcessInstance> \n')
        fichier.write('    </Process> \n')
        fichier.write('</WorkflowLog> \n')


write_mxml_file(fichier_mxml = 'new_data_mxml.mxml', input_folder = "logsCPN")
