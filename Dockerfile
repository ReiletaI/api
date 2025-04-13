# Utiliser une image Python officielle légère
FROM python:3.12-slim

# Définir le fuseau horaire (optionnel mais utile pour les logs)
ENV TZ=America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsox-fmt-mp3 \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt ./

# Installer les dépendances
# --no-cache-dir réduit la taille de l'image
# --trusted-host pypi.python.org peut être nécessaire dans certains environnements réseau
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Créer le répertoire qui sera monté comme volume (même si Docker Compose le créera)
# Assurez-vous que votre application écrit la BDD et les audios ici.
# Par exemple, le chemin de la BDD pourrait être /app/data/database.db
RUN mkdir -p /app/data

# Exposer le port sur lequel FastAPI écoute
EXPOSE 8000

# Commande pour lancer l'application FastAPI avec Uvicorn
# Remplacez 'app.main:app' par le chemin correct vers votre instance FastAPI
# --host 0.0.0.0 est crucial pour que l'application soit accessible depuis l'extérieur du conteneur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]