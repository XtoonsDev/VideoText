import os
import cv2

# Chemin du dossier source et du dossier d'export
dossier_source = "source/"
dossier_export = "export/"

# Vérifier si le dossier d'export existe, sinon le créer
if not os.path.exists(dossier_export):
    os.makedirs(dossier_export)

# Définir les positions possibles
positions = {
    1: ('left', 'top'),
    2: ('left', 'bottom'),
    3: ('right', 'top'),
    4: ('right', 'bottom'),
    5: ('center', 'top'),
    6: ('center', 'bottom'),
    7: ('center', 'center'),
    8: ('left', 'center'),
    9: ('right', 'center')
}

# Parcourir les fichiers du dossier source
for fichier in os.listdir(dossier_source):
    if fichier.endswith(".mp4"):  # S'assurer que le fichier est une vidéo
        chemin_source = os.path.join(dossier_source, fichier)
        chemin_export = os.path.join(dossier_export, f"mod_{fichier}")

        # Charger la vidéo
        cap = cv2.VideoCapture(chemin_source)
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Définir le texte à ajouter
        texte = u"TOM Tom TOM Président Directeur Général"

        # Définir le moment où le texte doit apparaître (en secondes)
        debut_texte = 0  # Le texte apparaîtra après 5 secondes
        frame_debut_texte = debut_texte * fps

        # Définir la durée d'affichage du texte (en secondes)
        duree_texte = 7  # Le texte restera affiché pendant 3 secondes
        frame_duree_texte = duree_texte * fps

        # Demander à l'utilisateur de choisir une position pour le texte
        print(f"\nChoisissez une position pour le texte (pour {fichier}) :")
        for key, value in positions.items():
            print(f"{key}: {value}")

        choix = int(input("Entrez le numéro de la position choisie : "))

        # Vérifier si le choix de position est valide
        if choix not in positions:
            print("Choix invalide. Veuillez entrer un numéro de position valide.")
            continue

        position_texte = positions[choix]

        # Traitement des frames
        frames_modifiees = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frames_modifiees.append(frame.copy())

            # Si l'on est dans la plage de frames où le texte doit être affiché
            if frame_debut_texte <= cap.get(cv2.CAP_PROP_POS_FRAMES) < frame_debut_texte + frame_duree_texte:
                font = cv2.FONT_HERSHEY_SIMPLEX

                epaisseur = 2
                taille = 1
                couleur = (39, 232, 84)  # Couleur verte (Couleur RGB)

                # Récupérer les dimensions du texte
                (dimensions_texte, _) = cv2.getTextSize(texte, font, taille, epaisseur)

                # Récupérer les dimensions de l'image
                hauteur, largeur, _ = frame.shape

                # Calculer la position en fonction de la position choisie
                if position_texte[0] == 'left':
                    position_x = 50
                elif position_texte[0] == 'right':
                    position_x = largeur - dimensions_texte[0] - 50
                else:  # Si la position est 'center'
                    position_x = (largeur - dimensions_texte[0]) // 2

                if position_texte[1] == 'top':
                    position_y = dimensions_texte[1] + 50
                elif position_texte[1] == 'bottom':
                    position_y = hauteur - 50
                else:  # Si la position est 'center'
                    position_y = (hauteur + dimensions_texte[1]) // 2

                position = (position_x, position_y)

                # Dans la boucle où le texte est ajouté à la vidéo
                frame = cv2.putText(frame, texte, position, font, taille, couleur, epaisseur, cv2.LINE_AA)

                frames_modifiees[-1] = frame

        # Libérez la ressource vidéo
        cap.release()

        # Écrivez les frames modifiées en tant que nouvelle vidéo
        if frames_modifiees:
            out = cv2.VideoWriter(chemin_export, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frames_modifiees[0].shape[1], frames_modifiees[0].shape[0]))
            for frame in frames_modifiees:
                out.write(frame)
            out.release()
