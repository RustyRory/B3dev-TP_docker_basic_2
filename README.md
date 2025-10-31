# TP Docker basics 2

**Nom :** Damien Paszkiewicz

## Objectif général

Mettre en place un environnement Docker fonctionnel, créer sa première image, lancer et diagnostiquer des conteneurs, puis comprendre les notions fondamentales (volumes, réseaux, bonnes pratiques de base).

## Prérequis

- Poste de travail avec Docker Desktop, Docker Engine ou Colima / Rancher Desktop configuré
- Accès à un shell (bash/zsh) avec curl , git , docker , docker compose
- Notions de base en ligne de commande et en Python (script simple)

## Compétences visées

- Vérifier et comprendre la configuration d’un moteur Docker
- Construire une image à partir d’un Dockerfile minimal
- Lancer, inspecter et supprimer des conteneurs
- Monter des volumes et publier des ports
- Diagnostiquer les erreurs courantes (build, run, permission)

## Fil rouge du TP

Tu vas conteneuriser un mini-service Python (« quotegen ») qui renvoie une citation aléatoire via une API Flask. Chaque étape t’amènera à introduire un concept Docker différent. Le répertoire recommandé est ~/workspace/docker-basic 

# Étape 0 — Préparer l’arborescence

- Crée le dossier de travail et initialise le dépôt
- Ajoute le squelette applicatif :

```python
import random
from flask import Flask, jsonify
QUOTES = [
"Docker vous donne l'isolement sans la douleur des VM.",
"Build once, run anywhere (du moins en théorie).",
"Les couches de Docker sont des caches déguisés.",
]
app = Flask(name)
@app.get("/quote")
def quote():
return jsonify({"quote": random.choice(QUOTES)})
if name == "main":
app.run(host="0.0.0.0", port=5000)
```

```python
flask==3.0.3
gunicorn==22.0.0
```

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python [app.py](http://app.py/)
```

![image.png](/B3dev-TP_docker_basic_2/media/image(1).png)

# Étape 1 — Découvrir son moteur Docker

```yaml
~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker version          
Client: Docker Engine - Community
 Version:           28.5.1
 API version:       1.51
 Go version:        go1.24.8
 Git commit:        e180ab8
 Built:             Wed Oct  8 12:17:26 2025
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          28.5.1
  API version:      1.51 (minimum version 1.24)
  Go version:       go1.24.8
  Git commit:       f8215cc
  Built:            Wed Oct  8 12:17:26 2025
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v1.7.28
  GitCommit:        b98a3aace656320842a23f4a392a33f46af97866
 runc:
  Version:          1.3.0
  GitCommit:        v1.3.0-0-g4ca628d1
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

```yaml
~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker info
Client: Docker Engine - Community
 Version:    28.5.1
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3
    Path:     /usr/libexec/docker/cli-plugins/docker-compose

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 3
 Server Version: 28.5.1
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: b98a3aace656320842a23f4a392a33f46af97866
 runc version: v1.3.0-0-g4ca628d1
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.8.0-87-generic
 Operating System: Linux Mint 22.2
 OSType: linux
 Architecture: x86_64
 CPUs: 8
 Total Memory: 15.28GiB
 Name: rusty-ThinkPad-T490s
 ID: a2aeb713-09f6-42d5-ba91-5ae6388c18ec
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
```

| Catégorie | Détail |
| --- | --- |
| **Version du serveur Docker** | Docker Engine - Community 28.5.1 (API 1.51) |
| **Go version** | go1.24.8 |
| **Git commit** | f8215cc |
| **OS / Architecture** | Linux Mint 22.2 / x86_64 |
| **Storage Driver** | overlay2 (Backing FS : extfs, Supports d_type : true) |
| **Logging Driver** | json-file |
| **Cgroup Driver** | systemd (Cgroup version 2) |
| **Runtimes disponibles** | io.containerd.runc.v2, runc |
| **Runtime par défaut** | runc |
| **Init Binary** | docker-init |
| **Conteneurs** | 0 (Running: 0, Paused: 0, Stopped: 0) |
| **Images** | 3 |
| **Plugins réseau** | bridge, host, ipvlan, macvlan, null, overlay |
| **Swarm** | inactive |

### commandes de base

```bash
docker ps # conteneurs en cours
~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

```bash
docker ps -a # conteneurs arrêtés compris
~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

```bash
docker image ls # images disponibles
~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED             SIZE
welcome       1.0.0     d4dbafc1c149   About an hour ago   119MB
alpine        3.20      e89557652e74   3 weeks ago         7.8MB
hello-world   latest    1b44b5a3e06a   2 months ago        10.1kB
```

```bash
docker volume ls # volumes existants
~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker volume ls
DRIVER    VOLUME NAME
```

# Étape 2 — Écrire un Dockerfile minimal

1. Crée un fichier Dockerfile avec les instructions de base 
    
    ```docker
    # syntax=docker/dockerfile:1
    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY [app.py](http://app.py/) .
    EXPOSE 5000
    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
    ```
    
    | Instruction | Justification |
    | --- | --- |
    | `FROM python:3.12-slim` | Définit l’**image de base**, ici Python 3.12 avec une version slim (léger) pour construire l’image. |
    | `WORKDIR /app` | Définit le **répertoire de travail** du conteneur. Toutes les commandes suivantes s’exécuteront dans `/app`. |
    | `COPY requirements.txt .` | Copie le fichier des dépendances dans le conteneur pour pouvoir les installer. |
    | `RUN pip install --no-cache-dir -r requirements.txt` | Installe les **dépendances Python** listées dans `requirements.txt`. L’option `--no-cache-dir` évite d’alourdir l’image. |
    | `COPY app.py .` | Copie le script principal de l’application dans le conteneur. |
    | `EXPOSE 5000` | Indique que le conteneur **écoute sur le port 5000** (utile pour les applications web). |
    | `CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]` | Définit la **commande par défaut** à exécuter quand le conteneur démarre. Ici Gunicorn lance l’application Flask ou similaire. |
2. Construis l’image :
    
    ```yaml
    ~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker build -t quotegen:1.0.0 .           
    [+] Building 5.5s (12/12) FINISHED                                    docker:default
     => [internal] load build definition from Dockerfile                            0.0s
     => => transferring dockerfile: 258B                                            0.0s
     => resolve image config for docker-image://docker.io/docker/dockerfile:1       0.8s
     => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:b6afd42430b15f2  0.0s
     => [internal] load metadata for docker.io/library/python:3.12-slim             0.5s
     => [internal] load .dockerignore                                               0.0s
     => => transferring context: 2B                                                 0.0s
     => [1/5] FROM docker.io/library/python:3.12-slim@sha256:e97cf9a2e84d604941d99  0.0s
     => [internal] load build context                                               0.0s
     => => transferring context: 507B                                               0.0s
     => CACHED [2/5] WORKDIR /app                                                   0.0s
     => [3/5] COPY requirements.txt .                                               0.0s
     => [4/5] RUN pip install --no-cache-dir -r requirements.txt                    3.6s
     => [5/5] COPY app.py .                                                         0.1s 
     => exporting to image                                                          0.2s 
     => => exporting layers                                                         0.2s 
     => => writing image sha256:9ade4bfee9a621f06d391a997b40fd3fd01a60859ababc7560  0.0s 
     => => naming to docker.io/library/quotegen:1.0.0                               0.0s 
    ```
    
3. Valide la présence de l’image :
    
    ```yaml
    ~/Documents/B3dev/Docker/B3dev-TP_docker_basic_2$ sudo docker image ls quotegen
    REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
    quotegen     1.0.0     9ade4bfee9a6   54 seconds ago   133MB
    ```
    
    - **Taille de l’image** : 133 MB
    - **Impact des dépendances** :
        - Chaque package Python installé via `requirements.txt` **augmente la taille de l’image**.
        - L’utilisation de l’image `python:3.12-slim` limite déjà la taille de base par rapport à `python:3.12` complète.
        - L’option `-no-cache-dir` dans `pip install` **évite de stocker le cache pip**, ce qui réduit encore la taille finale.
    - Pour la gestion de l’image, il faut :
        - Choisir une **image Alpine**
        - Installer uniquement les **dépendances nécessaires**
        - Nettoyer les caches (`-no-cache-dir`)

# Étape 3 — Lancer et tester le conteneur

Démarre le conteneur en avant-plan :

```bash
~/...$ sudo docker run --rm -p 5000:5000 --name quotegen quotegen:1.0.0
[2025-10-31 11:56:42 +0000] [1] [INFO] Starting gunicorn 22.0.0
[2025-10-31 11:56:42 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2025-10-31 11:56:42 +0000] [1] [INFO] Using worker: sync
[2025-10-31 11:56:42 +0000] [7] [INFO] Booting worker with pid: 7

[2025-10-31 11:59:12 +0000] [1] [INFO] Handling signal: int
[2025-10-31 11:59:12 +0000] [7] [INFO] Worker exiting (pid: 7)
[2025-10-31 11:59:13 +0000] [1] [INFO] Shutting down: Master

```

```bash
~$ sudo curl http://localhost:5000/quote            
{"quote":"Les couches de Docker sont des caches d\u00e9guis\u00e9s."}
~$ sudo curl http://localhost:5000/quote
{"quote":"Build once, run anywhere (du moins en th\u00e9orie)."}
```

2. Relance-le en arrière-plan :

```bash
~/...$ sudo docker run -d -p 5000:5000 --name quotegen quotegen:1.0.0
0c96068840986e0b25b1819381ee1d7f2c39232234f6094470389d46a4227985
```

```bash
$ sudo docker logs quotegen --tail 5
[2025-10-31 12:02:58 +0000] [1] [INFO] Starting gunicorn 22.0.0
[2025-10-31 12:02:58 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2025-10-31 12:02:58 +0000] [1] [INFO] Using worker: sync
[2025-10-31 12:02:58 +0000] [7] [INFO] Booting worker with pid: 7
```

3. Inspecte et supprime :

```bash
$ sudo docker inspect quotegen --format '{{json .NetworkSettings.Ports}
}' | python -m json.tool            
{
    "5000/tcp": [
        {
            "HostIp": "0.0.0.0",
            "HostPort": "5000"
        },
        {
            "HostIp": "::",
            "HostPort": "5000"
        }
    ]
}
```

```bash
$ sudo docker stop quotegen            
quotegen
$ sudo docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
0c96068840986e0b25b1819381ee1d7f2c39232234f6094470389d46a4227985

Total reclaimed space: 164.1kB
```

- `stop` → utile pour arrêter temporairement un conteneur sans le supprimer et le relancer ensuite.
- `rm` → supprime un conteneur précis pour libérer le nom et l’espace.
- `prune` → pratique pour **nettoyer tous les conteneurs arrêtés** d’un coup, surtout après plusieurs tests.

# Étape 4 — Volumes et persistance

Objectif : extraire la liste des citations vers un volume monté pour pouvoir la modifier sans rebuild.

1. Déplace le contenu dans un dossier data :
    
    ```
    Docker vous donne l'isolement sans la douleur des VM.
    Build once, run anywhere (du moins en théorie).
    Les couches de Docker sont des caches déguisés.
    ```
    
2. Modifie `app.py` pour lire depuis `data/quotes.txt` :
    
    ```python
    import random
    from flask import Flask, jsonify
    from pathlib import Path
    
    def load_quotes():
        with Path("data/quotes.txt").open() as fh:
            return [line.strip() for line in fh if line.strip()]
    
    app = Flask(__name__)
    
    @app.get("/quote")
    def quote():
        quotes = load_quotes()
        return jsonify({"quote": random.choice(quotes)})
    
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)
    ```
    
3. Mets à jour le `Dockerfile` :
    
    ```docker
    # syntax=docker/dockerfile:1
    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY app.py .
    COPY data ./data
    EXPOSE 5000
    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
    ```
    
4. Reconstruis l’image ( `docker build -t quotegen:1.1.0 .` ) et lance-la avec un volume :
    
    ```bash
    ~/$ sudo docker run -d -p 5000:5000 \
    -v "$(pwd)/data/quotes.txt:/app/data/quotes.txt:ro" \
    --name quotegen quotegen:1.1.0
    f430b58075c56332df9c2630299d7c370fb152c410bf8d4f4b349b5312b3c198
    ```
    
5. Édite `data/quotes.txt` localement, ajoute une citation, puis teste l’API.
    
    ```docker
    Docker vous donne l'isolement sans la douleur des VM.
    Build once, run anywhere (du moins en théorie).
    Les couches de Docker sont des caches déguisés.
    Ceci est une nouvelle quote.
    ```
    
    ![image.png](/B3dev-TP_docker_basic_2/media/image.png)
    

| Aspect | COPY | -v (volume) |
| --- | --- | --- |
| Moment | Build (construction) | Run (exécution) |
| Modification | Rebuild nécessaire | Instantanée |
| Portabilité | Totale | Dépend de l’hôte |
| Usage | Fichiers fixes, code | Fichiers dynamiques, données |

# Étape 5 — Gestion des tags et nettoyage

Liste les images et supprime les anciennes :

```bash
$ sudo docker image ls quotegen
REPOSITORY   TAG       IMAGE ID       CREATED             SIZE
quotegen     1.1.0     f179fa2d4cb0   19 minutes ago      133MB
quotegen     1.0.0     9ade4bfee9a6   About an hour ago   133MB
$ sudo docker image rm quotegen:1.0.0
Untagged: quotegen:1.0.0
Deleted: sha256:9ade4bfee9a621f06d391a997b40fd3fd01a60859ababc7560271eb1d8c5bc3b
```

Crée des aliases de tag :

```bash
docker tag quotegen:1.1.0 quotegen:latest
docker tag quotegen:1.1.0 registry.local:5000/quotegen:1.1.0 # exemple

$ sudo docker image ls quotegen
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
quotegen     1.1.0     f179fa2d4cb0   20 minutes ago   133MB
quotegen     latest    f179fa2d4cb0   20 minutes ago   133MB
```

Les tags multiples permettent de versionner une même image pour différents usages : un tag précis (`1.1.0`) pour la stabilité/reproductibilité, `latest` pour toujours utiliser la version la plus récente, et `staging` pour tester des versions intermédiaires avant production

Inspecte les couches pour comprendre la taille :

```
$ sudo docker history quotegen:1.1.0
IMAGE          CREATED             CREATED BY                                      SIZE      COMMENT
f179fa2d4cb0   22 minutes ago      CMD ["gunicorn" "--bind" "0.0.0.0:5000" "app…   0B        buildkit.dockerfile.v0
<missing>      22 minutes ago      EXPOSE [5000/tcp]                               0B        buildkit.dockerfile.v0
<missing>      22 minutes ago      COPY data ./data # buildkit                     181B      buildkit.dockerfile.v0
<missing>      22 minutes ago      COPY app.py . # buildkit                        402B      buildkit.dockerfile.v0
<missing>      About an hour ago   RUN /bin/sh -c pip install --no-cache-dir -r…   13.8MB    buildkit.dockerfile.v0
<missing>      About an hour ago   COPY requirements.txt . # buildkit              29B       buildkit.dockerfile.v0
<missing>      3 hours ago         WORKDIR /app                                    0B        buildkit.dockerfile.v0
<missing>      3 weeks ago         CMD ["python3"]                                 0B        buildkit.dockerfile.v0
<missing>      3 weeks ago         RUN /bin/sh -c set -eux;  for src in idle3 p…   36B       buildkit.dockerfile.v0
<missing>      3 weeks ago         RUN /bin/sh -c set -eux;   savedAptMark="$(a…   36.8MB    buildkit.dockerfile.v0
<missing>      3 weeks ago         ENV PYTHON_SHA256=fb85a13414b028c49ba18bbd52…   0B        buildkit.dockerfile.v0
<missing>      3 weeks ago         ENV PYTHON_VERSION=3.12.12                      0B        buildkit.dockerfile.v0
<missing>      3 weeks ago         ENV GPG_KEY=7169605F62C751356D054A26A821E680…   0B        buildkit.dockerfile.v0
<missing>      3 weeks ago         RUN /bin/sh -c set -eux;  apt-get update;  a…   3.81MB    buildkit.dockerfile.v0
<missing>      3 weeks ago         ENV LANG=C.UTF-8                                0B        buildkit.dockerfile.v0
<missing>      3 weeks ago         ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…   0B        buildkit.dockerfile.v0
<missing>      3 weeks ago         # debian.sh --arch 'amd64' out/ 'trixie' '@1…   78.6MB    debuerreotype 0.16
```

Identifie les instructions qui pèsent le plus.

- `RUN /bin/sh -c set -eux; ...` pour installer des paquets système (~36,8 MB)
- `debuerreotype` (base Debian slim) (~78,6 MB)
- `RUN pip install --no-cache-dir -r requirements.txt` (~13,8 MB)

**Différence volumes nommés vs bind mounts** :

- **Volumes nommés** : gérés par Docker, persistent même si le conteneur est supprimé, idéal pour stocker des données durables.
- **Bind mounts** : lient un dossier de ton système hôte au conteneur, utile pour le développement et la modification en temps réel, mais moins isolés.

# Étape 6 — Mini-quiz de validation

- Quelle est la différence entre ENTRYPOINT et CMD ?
    
    > **ENTRYPOINT** définit le programme principal du conteneur tandis que **CMD** fournit des arguments par défaut ou peut être remplacé au lancement.
    > 
- Comment inspecter les variables d’environnement d’un conteneur en cours d’exécution
    
    > Utilise `docker inspect <conteneur> | jq '.[0].Config.Env'` ou `docker exec <conteneur> env`.
    > 
- Comment diagnostiquer un build qui échoue derrière un proxy d’entreprise ?
    
    > Vérifie la configuration des variables `HTTP_PROXY`, `HTTPS_PROXY`, et `NO_PROXY` dans le Dockerfile ou le build context.
    > 
- Quelle commande permet de voir l’espace disque occupé par Docker ?
    
    > `docker system df` permet de voir l’espace disque utilisé par images, conteneurs et volumes.
    > 
- Pourquoi --rm est-il utile en développement ?
    
    > `--rm` supprime automatiquement le conteneur après son arrêt, évitant l’accumulation de conteneurs temporaires en développement.
    > 

# Bilan du TP

- Rapport de quelques lignes expliquant :
    - Les commandes clés utilisées
        - `docker build -t <image>:<tag> .` → construction des images à partir d’un Dockerfile.
        - `docker run [options] <image>` → lancement de conteneurs (avant-plan, arrière-plan, avec volumes ou variables d’environnement).
        - `docker ps`, `docker logs`, `docker inspect` → observation et diagnostic des conteneurs.
        - `docker rm`, `docker stop`, `docker container prune` → nettoyage des conteneurs.
        - `docker image ls`, `docker image rm` → gestion et suppression des images.
        - `docker volume prune` → nettoyage des volumes inutilisés.
    - Les difficultés rencontrées et leurs résolutions
        - Conflits de ports (`address already in use`) → résolus en tuant le processus local occupant le port ou en supprimant les conteneurs existants avec le même nom.
        - Conflits de noms de conteneurs → résolus avec `docker rm <container>` avant de relancer.
        - Gestion des données dynamiques → solution : bind mounts pour éditer les fichiers de l’hôte sans reconstruire l’image.
    - Une capture d’écran de l’API en fonctionnement

![image.png](/B3dev-TP_docker_basic_2/media/image(2).png)