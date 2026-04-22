# 🚗 MKO Performance - Système de Gestion de Location de Voitures

**MKO Performance** est une solution web complète conçue pour digitaliser et simplifier le processus de location de véhicules. [cite_start]Ce projet s'appuie sur l'architecture **Django MVT** et une conception UML rigoureuse[cite: 1, 8, 115].

## 👥 Équipe de Développement
Ce projet est le fruit d'une collaboration entre :
* [cite_start]**Mounib AFAILAL** [cite: 6]
* [cite_start]**Kamal BALLAGE** [cite: 7]
* [cite_start]**Oualae Eddine EJJED** [cite: 5]

## 🌟 Fonctionnalités Principales
[cite_start]Le système couvre l'intégralité du flux métier, de la consultation à la confirmation de réservation[cite: 13, 60]:
* [cite_start]**🔐 Authentification :** Inscription, connexion et gestion sécurisée des profils clients[cite: 18, 43].
* [cite_start]**🚗 Catalogue Interactif :** Consultation des voitures avec filtres par catégorie, marque et prix[cite: 20, 21].
* [cite_start]**📅 Réservation en ligne :** Sélection des dates, vérification de disponibilité et calcul automatique du montant total[cite: 23, 24, 50].
* [cite_start]**💳 Paiement & Suivi :** Simulation de paiement sécurisé et suivi en temps réel du statut (En attente, Payée, etc.)[cite: 26, 37, 56].
* [cite_start]**⚙️ Interface Administrateur :** Gestion complète (CRUD) des véhicules, des utilisateurs et des réservations[cite: 28, 40, 59].

## 🛠️ Stack Technique
* [cite_start]**Framework :** Django (Python) [cite: 14]
* [cite_start]**Base de données :** MySQL [cite: 15]
* [cite_start]**Front-end :** HTML5, CSS3, JavaScript [cite: 15]
* [cite_start]**Conception :** UML (Diagrammes de classes, séquences et cas d'utilisation) [cite: 8, 61, 79, 97]

## 📊 Architecture de Données
[cite_start]Le projet repose sur 7 classes principales interconnectées[cite: 81, 115]:
1. [cite_start]**Utilisateur :** Gère les informations personnelles et les rôles[cite: 82, 83].
2. [cite_start]**Voiture :** Détails techniques, prix et stock[cite: 84, 85].
3. [cite_start]**Catégorie :** Organisation des véhicules[cite: 86, 87].
4. [cite_start]**Panier & ArticlePanier :** Gestion des sélections temporaires[cite: 88, 90].
5. [cite_start]**Commande & ArticleCommande :** Finalisation et historique des transactions[cite: 92, 94].

---
*Projet réalisé dans le cadre de la formation d'ingénierie à l'EMSI.*
