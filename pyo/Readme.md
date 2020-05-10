# Utilisation du serveur xmlrpc pour Pyo

Le serveur xmlrpc permet une communication avec un process pyo à travers le réseau
Le script s'appuie sur deux processus imbriqués :
 - le serveur xmlrpc qui traite les demandes du client
 - le process Pyo server qui les traite
 
Globalement, il ne s'agit que d'une enveloppe qui permet de dissocier un serveur Pyo sur le réseau d'un client qui l'utilise


## Serveur


### configuration
Le serveur doit être associé à un fichier de configuration au format.ini

Les directives de configuration sont spécifiées de la façon suivante :

```
[DEFAULT]
audio device =  pulse  
log = /tmp/logpyo.log

[PYO]
verbosity = 8
output = 0
duplex = 0

[xmlrpcServ]
port = 1233

```



### lancement
```
serverPyoRPC.py --action=start --config=/where/is/the/config.ini
```

### arrêt

```
serverPyoRPC.py --action=stop
```


## Client xmlrpc

### Exemple

clientPyoRPC.py

### Exemple interactif
```
>>> import xmlrpc.client
>>> s = xmlrpc.client.ServerProxy('http://127.0.0.1:1233')
>>> s.get_pyopid()
'20769'
>>> s.is_pyostarted()
True
>>> s.pyocmd('a=Sine(800)')
'NULL'
>>> s.pyocmd('a.out()')
'NULL'
>>> s.pyocmd('a.stop()')
'NULL'
```
