# 🚀 Deployment Guide - RulingvoAIBot

Complete guide for deploying your bot to various platforms.

## 📋 Table of Contents

1. [Railway Deployment](#railway-deployment)
2. [Heroku Deployment](#heroku-deployment)
3. [DigitalOcean Deployment](#digitalocean-deployment)
4. [AWS Deployment](#aws-deployment)
5. [VPS Deployment](#vps-deployment)
6. [Docker Deployment](#docker-deployment)

---

## 🚂 Railway Deployment (Recommended)

**Pros:** Free tier, automatic deployments, easy setup  
**Best for:** Personal projects, small to medium scale

### Step-by-Step

1. **Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

2. **Create Railway Account**
- Visit [railway.app](https://railway.app)
- Sign up with GitHub

3. **Create New Project**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository

4. **Add PostgreSQL Database**
- Click "New" → "Database" → "PostgreSQL"
- Railway automatically creates `DATABASE_URL`

5. **Add Redis (Optional)**
- Click "New" → "Database" → "Redis"
- Railway automatically creates `REDIS_URL`

6. **Set Environment Variables**

Go to your bot service → Variables:

```
TELEGRAM_BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4
LOG_LEVEL=INFO
NOTIFICATION_TIME_HOUR=9
DAILY_GOAL_XP=50
USE_REDIS=True
```

7. **Deploy**
- Railway automatically detects `Procfile` or `Dockerfile`
- Click "Deploy"
- Watch logs for any errors

8. **Custom Domain (Optional)**
- Settings → Domains → Generate Domain

### Railway-Specific Files

Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:
```
worker: python bot.py
```

---

## 🟣 Heroku Deployment

**Pros:** Established platform, good documentation  
**Cons:** Paid dynos required for 24/7 uptime

### Step-by-Step

1. **Install Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from heroku.com/downloads
```

2. **Login**
```bash
heroku login
```

3. **Create App**
```bash
heroku create russian-learner-bot
```

4. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:mini
```

5. **Add Redis**
```bash
heroku addons:create heroku-redis:mini
```

6. **Set Environment Variables**
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
heroku config:set OPENAI_MODEL=gpt-4
heroku config:set USE_REDIS=True
```

7. **Deploy**
```bash
git push heroku main
```

8. **Scale Worker**
```bash
heroku ps:scale worker=1
```

9. **View Logs**
```bash
heroku logs --tail
```

### Heroku-Specific Files

Ensure `Procfile` exists:
```
worker: python bot.py
```

Create `runtime.txt`:
```
python-3.11.7
```

---

## 🌊 DigitalOcean Deployment

**Pros:** Full control, good performance  
**Best for:** Medium to large scale applications

### Using App Platform

1. **Create Account** at [digitalocean.com](https://digitalocean.com)

2. **Create App**
- Apps → Create App
- Connect GitHub repository

3. **Configure Services**

**Bot Service:**
- Type: Worker
- Build Command: `pip install -r requirements.txt`
- Run Command: `python bot.py`

**Database:**
- Add PostgreSQL managed database
- Note connection string

4. **Environment Variables**
```
TELEGRAM_BOT_TOKEN
OPENAI_API_KEY
DATABASE_URL
```

5. **Deploy**
- Click "Create Resources"

### Using Droplet (VPS)

See [VPS Deployment](#vps-deployment) section.

---

## ☁️ AWS Deployment

**Pros:** Scalable, enterprise-ready  
**Best for:** Large scale, production applications

### Using EC2

1. **Launch EC2 Instance**
- Choose Ubuntu 22.04 LTS
- t2.micro for testing, t2.small+ for production
- Configure security groups

2. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3.11 python3-pip postgresql redis git -y
```

4. **Clone Repository**
```bash
git clone https://github.com/yourusername/russian-learner-bot.git
cd russian-learner-bot
```

5. **Install Python Packages**
```bash
pip3 install -r requirements.txt
```

6. **Configure Database**
```bash
sudo -u postgres psql
CREATE DATABASE RulingvoAIBot;
CREATE USER bot_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE RulingvoAIBot TO bot_user;
\q
```

7. **Set Environment Variables**
```bash
nano .env
# Add your variables
```

8. **Run with Systemd**

Create `/etc/systemd/system/russian-bot.service`:
```ini
[Unit]
Description=Russian Learner Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/russian-learner-bot
Environment="PATH=/home/ubuntu/.local/bin:/usr/bin"
EnvironmentFile=/home/ubuntu/russian-learner-bot/.env
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable russian-bot
sudo systemctl start russian-bot
sudo systemctl status russian-bot
```

### Using RDS for Database

1. **Create RDS PostgreSQL Instance**
- Choose PostgreSQL 15
- db.t3.micro for testing
- Note endpoint

2. **Update DATABASE_URL**
```
DATABASE_URL=postgresql://user:pass@endpoint:5432/dbname
```

### Using ElastiCache for Redis

1. **Create ElastiCache Redis Cluster**
2. **Update REDIS_URL**

---

## 🖥️ VPS Deployment (Generic)

**Works for:** DigitalOcean, Linode, Vultr, Hetzner, etc.

### Initial Setup

1. **Create VPS**
- Ubuntu 22.04 LTS
- At least 1GB RAM
- 25GB storage

2. **Connect via SSH**
```bash
ssh root@your-vps-ip
```

3. **Create User**
```bash
adduser botuser
usermod -aG sudo botuser
su - botuser
```

4. **Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

5. **Install Dependencies**
```bash
sudo apt install python3.11 python3-pip python3-venv \
                 postgresql postgresql-contrib \
                 redis-server git nginx \
                 supervisor ffmpeg -y
```

6. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE RulingvoAIBot;
CREATE USER bot_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE RulingvoAIBot TO bot_user;
\q
```

7. **Configure Redis**
```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

8. **Clone and Setup Bot**
```bash
cd /home/botuser
git clone https://github.com/yourusername/russian-learner-bot.git
cd russian-learner-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

9. **Configure Environment**
```bash
cp .env.example .env
nano .env
# Fill in your credentials
```

10. **Setup Supervisor**

Create `/etc/supervisor/conf.d/russian-bot.conf`:
```ini
[program:russian-bot]
directory=/home/botuser/russian-learner-bot
command=/home/botuser/russian-learner-bot/venv/bin/python bot.py
user=botuser
autostart=true
autorestart=true
stderr_logfile=/var/log/russian-bot/error.log
stdout_logfile=/var/log/russian-bot/output.log
environment=PATH="/home/botuser/russian-learner-bot/venv/bin"

[program:russian-bot-scheduler]
directory=/home/botuser/russian-learner-bot
command=/home/botuser/russian-learner-bot/venv/bin/python scheduler.py
user=botuser
autostart=true
autorestart=true
stderr_logfile=/var/log/russian-bot/scheduler-error.log
stdout_logfile=/var/log/russian-bot/scheduler-output.log
```

Start supervisor:
```bash
sudo mkdir -p /var/log/russian-bot
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start russian-bot:*
sudo supervisorctl status
```

### Monitoring

**View Logs:**
```bash
sudo tail -f /var/log/russian-bot/output.log
sudo tail -f /var/log/russian-bot/error.log
```

**Restart Bot:**
```bash
sudo supervisorctl restart russian-bot
```

**Check Status:**
```bash
sudo supervisorctl status russian-bot
```

---

## 🐳 Docker Deployment

**Pros:** Consistent environment, easy updates  
**Best for:** Any platform supporting Docker

### Local Docker

1. **Build Image**
```bash
docker build -t russian-learner-bot .
```

2. **Run with Docker Compose**
```bash
docker-compose up -d
```

3. **View Logs**
```bash
docker-compose logs -f bot
```

4. **Stop**
```bash
docker-compose down
```

### Docker Swarm

1. **Initialize Swarm**
```bash
docker swarm init
```

2. **Deploy Stack**
```bash
docker stack deploy -c docker-compose.yml bot
```

3. **Scale Services**
```bash
docker service scale bot_bot=3
```

### Kubernetes

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: russian-learner-bot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: russian-bot
  template:
    metadata:
      labels:
        app: russian-bot
    spec:
      containers:
      - name: bot
        image: your-registry/russian-learner-bot:latest
        envFrom:
        - secretRef:
            name: bot-secrets
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit `.env` file
- Use secrets management (AWS Secrets Manager, etc.)
- Rotate API keys regularly

### 2. Database Security
- Use strong passwords
- Enable SSL connections
- Restrict access by IP
- Regular backups

### 3. Bot Security
- Rate limiting enabled
- Input validation
- SQL injection prevention
- XSS protection

### 4. Server Security
```bash
# Firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### 5. SSL/TLS
```bash
# Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com
```

---

## 📊 Monitoring & Maintenance

### Monitoring Tools

1. **Sentry** - Error tracking
```bash
pip install sentry-sdk
```

Add to bot:
```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

2. **Prometheus** - Metrics
3. **Grafana** - Dashboards
4. **Uptime Robot** - Availability monitoring

### Backup Strategy

**Database Backup:**
```bash
# Automated daily backup
0 2 * * * pg_dump RulingvoAIBot > /backup/db_$(date +\%Y\%m\%d).sql
```

**Files Backup:**
```bash
# Backup user data
0 3 * * * tar -czf /backup/files_$(date +\%Y\%m\%d).tar.gz /app/audio /app/temp
```

### Update Procedure

```bash
# 1. Pull latest code
git pull origin main

# 2. Backup database
pg_dump RulingvoAIBot > backup.sql

# 3. Install new dependencies
pip install -r requirements.txt

# 4. Run migrations (if any)
alembic upgrade head

# 5. Restart bot
sudo supervisorctl restart russian-bot
```

---

## 🆘 Troubleshooting

### Bot Not Starting

```bash
# Check logs
sudo supervisorctl tail -f russian-bot stderr

# Check process
ps aux | grep python

# Check port conflicts
sudo netstat -tulpn | grep :8080
```

### Database Connection Issues

```bash
# Test connection
psql -h localhost -U bot_user -d RulingvoAIBot

# Check PostgreSQL status
sudo systemctl status postgresql
```

### High Memory Usage

```bash
# Monitor resources
htop

# Restart services
sudo supervisorctl restart russian-bot

# Clear cache
redis-cli FLUSHALL
```

---

## 📞 Support

If you encounter issues:
1. Check logs first
2. Search GitHub Issues
3. Create new issue with details
4. Join Telegram support group

---

**Happy Deploying! 🚀**

# © 2025 Mr.DosMa | Rulingvo Project
# All rights reserved / Все права защищены / Barcha huquqlar himoyalangan.