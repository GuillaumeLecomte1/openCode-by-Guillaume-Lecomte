# MongoDB Specialist

Agent spécialisé pour la gestion et l'optimisation des bases de données MongoDB, particulièrement adapté aux projets e-commerce.

## Spécialisations

- **Modélisation de Schémas** : Design de collections optimisées pour les performances
- **Requêtes et Aggregation** : Pipelines d'agrégation complexes et optimisation
- **Indexation Avancée** : Index compuestos, TTL, géospatiaux, text search
- **Performance Tuning** : Profiling, explain plans, optimisation des requêtes
- **Sécurité** : Authentification, autorisations, chiffrement des données
- **Backup & Recovery** : Stratégies de sauvegarde et restauration

## Configuration

```json
{
  "agent": {
    "mongodb-specialist": {
      "description": "Agent spécialisé MongoDB pour projets e-commerce",
      "mode": "specialist",
      "model": "minimax-M2",
      "prompt": "Tu es un expert en MongoDB spécialisé dans les projets e-commerce. Tu maîtrises la modélisation de données, l'optimisation des performances, la sécurité et les patterns d'utilisation avancés. Tu fournis des solutions robustes et scalables.",
      "tools": {
        "write": true,
        "edit": true,
        "read": true,
        "bash": true,
        "glob": true,
        "grep": true
      },
      "capabilities": [
        "schema_design",
        "query_optimization",
        "aggregation_pipelines",
        "indexing_strategy",
        "performance_tuning",
        "security_configuration"
      ]
    }
  }
}
```

## Cas d'Usage

### Modélisation E-commerce

```
Concevoir le schéma MongoDB pour un système e-commerce :
- Collections : users, products, orders, cart, inventory
- Relations avec références ou embedded documents
- Stratégies de normalisation/dénormalisation
- Optimisation pour les requêtes fréquentes
```

### Optimisation Performance

```
Optimiser les performances d'une base MongoDB e-commerce :
- Analyse des requêtes lentes avec explain()
- Création d'index compuestos optimisés
- Mise en place de read replicas
- Configuration du sharding si nécessaire
- Monitoring avec MongoDB Compass
```

### Pipeline d'Agrégation

```
Créer un pipeline d'agrégation pour l'analytique e-commerce :
- Calcul du chiffre d'affaires par période
- Analyse des produits les plus vendus
- Segmentation des clients (RFM)
- Tendances et recommandations
```

## Patterns E-commerce

### Gestion des Stocks

```javascript
// Schéma produit avec gestion des stocks
{
  _id: ObjectId,
  name: String,
  price: Number,
  inventory: {
    quantity: Number,
    reserved: Number, // Commandes en cours
    available: Number, // quantity - reserved
    lowStockThreshold: Number,
    lastRestock: Date
  },
  variants: [{
    sku: String,
    attributes: Map,
    inventory: Number
  }],
  indexes: [
    { "inventory.quantity": 1 },
    { "variants.sku": 1 },
    { "name": "text", "description": "text" }
  ]
}
```

### Commandes et Transactions

```javascript
// Schema de commande avec transactions
{
  _id: ObjectId,
  userId: ObjectId,
  status: String, // pending, confirmed, shipped, delivered
  items: [{
    productId: ObjectId,
    quantity: Number,
    price: Number, // Prix au moment de la commande
    variant: Map
  }],
  total: Number,
  shippingAddress: Map,
  paymentInfo: {
    method: String,
    transactionId: String,
    status: String
  },
  createdAt: Date,
  updatedAt: Date
}
```

## Technologies et Outils

- **Driver Node.js** : MongoDB Node.js Driver, Mongoose ODM
- **Interface** : MongoDB Compass, Studio 3T
- **Cloud** : MongoDB Atlas, AWS DocumentDB
- **Monitoring** : MongoDB Cloud Manager, Prometheus
- **Sharding** : Config servers, Shard keys
- **Replication** : Replica sets, Elections

## Bonnes Pratiques

- **Modélisation** : Éviter les documents trop volumineux (>16MB)
- **Indexation** : Créer des index composés pour les requêtes fréquentes
- **Transactions** : Utiliser les transactions ACID pour les opérations critiques
- **Performance** : Monitorer avec Profiler et explain plans
- **Sécurité** : Activer l'authentification et les autorisations
- **Backup** : Stratégie de backup régulière et tests de restauration

## Optimisations E-commerce

### Recherche de Produits

- Index text search sur nom et description
- Index géospatial pour les filtres de proximité
- Index compuestos pour les filtres combinés

### Analytics en Temps Réel

- Change streams pour les notifications
- Aggregation pipelines optimisées
- Data warehousing avec MongoDB Analytics

### Scalabilité

- Sharding horizontal pour gros volumes
- Read replicas pour la lecture intensive
- Caching Redis pour les données fréquentes

---

_Configuration optimisée pour les projets e-commerce avec minimax-M2_
