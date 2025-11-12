# SPLANTS Marketing Engine - Deployment Guide

## Deployment Options

### Option 1: Local Machine (Development)

Perfect for testing and personal use.

**Requirements:**
- Docker Desktop
- 2GB RAM minimum
- 10GB disk space

**Steps:**
```bash
# Clone repository
git clone https://github.com/your-repo/splants-marketing.git
cd splants-marketing

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Access at http://localhost:8080
```

### Option 2: VPS Deployment (Recommended)

Deploy on a Virtual Private Server for production use.

**Recommended Providers:**
- DigitalOcean Droplet ($6-12/month)
- Linode ($5-10/month)
- Vultr ($6-12/month)
- Hetzner ($5-10/month)

**VPS Requirements:**
- Ubuntu 22.04 LTS
- 2GB RAM minimum
- 20GB SSD
- 1 vCPU

**Deployment Steps:**

1. **Setup VPS:**
```bash
# SSH into your VPS
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y
```

2. **Deploy Application:**
```bash
# Clone repository
git clone https://github.com/your-repo/splants-marketing.git
cd splants-marketing

# Setup environment
cp .env.example .env
nano .env  # Add your API keys

# Start services
docker-compose up -d
```

3. **Setup Nginx (Optional):**
```bash
# Install Nginx
apt install nginx -y

# Create configuration
nano /etc/nginx/sites-available/splants

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
ln -s /etc/nginx/sites-available/splants /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

4. **Setup SSL (Optional):**
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d your-domain.com
```

### Option 3: Cloud Platform Deployment

#### AWS EC2

1. Launch EC2 instance (t3.small recommended)
2. Security group: Open ports 80, 443, 8080
3. Follow VPS deployment steps

#### Google Cloud Platform

1. Create Compute Engine instance
2. Machine type: e2-small
3. Follow VPS deployment steps

#### Azure

1. Create Virtual Machine
2. Size: B1s or B2s
3. Follow VPS deployment steps

### Option 4: Docker Swarm (Scaling)

For high availability and scaling:

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml splants

# Scale services
docker service scale splants_app=3
```

### Option 5: Kubernetes (Enterprise)

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: splants-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: splants
  template:
    metadata:
      labels:
        app: splants
    spec:
      containers:
      - name: app
        image: splants-marketing:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: splants-secrets
              key: database-url
```

## Production Checklist

### Security

- [ ] Change default API_KEY in .env
- [ ] Use strong database password
- [ ] Setup firewall rules
- [ ] Enable SSL/TLS
- [ ] Regular security updates
- [ ] Limit API access by IP (optional)

### Performance

- [ ] Enable Redis caching ($10/month)
- [ ] Setup CDN for static assets
- [ ] Configure rate limiting
- [ ] Monitor resource usage
- [ ] Setup database indexing

### Monitoring

- [ ] Setup uptime monitoring (UptimeRobot)
- [ ] Configure error tracking (Sentry)
- [ ] Enable application logs
- [ ] Setup backup automation
- [ ] Monitor API costs

### Backups

#### Automated Daily Backups

```bash
# Create backup script
nano /home/backup.sh

#!/bin/bash
docker-compose exec -T db pg_dump -U splants splants > /backups/backup-$(date +%Y%m%d).sql
find /backups -name "*.sql" -mtime +7 -delete

# Add to crontab
crontab -e
0 2 * * * /home/backup.sh
```

#### Backup to S3

```bash
# Install AWS CLI
apt install awscli -y

# Configure AWS
aws configure

# Backup script with S3
#!/bin/bash
BACKUP_FILE="backup-$(date +%Y%m%d).sql"
docker-compose exec -T db pg_dump -U splants splants > /tmp/$BACKUP_FILE
aws s3 cp /tmp/$BACKUP_FILE s3://your-bucket/backups/
rm /tmp/$BACKUP_FILE
```

## Environment Variables for Production

```env
# Production .env example
OPENAI_API_KEY=sk-prod-xxx
API_KEY=strong-random-password-here
DATABASE_URL=postgresql://splants:strong-db-password@db:5432/splants

# Production settings
MONTHLY_AI_BUDGET=100
DAILY_API_LIMIT=500
MAX_CONTENT_LENGTH=5000

# Redis (recommended for production)
REDIS_URL=redis://redis:6379

# Monitoring
SENTRY_DSN=https://xxx@sentry.io/xxx
```

## Scaling Guidelines

### When to Scale

- **Vertical Scaling** (bigger server):
  - CPU usage > 80% consistently
  - Memory usage > 90%
  - Response times > 2 seconds

- **Horizontal Scaling** (more servers):
  - > 1000 requests/day
  - Need high availability
  - Geographic distribution needed

### Resource Requirements by Usage

| Daily Requests | Server Size | RAM | Storage | Monthly Cost |
|----------------|-------------|-----|---------|--------------|
| < 100 | Small | 2GB | 20GB | $10-15 |
| 100-500 | Medium | 4GB | 40GB | $20-30 |
| 500-2000 | Large | 8GB | 80GB | $40-60 |
| 2000+ | Multiple | 8GB+ | 100GB+ | $80+ |

## Troubleshooting Production Issues

### High Memory Usage

```bash
# Check memory
docker stats

# Restart services
docker-compose restart

# Clear cache if using Redis
docker-compose exec redis redis-cli FLUSHALL
```

### Database Connection Issues

```bash
# Check database
docker-compose exec db pg_isready

# Restart database
docker-compose restart db

# Check connections
docker-compose exec db psql -U splants -c "SELECT count(*) FROM pg_stat_activity;"
```

### API Errors

```bash
# Check logs
docker-compose logs -f app

# Check disk space
df -h

# Check API keys
docker-compose exec app env | grep API_KEY
```

## Migration Guide

### Moving to New Server

1. **Backup old server:**
```bash
docker-compose exec db pg_dump -U splants splants > backup.sql
```

2. **Transfer files:**
```bash
scp backup.sql root@new-server:/tmp/
scp .env root@new-server:/path/to/app/
```

3. **Restore on new server:**
```bash
docker-compose up -d db
docker-compose exec -T db psql -U splants splants < /tmp/backup.sql
docker-compose up -d
```

## Support

For deployment help:
- Documentation: `/docs`
- API Reference: `http://your-domain/docs`
- Logs: `docker-compose logs -f app`