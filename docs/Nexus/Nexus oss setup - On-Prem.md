<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
# ✅ Use this correct working download command:
```
wget https://sonatype-download.global.ssl.fastly.net/repository/downloads-prod-group/3/nexus-3.81.1-01-linux-x86_64.tar.gz
```

🔄 After downloading:
```
tar -xvzf nexus-3.68.0-01-unix.tar.gz
mv nexus-3.68.0-01 nexus
```
### ✅ Steps to run Nexus under systemd with current user

> Assuming Nexus is extracted to: `~/nexus`  
> And data dir is: `~/sonatype-work`

1. **Edit the `nexus.rc` file**  
    Set run_as_user empty so it runs as current user:
    ```bash
    echo 'run_as_user=""' > ~/nexus/bin/nexus.rc
    ```

2. **Create a systemd service file**
```bash
sudo tee /etc/systemd/system/nexus.service > /dev/null <<EOF
[Unit]
Description=Nexus Repository Manager
After=network.target

[Service]
Type=forking
ExecStart=${HOME}/nexus3/nexus/bin/nexus start
ExecStop=${HOME}/nexus3/nexus/bin/nexus stop
User=${USER}
Restart=on-abort
LimitNOFILE=65536
TimeoutStartSec=120

[Install]
WantedBy=multi-user.target
EOF
```

3. **Reload systemd and enable the service**
```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable nexus
```

4. **Start Nexus manually (first time)**
```bash
sudo systemctl start nexus
```

5. **Check service status**
```bash
sudo systemctl status nexus
```

Now Nexus will start automatically on boot under your user.

```
http://localhost:8081
get the default password: 
/home/gouse/nexus3/sonatype-work/nexus3/admin.password
```

By **default**, **Nexus Repository Manager OSS** does **not support external databases**. It uses an **embedded, file-based database (OrientDB)** stored in:

```
<sonatype-work>/nexus3/db/
```

### ❌ No Support for External Databases Like:

|Database|Supported?|Notes|
|---|---|---|
|PostgreSQL|❌|Not supported|
|MySQL/MariaDB|❌|Not supported|
|Oracle DB|❌|Not supported|
|MongoDB|❌|Not supported|
### ✅ What Nexus Does Support:

|Component|Type|Notes|
|---|---|---|
|Metadata & config|Embedded DB|Uses embedded OrientDB|
|Blob storage (artifacts)|File system or S3|You can configure external blob stores|
|LDAP/SSO|External service|Used for auth, not data|
### 🔐 Nexus Pro/Enterprise Edition Adds:

- High Availability (HA)
- External object stores
- Smart proxy features  
    But **still no external RDBMS** support — everything remains file/embedded based.

### ✅ Conclusion:

You **cannot use an external DB like PostgreSQL/MySQL** with Nexus.  
All metadata and artifact info is stored internally, and backups are done by **snapshotting the `sonatype-work/nexus3` directory**.

Let me know if you want steps to **move blob storage to S3** or other persistent volume setup.
### ⚙️ Recommended Use in OSS

1. Use **MinIO/SeaweedFS/GlusterFS** as a **mounted local filesystem**
2. Point Nexus File Blob Store to that mount
3. Use `rclone`/`restic` to backup to S3/GCS

✅ Open Source Blob Storage Tools

| Tool           | Type                       | Compatible Use Case for Nexus OSS  | Notes                                          |
| -------------- | -------------------------- | ---------------------------------- | ---------------------------------------------- |
| **MinIO**      | S3-compatible Object Store | ❌* (not natively supported in OSS) | Can be used with `rclone` or as NFS-like mount |
| **SeaweedFS**  | Distributed File System    | ✅ (mountable as local FS)          | Lightweight and good for blob storage          |
| **CephFS**     | Distributed File System    | ✅ (via mount)                      | Reliable at scale, mountable as local FS       |
| **Nextcloud**  | File Sync & Share          | ⚠️ (manual upload/backup)          | Useful for syncing artifacts externally        |
| **rclone**     | Sync tool (S3, GCS, etc.)  | ✅ (for sync/backup)                | Can sync blobs from Nexus to cloud storage     |
| **Restic**     | Backup tool                | ✅ (backup sonatype-work directory) | Can back up to S3, GCS, etc.                   |
| **BorgBackup** | Backup tool                | ✅                                  | Fast deduplicated backup of blob data          |
| **GlusterFS**  | Distributed File System    | ✅                                  | Mount as blob store in Nexus OSS               |
