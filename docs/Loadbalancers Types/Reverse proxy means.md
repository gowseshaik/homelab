<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

A **reverse proxy** is a server that sits **in front of one or more backend servers** and forwards **client requests to those servers**. It hides the backend servers from clients and can provide:

- **Load balancing**
- **SSL termination**
- **Caching**
- **Compression**
- **Security filtering**
### Simple flow:
```
Client → Reverse Proxy → Backend Server
```
### Example:
When you access a website:
```
User → Nginx (Reverse Proxy) → Web App Server
```

The client doesn’t see or talk directly to the backend server—only to the reverse proxy.