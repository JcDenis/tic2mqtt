# TIC 2 MQTT
Read, parse and send TIC data from French electric meter to an MQTT broker.

Ce script utilise les librairies :

* [python-teleinfo](https://github.com/demikl/python-teleinfo)
* [paho-mqtt](https://github.com/eclipse/paho.mqtt.python)

## Prérequis

Il faut installer python et pip :

```
sudo apt install python-pip

```

On a besoin des librairies pip suivantes :

```
sudo pip install paho-mqtt pyserial teleinfo
```

L'utilisateur courant doit aussi avoir les droits sur la lecture serie :

```
sudo usermod -G dialout $USER
```

(Il faut se déconnecter et se reconnecter à la console pour que prendre effet.)

Enfin on a besoin de ce script !

```
cd ~
git clone https://github.com/JcDenis/tic2mqtt
```

## Usage

Une fois les prérequis fait, on peut tester directement dans la console:

```
cd ~/tic2mqtt
python tic2mqtt.py -v
```

Le script supporte les options suivantes :

* -c, --client, le nom du client qui se connectera au broker MQTT, enedis
* -b, --host, l'adresse du broker (ex: 192.168.0.10), localhost
* -p, --port, le port du broker, 1883
* -u, --user, le login de connexion au broker si nécessaire
* -w, --password, le mot de passe de connexion au broker si nécessaire
* -t, --topic, le topic principal de publication, teleinfo
* -i, --interface, le port usb ou est connecté le dongle teleinfo, /dev/ttyUSB0
* -v, --verbose, mode verbeux pratique pour les tests

Exemple :

```
cd ~/tic2mqtt
python tic2mqtt.py -c EDF -b 192.168.0.10 -u bob -w plop -v
```

## Boot

Pour démarrer ce script au boot, copier le fichier service et remplacer 
l'utilisateur courant dans les chemin d'accès:

```
cd ~/tic2mqtt
sudo cp tic2mqtt.service /etc/systemd/system/tic2mqtt.service
sudo sed -i "s/USER/$USER/" /etc/systemd/system/tic2mqtt.service
sudo nano /etc/systemd/system/tic2mqtt.service
```

On l'édite et on modifie la fin de la ligne `ExecStart` en ajoutant 
les options précédemment vues pour coller à nos besoins.
(Voir exemple au dessus.)

Enfin on test et on l'ajoute au systemd :

```
sudo systemctl daemon-reload
sudo systemctl start tic2mqtt.service
sudo systemctl status tic2mqtt.service
sudo systemctl enable tic2mqtt.service
```

## TODO

* Manage exceptions
* Better sanitize
* Use a config gile
* Add option to use json or topics

## PS

Je ne suis pas dev, n'hésitez pas à modifier, corriger tout ça.