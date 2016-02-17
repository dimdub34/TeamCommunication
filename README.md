# Team Communication

This a program for LE2M ([https://github.com/dimdub34/le2m-v2.1](https://github.com/dimdub34/le2m-v2.1)).  

This part must be put in the directory le2m/parts. This way, LE2M will find it and will be able to load it. 


## Réalisation d'une session de TeamCommunication
Lancer serverrun.py, puis menu Fichier/Charger une partie. Sélectionner alors Dictator et TeamCommunication. Penser à choisir le dossier dans lequel enregistrer la base de données et définir le nom de fichier de cette base.  Si la session n'est pas une session de test décocher la case correspondante.  

_remarque:  d'une session à l'autre enregistrer la base dans le même dossier et avec le même nom de fichier afin que les données de toutes les sessions soient dans la même base._

Une fois chargées chacune de ces parties ajoute un sous-menu au menu "Parties" sur le serveur. Chaque partie est gérée depuis son sous-menu: configuration, fixation du traitement ...

Connecter les clients. Pour la langue du client, utiliser l'option -l fr ou -l en. Peut-être préparer un raccourci pour un lancement en français et un raccourci pour un lancement en anglais. 

_remarque: pour des tests l'option -s lance le client en mode simulation, c'est à dire que le programme prend les décisions tout seul et sans interface graphique. Avec l'option -a le client se lanche en mode automatique. Avec ce mode le programme prend les décisions tout seul également mais cette fois avec les interfaces graphiques._

### Configuration et lancement de TeamCommunication
Avant de démarrer la partie il faut la configurer, en cliquant sur le sous-menu "Configurer". Cet sous-menu ouvre une boîte de dialogue qui permet de configurer la partie: choisir le fichier grilles_0.pck qui contient les grilles pour la première séquence de jeu, définir le temps de la partie et définir le traitement. Les fichiers *.pck sont dans le sous-dossier TeamCommunication/grilles. Il est possible de générer de nouvelles grilles, me demander.  

Une fois la configuration effectuée et les clients connectés, lancer la partie en cliquant sur le bouton "Démarrer". Après confirmation cela lance la partie et fait donc afficher l'écran sur les postes clients (les fenêtres sur les postes clients peuvent mettre un peu de temps à s'afficher car au lancement le programme fait pas mal de choses). Les sujets jouent au jeu pendant le temps imparti. A la fin de ce temps ils doivent répondre à trois questions. L'enchaînement est automatique, il n'y a pas besoin d'intervenir.  

_remarque: pendant que les sujets jouent l'expérimentateur peut suivre les ouvertures de grilles, les essais et les messages échangés (si traitement avec\_communication)._

Lorsque la séquence est terminée, il faut de nouveau configurer la partie avant de lancer la nouvelle séquence: charger les grilles de la seconde séquence (grilles_1.pck), le temps de jeu et le traitement. Une fois tout cela effectué, lancer la partie en cliquant sur "Démarrer". Comme précédemment lorsque le temps de jeu est écoulé les sujets doivent répondre à deux ou trois questions selon le traitement.

## Configuration et lancement de Dictator
Avant de lancer la partie Dictateur il faut absolument former les groupes depuis le sous-menu de la partie TeamCommunication. Ceci du fait que dans cette partie de dictateur on ne veut pas que deux joueurs qui ont été dans un même groupe se retrouvent dans la même paire, c'est donc TeamCommunication qui gère les appariements pour Dictator.  

Une fois les paires formées il faut configurer Dictator (cette configuration peut-être faite avant, pas de soucis), c'est à dire définir le traitement, à savoir STRATEGY_METHOD. Ensuite la partie peut-être lancée, en cliquant sur "Démarrer". Une fois la partie terminée, il faut retourner dans le sous-menu TeamCommunication pour faire afficher la question d'après Dictator (le lancement de cette question se fait depuis TeamCommunication car c'est propre à cette expérience, alors que Dictator est une partie qui a été développée il y a quelques temps déjà).

## Lancement du questionnaire final
Une fois que les deux séquences de TeamCommunication et la partie Dictator sont terminée, lancer le questionnaire final (par encore traduit). Pour cela cliquer sur le sous-menu "Afficher le questionnaire final" du menu "Expérience". 

## Gains de l'expérience
Pour tirer au sort la partie ou la séquence à rémunérer, utiliser un des outils à disposition pour faire un tirage au sort (cf. menu outils).   

Si c'est une séquence de TeamCommunication, cliquer sur "Afficher les gains" et déterminer la séquence pour laquelle afficher les gains (la première séquence est la séquence 0, la seconde la séquence 1). Ceci ouvre alors une fenêtre avec les gains des sujets (par poste) pour cette séquence. Les gains peuvent alors être imprimés, ajoutés aux gains finaux ou affichés sur les postes clients. Normalement la bonne procédure est de les ajouter aux gains finaux puis de fermer la fenêtre. Ensuite dans le menu Expérience cliquer sur "Gains". Cela ouvre une fenêtre quasiment identique à la précédente. Cliquer alors sur "Afficher sur les postes clients" afin de faire afficher l'écran final, il informe le sujet de son gain et lui laisse un espace pour écrire des commentaires sur l'expérience.  

Si c'est le Dictateur qui est rémunéré il faut alors cliquer sur le sous-menu "Afficher les gains" du menu Dictator. La procédure est ensuite la même que celle décrite dans le paragraphe au-dessus.  

S'il y a plusieurs séquences ou parties à rémunérer il faut alors afficher les gains de ces séquences parties et ajouter les gains aux gains finaux, ils s'additionnent. Une fois effectué cliquer sur le sous-menu "Gains" du menu Expérience. Les gains cumulés des séquences/parties sont affichés. Les imprimer puis rémunérer les sujets.
