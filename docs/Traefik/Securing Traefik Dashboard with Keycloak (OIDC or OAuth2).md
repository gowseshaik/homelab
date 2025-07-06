<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
# Securing Traefik Dashboard with Keycloak (OIDC/OAuth2)

Yes, you can definitely use Keycloak instead of basic auth to secure your Traefik dashboard. This is a more secure and modern approach using OIDC/OAuth2. Here's how to set it up:

## Prerequisites
- Running Keycloak instance
- Traefik deployed (preferably via Helm)

## Step 1: Configure Keycloak

1. **Create a new client in Keycloak**:
   - Client ID: `traefik-dashboard`
   - Client Protocol: `openid-connect`
   - Root URL: `https://traefik.yourdomain.com`
   - Valid Redirect URIs: `https://traefik.yourdomain.com/oauth2/callback`
   - Web Origins: `+`
   - Access Type: `confidential`
   - Standard Flow Enabled: ON

2. **Create roles** (e.g., `traefik-admin`) and assign them to users

3. **Note down these values** from the client's "Credentials" tab:
   - Client ID
   - Client Secret

## Step 2: Configure Traefik with Keycloak Integration

### Using Helm Values

Update your `values.yaml`:

```yaml
additionalArguments:
  - --api.dashboard=true
  - --providers.kubernetesingress
  - --providers.kubernetescrd
  - --entrypoints.web.address=:80
  - --entrypoints.websecure.address=:443
  - --certificatesresolvers.default.acme.tlschallenge=true
  - --certificatesresolvers.default.acme.email=your@email.com
  - --certificatesresolvers.default.acme.storage=/data/acme.json

ingressRoute:
  dashboard:
    enabled: true
    matchRule: Host(`traefik.yourdomain.com`) && (PathPrefix(`/api`) || PathPrefix(`/dashboard`))
    entryPoints: ["websecure"]
    middlewares:
      - name: keycloak-auth
    tls:
      certResolver: default

middlewares:
  keycloak-auth:
    enabled: true
    forwardAuth:
      address: "https://keycloak.yourdomain.com/auth/realms/your-realm/protocol/openid-connect/auth"
      trustForwardHeader: true
      authResponseHeaders:
        - "X-Forwarded-User"
        - "Authorization"
```

### Create ForwardAuth Middleware (Alternative)

For more control, create a separate ForwardAuth middleware:

```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: keycloak-oauth
spec:
  forwardAuth:
    address: "https://keycloak.yourdomain.com/auth/realms/your-realm/protocol/openid-connect/auth"
    authResponseHeaders:
      - "X-Forwarded-User"
      - "Authorization"
    tls:
      insecureSkipVerify: false # Set to true if using self-signed certs
```

## Step 3: Configure Keycloak Authentication Flow

1. In Keycloak, go to your client's settings
2. Add these valid redirect URIs:
   - `https://traefik.yourdomain.com/oauth2/callback`
   - `https://traefik.yourdomain.com/dashboard/*`
3. Configure roles/scopes as needed

## Step 4: Deploy the Configuration

```bash
helm upgrade --install traefik traefik/traefik -f values.yaml -n traefik
```

## Verification

1. Access `https://traefik.yourdomain.com/dashboard/`
2. You should be redirected to Keycloak for authentication
3. After successful login, you'll be redirected back to the Traefik dashboard

## Additional Security Recommendations

1. **Add role-based access**:
   ```yaml
   # In your middleware configuration
   labels:
     traefik.forwardauth.authResponseHeadersRegex: "^X-Forwarded-User$"
     traefik.forwardauth.authResponseHeaders: "X-Forwarded-User, Authorization"
   ```

2. **Enable HTTPS everywhere**:
   ```yaml
   additionalArguments:
     - --entrypoints.web.http.redirections.entryPoint.to=websecure
     - --entrypoints.web.http.redirections.entryPoint.scheme=https
   ```

3. **Configure session timeout** in Keycloak client settings

This setup provides much better security than basic auth, with features like:
- Single Sign-On (SSO)
- Multi-factor authentication
- Session management
- Fine-grained access control
- Token expiration

