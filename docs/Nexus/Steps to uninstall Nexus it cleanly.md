If you installed **Nexus 3 on Ubuntu manually** (not via package manager), follow these steps to uninstall it cleanly:
### ✅ 1. **Stop the Nexus service**
```bash
sudo systemctl stop nexus
```
### ✅ 2. **Disable the service**
```bash
sudo systemctl disable nexus
```
### ✅ 3. **Remove the service file**
```bash
sudo rm /etc/systemd/system/nexus.service
sudo systemctl daemon-reload
```
### ✅ 4. **Remove Nexus installation directory**
> Replace path if you used a different install location
```bash
sudo rm -rf /opt/nexus
sudo rm -rf /opt/sonatype-work
```
### ✅ 5. **Remove nexus user (if created)**
```bash
sudo userdel -r nexus
```
### ✅ 6. **Remove logs or custom configs (if any)**
```bash
sudo rm -rf /var/log/nexus
sudo rm -rf /etc/nexus
```
