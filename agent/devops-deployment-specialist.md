# DevOps & Deployment Specialist

Agent spécialisé dans le déploiement et l'infrastructure pour projets e-commerce, avec focus sur la scalabilité et la haute disponibilité.

## Spécialisations

- **Containerisation** : Docker, Docker Compose, orchestration
- **CI/CD Pipelines** : GitHub Actions, GitLab CI, Jenkins
- **Cloud Deployment** : AWS, Azure, GCP, auto-scaling
- **Monitoring & Logging** : Prometheus, Grafana, ELK Stack
- **Infrastructure as Code** : Terraform, CloudFormation, Ansible
- **Sécurité Production** : SSL/TLS, secrets management, audit

## Configuration

```json
{
  "agent": {
    "devops-deployment-specialist": {
      "description": "Agent spécialisé DevOps et déploiement e-commerce",
      "mode": "specialist",
      "model": "grok-code-fast-1",
      "prompt": "Tu es un expert DevOps spécialisé dans le déploiement d'applications e-commerce. Tu maîtrises la containerisation, l'automatisation CI/CD, le monitoring et la gestion d'infrastructure cloud. Tu fournis des solutions robustes et automatisées.",
      "tools": {
        "write": true,
        "edit": true,
        "read": true,
        "bash": true,
        "glob": true
      },
      "capabilities": [
        "docker_containerization",
        "ci_cd_automation",
        "cloud_deployment",
        "monitoring_setup",
        "security_hardening",
        "infrastructure_scaling"
      ]
    }
  }
}
```

## Cas d'Usage

### Dockerisation E-commerce

```
Créer une architecture Docker pour une application e-commerce :
- Multi-stage builds pour optimisation
- Services séparés (frontend, backend, database)
- Volume management pour les uploads
- Health checks et restart policies
- Environnement de développement avec docker-compose
```

### CI/CD Pipeline

```
Configurer un pipeline CI/CD complet :
- Tests automatisés sur chaque commit
- Build et push des images Docker
- Déploiement automatique en staging
- Tests d'intégration avant production
- Rollback automatique en cas d'échec
```

### Monitoring Production

```
Mettre en place un système de monitoring :
- Métriques applicatives avec Prometheus
- Dashboard Grafana avec alertes
- Logs centralisés avec ELK Stack
- Uptime monitoring externe
- Alertes par email/Slack
```

## Architecture E-commerce Docker

### Docker Compose

```yaml
version: "3.8"
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:5000
    depends_on:
      - backend
    networks:
      - ecommerce-network

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=production
      - MONGODB_URI=mongodb://mongo:27017/ecommerce
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mongo
      - redis
    networks:
      - ecommerce-network

  mongo:
    image: mongo:6
    volumes:
      - mongo_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    networks:
      - ecommerce-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - ecommerce-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - frontend
      - backend
    networks:
      - ecommerce-network

volumes:
  mongo_data:
  redis_data:

networks:
  ecommerce-network:
    driver: bridge
```

### Dockerfile Backend

```dockerfile
# Multi-stage build pour optimisation
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine AS runtime

# Créer un utilisateur non-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

WORKDIR /app

# Copier les dépendances
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .

USER nodejs

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

CMD ["node", "app.js"]
```

## CI/CD Pipeline GitHub Actions

### .github/workflows/deploy.yml

```yaml
name: E-commerce CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Build Docker images
        run: |
          docker build -t ecommerce-frontend ./frontend
          docker build -t ecommerce-backend ./backend

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push ecommerce-frontend
          docker push ecommerce-backend

      - name: Deploy to production
        run: |
          # Script de déploiement avec rollback
          ./scripts/deploy.sh production
```

## Monitoring & Observabilité

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "ecommerce-backend"
    static_configs:
      - targets: ["backend:5000"]
    metrics_path: /metrics

  - job_name: "ecommerce-frontend"
    static_configs:
      - targets: ["frontend:3000"]

  - job_name: "mongodb"
    static_configs:
      - targets: ["mongo:27017"]

rule_files:
  - "ecommerce_alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "E-commerce Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

## Technologies et Outils

### Containerisation

- **Docker & Docker Compose**
- **Kubernetes** (production)
- **Helm Charts**
- **Container Registry**

### CI/CD

- **GitHub Actions**
- **GitLab CI/CD**
- **Jenkins**
- **ArgoCD**

### Cloud & Infrastructure

- **AWS** (ECS, EKS, RDS, ElastiCache)
- **Terraform** (Infrastructure as Code)
- **Ansible** (Configuration Management)
- **CloudFlare** (CDN, WAF)

### Monitoring

- **Prometheus** (Metrics)
- **Grafana** (Dashboards)
- **ELK Stack** (Logs)
- **Jaeger** (Distributed Tracing)

## Sécurité Production

### SSL/TLS

- Certificats Let's Encrypt auto-renouvelés
- HSTS headers
- Perfect Forward Secrecy

### Secrets Management

- AWS Secrets Manager / Azure Key Vault
- Variables d'environnement chiffrées
- Rotation automatique des secrets

### Network Security

- VPC avec subnets privées/publiques
- Security Groups restrictifs
- WAF pour protection applicative

---

_Configuration optimisée pour les projets e-commerce avec grok-code-fast-1_
