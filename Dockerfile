# Image de base officielle
FROM python:3.9-slim
ENV PYTHONPATH=/app/backend_running
ENV DJANGO_SETTINGS_MODULE=backend_running.settings

# Répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY . /app
COPY backend_running/firebase_auth/serviceAccountKey.json /app/backend_running/firebase_auth/serviceAccountKey.json



# Installer les dépendances
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
