# Guide de Migration - MKO Performance

## Modifications apportées

### Changement du modèle Voiture

**Fichier:** `products/models.py`

Le champ `image` unique a été remplacé par deux champs séparés :
- `image_exterieur` - photo de l'extérieur du véhicule
- `image_interieur` - photo de l'intérieur du véhicule

---

## Instructions pour les collègues (après git pull)

### Option 1: Nouvelle base de données (recommandé)

Si vous partez d'une nouvelle base de données :

```bash
# Supprimer les anciennes migrations de toutes les apps
rm -rf products/migrations/*.py
rm -rf users/migrations/*.py
rm -rf cart/migrations/*.py
rm -rf orders/migrations/*.py

# Supprimer la base de données existante
rm -f db.sqlite3  # (ou votre fichier MySQL selon config)

# Recréer les migrations
python manage.py makemigrations products users cart orders

# Appliquer les migrations
python manage.py migrate

# (Optionnel) Charger les données de test
python manage.py fake_data
```

### Option 2: Base de données existante avec données

Si vous avez des données dans la base et vous voulez les garder :

```bash
# 1. Faire un backup de la base de données avant tout
mysqldump -u username -p database_name > backup.sql

# 2. Supprimer les anciennes migrations
rm -rf products/migrations/*.py
rm -rf users/migrations/*.py
rm -rf cart/migrations/*.py
rm -rf orders/migrations/*.py

# 3. Recréer les migrations propres
python manage.py makemigrations products users cart orders

# 4. Migrer (Django va demander quoi faire avec les anciennes données)
python manage.py migrate

# 5. IMPORTANT: Ajouter manuellement les images dans l'admin
#    - Chaque voiture aura besoin de 2 images (ext + int)
#    - Les anciennes images sont perdues
```

---

## Note pour le frontend

Dans les templates, remplacez :
- `voiture.image` → `voiture.image_exterieur` ou `voiture.image_interieur`

Exemple dans `product_list.html` :
```html
<!-- Avant -->
<img src="{{ voiture.image.url }}" alt="{{ voiture.nom }}">

<!-- Après -->
<img src="{{ voiture.image_exterieur.url }}" alt="{{ voiture.nom }}">
```