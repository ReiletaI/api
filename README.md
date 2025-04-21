# 📦 API Reiletai

Service backend implémenté avec **FastAPI**, exposant vos endpoints sous `/api/v1/…`.

## 📋 Prérequis

- Docker ≥ 20.10
- Docker Compose ≥ 1.29

## 📂 Structure du projet

```
/api
├── Dockerfile
├── main.py         # Point d’entrée FastAPI
├── requirements.txt
└── .env.example    # Variables d’environnement
```

## ⚙️ Configuration

1. Copiez `.env.example` en `.env`:
   ```env
   GROQ_API_KEY=<votre_clef>
   HF_TOKEN=<votre_token>
   ```
2. Adaptez les valeurs selon votre environnement.