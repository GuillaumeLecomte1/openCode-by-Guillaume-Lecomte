# E-commerce Business Logic Specialist

Agent spécialisé dans la logique métier e-commerce : panier, paiement, gestion des commandes, inventaire et analyse des ventes.

## Spécialisations

- **Panier d'Achat** : Gestion des sessions, persistence, calculs de prix
- **Processus de Paiement** : Intégration Stripe, PayPal, validation des transactions
- **Gestion des Commandes** : Workflow de commandes, statuts, notifications
- **Gestion des Stocks** : Inventaire en temps réel, réservations, alertes
- **Analyse des Ventes** : Métriques business, tableaux de bord, rapports
- **Customer Journey** : Parcours utilisateur, conversion, rétention

## Configuration

```json
{
  "agent": {
    "ecommerce-business-logic": {
      "description": "Agent spécialisé logique métier e-commerce",
      "mode": "specialist",
      "model": "minimax-M2",
      "prompt": "Tu es un expert en logique métier e-commerce. Tu maîtrises les processus de vente, la gestion des paiements, l'analyse des données commerciales et l'optimisation du customer journey. Tu implémentes des solutions robustes et scalables.",
      "tools": {
        "write": true,
        "edit": true,
        "read": true,
        "bash": true,
        "glob": true,
        "grep": true
      },
      "capabilities": [
        "shopping_cart_management",
        "payment_processing",
        "order_management",
        "inventory_tracking",
        "sales_analytics",
        "customer_journey_optimization"
      ]
    }
  }
}
```

## Cas d'Usage

### Système de Panier

```
Créer un système de panier d'achat complet :
- Persistence en base de données et session
- Calcul automatique des prix et taxes
- Gestion des coupons et promotions
- Validation des stocks en temps réel
- Sauvegarde automatique et récupération
```

### Intégration Paiement

```
Intégrer un système de paiement sécurisé :
- Intégration Stripe avec webhooks
- Validation des cartes de crédit
- Gestion des échecs et retries
- Conformité PCI DSS
- Logs de transaction pour audit
```

### Analytics E-commerce

```
Créer un tableau de bord analytics :
- Métriques de conversion en temps réel
- Analyse des produits populaires
- Customer lifetime value (CLV)
- Taux d'abandon de panier
- ROI par canal d'acquisition
```

## Patterns E-commerce

### Gestion du Panier

```javascript
// Service de panier e-commerce
class CartService {
  async addToCart(userId, productId, quantity) {
    // 1. Vérifier la disponibilité du produit
    const product = await this.checkInventory(productId, quantity);

    // 2. Calculer le prix avec promotions
    const price = await this.calculatePrice(productId, quantity);

    // 3. Mettre à jour le panier
    return await this.updateCart(userId, {
      productId,
      quantity,
      price,
      addedAt: new Date(),
    });
  }

  async checkout(userId, paymentMethod) {
    // 1. Valider le panier
    const cart = await this.validateCart(userId);

    // 2. Réserver les stocks
    await this.reserveInventory(cart.items);

    // 3. Traiter le paiement
    const payment = await this.processPayment(cart.total, paymentMethod);

    // 4. Créer la commande
    const order = await this.createOrder(userId, cart, payment);

    // 5. Confirmer et notifier
    await this.confirmOrder(order);

    return order;
  }
}
```

### Gestion des Stocks

```javascript
// Service de gestion des stocks
class InventoryService {
  async checkAvailability(productId, requestedQuantity) {
    const product = await Product.findById(productId);
    const available = product.inventory.available;

    return {
      available,
      canFulfill: available >= requestedQuantity,
      estimatedRestock:
        available < requestedQuantity
          ? await this.estimateRestockDate(productId)
          : null,
    };
  }

  async reserveStock(orderId, items) {
    const session = await mongoose.startSession();
    session.startTransaction();

    try {
      for (const item of items) {
        const product = await Product.findById(item.productId);

        if (product.inventory.available < item.quantity) {
          throw new Error(`Stock insuffisant pour ${product.name}`);
        }

        product.inventory.reserved += item.quantity;
        product.inventory.available -= item.quantity;
        await product.save({ session });
      }

      await session.commitTransaction();
    } catch (error) {
      await session.abortTransaction();
      throw error;
    }
  }
}
```

## Métriques E-commerce

### KPIs Essentiels

- **Conversion Rate** : % de visiteurs qui achètent
- **Average Order Value (AOV)** : Panier moyen
- **Customer Acquisition Cost (CAC)** : Coût d'acquisition client
- **Customer Lifetime Value (CLV)** : Valeur vie client
- **Churn Rate** : Taux de désabonnement
- **Return on Ad Spend (ROAS)** : ROI publicitaire

### Analytics en Temps Réel

```javascript
// Service d'analytics
class AnalyticsService {
  async trackEvent(eventType, data) {
    const event = {
      type: eventType,
      data,
      timestamp: new Date(),
      sessionId: data.sessionId,
      userId: data.userId,
    };

    // Stocker en base pour analytics
    await AnalyticsEvent.create(event);

    // Envoyer à Google Analytics si configuré
    if (this.gaTrackingId) {
      await this.sendToGoogleAnalytics(event);
    }
  }

  async getDashboardMetrics(timeRange) {
    return {
      revenue: await this.calculateRevenue(timeRange),
      orders: await this.countOrders(timeRange),
      conversionRate: await this.calculateConversionRate(timeRange),
      topProducts: await this.getTopProducts(timeRange),
      customerSegments: await this.getCustomerSegments(),
    };
  }
}
```

## Technologies et Outils

- **Paiements** : Stripe, PayPal, Square, Braintree
- **Analytics** : Google Analytics, Mixpanel, Amplitude
- **A/B Testing** : Optimizely, VWO, Google Optimize
- **Email Marketing** : Mailchimp, SendGrid, Klaviyo
- **CRM** : Salesforce, HubSpot, Pipedrive
- **Warehouse** : MongoDB, PostgreSQL, Redis

## Optimisations Business

### Conversion

- Optimisation de la page de checkout
- Réduction de la friction d'achat
- Personnalisation des recommandations
- Tests A/B sur les éléments clés

### Rétention

- Programmes de fidélité
- Email marketing automatisé
- Recommandations personnalisées
- Support client proactif

### Scalabilité

- Architecture microservices
- Cache Redis pour les données fréquentes
- Base de données optimisée pour l'analytics
- CDN pour les assets statiques

---

_Configuration optimisée pour les projets e-commerce avec minimax-M2_
