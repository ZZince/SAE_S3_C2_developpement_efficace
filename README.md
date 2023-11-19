# SAE_C2_Developement_Efficace
 
**Réalisé par Florient Artu (BUT2-TPD)**

## Liste des réalisations

- Défi basique
- Algorithme de génération de gradient 

## Réalisation tentée sans réussite

- Comparaison du temps de traitement entre Python et C++

## Exécution des programmes

- Python:
```bash
pip install -r requierements.txt
python3 gui.py
```

- C++:
```bash
sudo apt-get install libopencv-dev
g++ -o test_speed_cpp test_speed_cpp.cpp `pkg-config --cflags --libs opencv4`
./test_speed_cpp
```

- Executable: Lancez l'éxécutable app.exe (sous Windows, compilé à partir de gui.py)

## Liste des dossiers et fichiers

- gradient: Image utilisable pour tester les programmes
- gui.py: Fichier source de l'interface
- image_traitement.py: Fichier source des fonctions de traitement
- requierement.txt: Fichier des bibliothéques Python utilisées
- test_speed_cpp.cpp: Fichier source de la tentative de test du temps de traitement en C++
- test_speed_python.py: Fichier source du test du temps de traitement en Python
- app.exe: Fichier exécutable de l'interface

