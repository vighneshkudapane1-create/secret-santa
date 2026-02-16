# 🚀 Deployment Guide - Secret Santa Application

This guide will help you deploy your Secret Santa application to production.

## 📋 Pre-Deployment Checklist

- [ ] All code is committed to Git
- [ ] Environment variables are configured
- [ ] Database is set up and accessible
- [ ] Email SMTP credentials are ready
- [ ] Secret key is generated

## 🌐 Option 1: Deploy to Render (Recommended)

Your project is already configured for Render deployment with `render.yaml`.

### Steps:

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Connect Your Repository**
   - Push your code to GitHub/GitLab/Bitbucket
   - In Render dashboard, click "New +" → "Web Service"
   - Connect your repository

3. **Configure Environment Variables**
   In Render dashboard, go to your service → Environment tab, add:
   ```
   SECRET_KEY=your-secret-key-here-generate-a-random-string
   FLASK_ENV=production
   DATABASE_URL=postgresql://user:password@host:port/dbname
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

4. **Set Up PostgreSQL Database**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Choose a name and plan (Free tier available)
   - Copy the Internal Database URL
   - Add it as `DATABASE_URL` environment variable

5. **Deploy**
   - Render will automatically detect `render.yaml` and deploy
   - Wait for the build to complete
   - Your app will be live at `https://your-app-name.onrender.com`

### Generate Secret Key:
```python
import secrets
print(secrets.token_hex(32))
```

## 🐳 Option 2: Deploy with Docker

### Build and Run Locally:
```bash
docker build -t secret-santa .
docker run -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=your-database-url \
  -e MAIL_USERNAME=your-email \
  -e MAIL_PASSWORD=your-password \
  secret-santa
```

### Deploy to Docker Hosting:
- **DigitalOcean App Platform**: Connect GitHub and use Dockerfile
- **AWS ECS/Fargate**: Push to ECR and deploy
- **Google Cloud Run**: `gcloud run deploy`
- **Azure Container Instances**: Use Azure CLI

## ☁️ Option 3: Deploy to Other Platforms

### Heroku:
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn -b 0.0.0.0:$PORT run:app
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   ```

### Railway:
1. Connect GitHub repository
2. Railway auto-detects Python
3. Add environment variables in dashboard
4. Add PostgreSQL service
5. Deploy automatically

### Fly.io:
```bash
flyctl launch
flyctl deploy
```

## 🔧 Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `secrets.token_hex(32)` |
| `FLASK_ENV` | Environment mode | `production` |
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@host/db` |
| `MAIL_SERVER` | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USE_TLS` | Use TLS | `true` |
| `MAIL_USERNAME` | Email address | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Email password/app password | `your-app-password` |

## 📝 Post-Deployment Steps

1. **Initialize Database**
   - Run migrations if using Flask-Migrate
   - Or run your `create_tables.py` script
   - Create admin user using `create_admin_user.py`

2. **Test the Application**
   - Visit your deployed URL
   - Test registration/login
   - Create a test event
   - Verify email notifications

3. **Set Up Custom Domain** (Optional)
   - In Render: Settings → Custom Domains
   - Add your domain and configure DNS

4. **Monitor Logs**
   - Check Render logs for errors
   - Monitor database connections
   - Check email delivery

## 🔒 Security Checklist

- [ ] `SECRET_KEY` is set and secure
- [ ] `SESSION_COOKIE_SECURE=True` in production
- [ ] Database credentials are secure
- [ ] Email credentials use app passwords (not regular passwords)
- [ ] HTTPS is enabled
- [ ] No sensitive data in code

## 🐛 Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Verify `DATABASE_URL` is correct
   - Check database is accessible from hosting platform
   - Ensure database is running

2. **Email Not Sending**
   - Verify SMTP credentials
   - For Gmail, use App Password (not regular password)
   - Check firewall/security settings

3. **Build Fails**
   - Check `requirements.txt` is up to date
   - Verify Python version in `runtime.txt`
   - Check Dockerfile syntax

4. **App Crashes on Startup**
   - Check environment variables are set
   - Review application logs
   - Verify database tables exist

## 📞 Support

For issues specific to:
- **Render**: [Render Docs](https://render.com/docs)
- **Docker**: [Docker Docs](https://docs.docker.com)
- **Flask**: [Flask Docs](https://flask.palletsprojects.com)

---

**Ready to deploy?** Choose your platform and follow the steps above! 🚀
