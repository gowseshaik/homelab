# **Real-World CronJob Example: Automated Database Backup & Cleanup**

Here's a complete, production-ready example of a Kubernetes CronJob that:
1. **Backs up a PostgreSQL database daily at 2 AM**
2. **Compresses the backup**
3. **Uploads it to AWS S3**
4. **Cleans up old backups (older than 7 days)**

## **1. The CronJob Definition**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: production
spec:
  schedule: "0 2 * * *"  # Runs at 2 AM UTC daily
  concurrencyPolicy: Forbid  # Prevents overlapping jobs
  successfulJobsHistoryLimit: 3  # Keeps logs of last 3 successes
  failedJobsHistoryLimit: 5      # Keeps logs of last 5 failures
  jobTemplate:
    spec:
      backoffLimit: 2  # Retries twice on failure
      template:
        spec:
          containers:
          - name: backup
            image: postgres:14.5
            env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
            - name: S3_BUCKET
              value: "my-db-backups"
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access_key
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret_key
            command: 
              - /bin/sh
              - -c
              - |
                # Create timestamped backup filename
                BACKUP_FILE="/backups/db-$(date +%Y-%m-%d-%H%M%S).sql"
                
                # Dump database
                pg_dump -U $POSTGRES_USER -h postgres-service.production.svc.cluster.local -d myapp > $BACKUP_FILE
                
                # Compress backup
                gzip $BACKUP_FILE
                
                # Upload to S3
                aws s3 cp ${BACKUP_FILE}.gz s3://${S3_BUCKET}/
                
                # Cleanup local files
                rm ${BACKUP_FILE}.gz
                
                # Delete backups older than 7 days from S3
                aws s3 ls s3://${S3_BUCKET}/ | \
                awk '{print $4}' | \
                while read -r file; do
                  file_date=$(echo $file | cut -d'-' -f2-4)
                  if [[ $(date -d "$file_date" +%s) -lt $(date -d "7 days ago" +%s) ]]; then
                    aws s3 rm s3://${S3_BUCKET}/$file
                  fi
                done
            volumeMounts:
            - name: backup-storage
              mountPath: /backups
          restartPolicy: OnFailure
          volumes:
          - name: backup-storage
            emptyDir: {}
```

## **2. Required Supporting Resources**

### **PostgreSQL Credentials Secret**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-credentials
  namespace: production
type: Opaque
data:
  username: base64_encoded_username
  password: base64_encoded_password
```

### **AWS S3 Credentials Secret**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: aws-credentials
  namespace: production
type: Opaque
data:
  access_key: base64_encoded_access_key
  secret_key: base64_encoded_secret_key
```

## **3. Key Features Explained**

1. **Security**:
   - Uses Kubernetes Secrets for sensitive data
   - Never stores credentials in the CronJob definition

2. **Reliability**:
   - Prevents concurrent runs with `concurrencyPolicy: Forbid`
   - Retries failed jobs twice (`backoffLimit: 2`)

3. **Storage Management**:
   - Uses `emptyDir` for temporary storage during backup
   - Automatically cleans up old backups (>7 days) from S3

4. **Monitoring**:
   - Keeps history of 3 successful and 5 failed runs
   - Easy to check logs with `kubectl logs <pod-name>`

## **4. How to Deploy & Test**

1. **Apply the configuration**:
   ```bash
   kubectl apply -f postgres-backup-cronjob.yaml
   kubectl apply -f postgres-secret.yaml
   kubectl apply -f aws-secret.yaml
   ```

2. **Verify the CronJob**:
   ```bash
   kubectl get cronjobs -n production
   kubectl describe cronjob/postgres-backup -n production
   ```

3. **Manually trigger for testing**:
   ```bash
   kubectl create job --from=cronjob/postgres-backup manual-test -n production
   ```

4. **Check logs**:
   ```bash
   # Get the pod name
   kubectl get pods -n production | grep manual-test

   # View logs
   kubectl logs <pod-name> -n production
   ```

## **5. Advanced Enhancements**

For production environments, consider adding:

1. **Notifications on failure** (via Slack/Email):
   ```yaml
   # Add to the container's command:
   - curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Database backup failed!"}' \
     $SLACK_WEBHOOK_URL || true
   ```

2. **Prometheus monitoring**:
   ```yaml
   annotations:
     prometheus.io/scrape: "true"
     prometheus.io/path: "/metrics"
   ```

3. **Backup verification**:
   ```bash
   # Add after upload to S3:
   aws s3 ls s3://${S3_BUCKET}/$(basename ${BACKUP_FILE}.gz) || \
   (echo "Backup verification failed!" && exit 1)
   ```

This example provides a complete, production-grade solution for database backups with proper security, reliability, and maintenance features. Would you like any modifications for your specific use case?