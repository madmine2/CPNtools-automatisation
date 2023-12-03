import os
import xml.etree.ElementTree as ET
from lxml import etree

def convert_folder_to_xml(input_folder, output_file):
    # Créer le document XML global
    global_root = ET.Element("GlobalRootElement")
    i = 0
    # Parcourir tous les fichiers dans le dossier
    for filename in os.listdir(input_folder):
        if filename.endswith(".cpnxml"):
            cpnxml_path = os.path.join(input_folder, filename)

            #print("Chemin du fichier CPNXML :", cpnxml_path)
            # Charger le fichier .cpnxml
            #tree = ET.parse(cpnxml_path)
            try:
                tree = ET.parse(cpnxml_path)
                root = tree.getroot()

                # Ajouter le contenu du fichier .cpnxml au document global
                global_root.extend(root)
            except ET.ParseError as e:
                print(f"Erreur lors de la lecture de {cpnxml_path}: {e}")
                i += 1

    print(i)
    if 'tree' in locals():  # Vérifiez si 'tree' est déclarée
        # Créer un nouvel arbre avec le document global
        global_tree = ET.ElementTree(global_root)

        # Sauvegarder en tant que fichier .xml
        global_tree.write(output_file)


def add_root_element(cpnxml_file_path):

    #try:

    # Charger le fichier .cpnxml
    tree = etree.parse(cpnxml_file_path)
    print(f'tree {tree}')
    root = tree.getroot()
    print(root)

    # Vérifier si l'élément racine existe
    if root.tag != 'Root':
        print(root)
        # Créer un nouvel élément racine et déplacer le contenu existant en dessous
        new_root = etree.Element('Root')
        new_root.extend(root)

        # Créer un nouvel arbre avec le nouvel élément racine
        new_tree = etree.ElementTree(new_root)

        # Sauvegarder en tant que fichier .xml
        new_tree.write(cpnxml_file_path)
    #except ET.ParseError as e:
    #    print(f"Erreur lors de la lecture de {cpnxml_file_path}: {e}")

def add_root_to_folder(input_folder):
    # Parcourir tous les fichiers dans le dossier
    for filename in os.listdir(input_folder):
        if filename.endswith(".cpnxml"):
            cpnxml_file_path = os.path.join(input_folder, filename)
            add_root_element(cpnxml_file_path)

add_root_to_folder('logsCPN')

# Exemple d'utilisation
convert_folder_to_xml('logsCPN', 'data.xml')

