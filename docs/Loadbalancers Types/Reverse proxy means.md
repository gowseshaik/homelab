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