# TP Docker

## Exercice 1

### Question 1.b
![alt text](image.png)

### Question 1.c
![alt text](image-1.png)

## Exercice 2

### Question 2.a
Une image est le modèle sur lequel va se baser le conteneur pour tourner. C’est un framework qu’on utilise pour lancer des conteneurs similaires.

### Question 2.b
![alt text](image-2.png)

### Question 2.c
![alt text](image-3.png)

### Question 2.d
![alt text](image-4.png)

## Exercice 3

### Question 3.a — *app.py*
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

### Question 3.b — *Dockerfile*
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install fastapi uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Question 3.c
![alt text](image-5.png)
![alt text](image-6.png)

## Exercice 4

### Question 4.a
![alt text](image-7.png)
![alt text](image-8.png)

La partie `-p 8000:8000` permet de lier le port ouvert du conteneur au port local de notre machine pour accéder au service.

### Question 4.b
![alt text](image-9.png)
![alt text](image-10.png)

### Question 4.c
![alt text](image-11.png)

### Question 4.d
![alt text](image-12.png)
![alt text](image-13.png)

`docker ps -a` affiche tous les conteneurs (actifs ou non), tandis que `docker ps` ne montre que les conteneurs actifs.

## Exercice 5

### Question 5.a
![alt text](image-14.png)

### Question 5.b — *docker-compose.yml*
```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: demo
      POSTGRES_PASSWORD: demo
      POSTGRES_DB: demo
    ports:
      - "5432:5432"

  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - db
```

### Question 5.c
![alt text](image-15.png)

### Question 5.d
![alt text](image-16.png)

### Question 5.e
`docker compose down` arrête tous les conteneurs du compose et supprime le réseau, alors que `docker stop` ne stoppe qu’un conteneur spécifique.

## Exercice 6

### Question 6.a
`exec` permet d'exécuter une commande dans un conteneur actif.  
`db` est le service ciblé.  
`-U` indique l’utilisateur PostgreSQL.  
`-d` indique la base à utiliser.

### Question 6.b
![alt text](image-17.png)

### Question 6.c
Grâce au code contenu dans notre service, on peut s’y connecter.  
`hostname` indique le service Docker, le port celui exposé, et l’utilisateur, le mot de passe et le nom de la base restent `demo`.

### Question 6.d
Le `-v` supprime aussi les volumes, effaçant donc toutes les données associées.

## Exercice 7

### Question 7.a
![alt text](image-18.png)
![alt text](image-19.png)

On peut observer ici l’ensemble des logs générés par le service.

### Question 7.b
![alt text](image-20.png)

Le conteneur qui héberge l’API utilise Python.

### Question 7.c
![alt text](image-21.png)
![alt text](image-22.png)

Le redémarrage permet d’appliquer une modification de configuration sans toucher aux autres services.

### Question 7.d
![alt text](image-23.png)
![alt text](image-24.png)
![alt text](image-25.png)

L’application échoue ici car elle est mal déclarée.

### Question 7.e
Nettoyer régulièrement évite l’encombrement disque et maintient un environnement propre.

## Exercice 8

### Question 8.a
Un Jupyter Notebook n’est pas adapté au déploiement : pas de gestion de versions, pas de services associés (BDD…), faible reproductibilité entre machines. Docker règle ces problèmes.

### Question 8.b
Docker Compose permet d’orchestrer plusieurs services liés simplement, rapidement et de manière reproductible.
