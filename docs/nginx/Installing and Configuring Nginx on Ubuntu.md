<span style="color:#4caf50;"><b>Created:</b> 2025-07-01</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

## Step 1: Install Nginx
1. Update your package index:
   ```bash
   sudo apt update
   ```

2. Install Nginx:
   ```bash
   sudo apt install nginx -y
   ```

3. Check if Nginx is running:
   ```bash
   sudo systemctl status nginx
   ```
   You should see "active (running)" status.

## Step 2: Configure Firewall
Allow Nginx through the firewall:
```bash
sudo ufw allow 'Nginx HTTP'
```

## Step 3: Create a Sample Application

1. Create a directory for your sample application:
   ```bash
   sudo mkdir -p /var/www/sample
   ```

2. Create a simple HTML file:
   ```bash
   sudo nano /var/www/sample/index.html
   ```

3. Add this content:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>Sample Application</title>
   </head>
   <body>
       <h1>Welcome to the Sample Application!</h1>
       <p>Nginx is successfully serving this page.</p>
   </body>
   </html>
   ```

4. Set proper permissions:
   ```bash
   sudo chown -R www-data:www-data /var/www/sample
   sudo chmod -R 755 /var/www/sample
   ```

## Step 4: Configure Nginx Server Block

1. Create a new server block configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/sample
   ```

2. Add this configuration (replace `your_domain_or_IP` with your server's IP or domain):
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_IP;

       root /var/www/sample;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

3. Enable the configuration by creating a symbolic link:
   ```bash
   sudo ln -s /etc/nginx/sites-available/sample /etc/nginx/sites-enabled/
   ```

4. Test the configuration for syntax errors:
   ```bash
   sudo nginx -t
   ```

5. Restart Nginx to apply changes:
   ```bash
   sudo systemctl restart nginx
   ```

## Step 5: Verify the Installation

Open your web browser and navigate to your server's IP address or domain name. You should see your sample application page.
## Optional: Additional Configurations

### Set Up a Domain Name
If you have a domain name, update your DNS records to point to your server's IP, then update the `server_name` in the Nginx configuration.
### Enable HTTPS with Let's Encrypt
1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

2. Obtain and install certificate:
   ```bash
   sudo certbot --nginx -d your_domain
   ```

3. Certbot will automatically update your Nginx configuration to use HTTPS.
## Troubleshooting

- If you get a 403 Forbidden error, check permissions on your web directory.
- Check Nginx error logs: `/var/log/nginx/error.log`
- If changes don't appear, try clearing your browser cache or use incognito mode.
