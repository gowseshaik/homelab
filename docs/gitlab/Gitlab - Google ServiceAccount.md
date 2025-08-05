# 🔐 Service Account Creation Guide (Google → GitLab)

## **📍 WHERE TO CREATE: Google Cloud Platform**
Service accounts are created in **Google Cloud Console**, then the credentials are stored in **GitLab**. Here's the exact process:

## **🚀 STEP 1: CREATE GOOGLE CLOUD PROJECT**

### **1.1 Go to Google Cloud Console**

- 🌐 Visit: [console.cloud.google.com](https://console.cloud.google.com/)
- 📝 Sign in with your Google account (free account works fine)
### **1.2 Create New Project**
```
1. Click "Select a project" (top bar)
2. Click "NEW PROJECT" 
3. Enter project name: "Superstar-Analysis"
4. Click "CREATE"
5. Wait 30 seconds for project creation
```
### **1.3 Select Your Project**
```
1. Click project selector (top bar)
2. Choose "Superstar-Analysis" 
3. Verify project name shows in top bar
```

## **🔧 STEP 2: ENABLE REQUIRED APIs**

### **2.1 Enable Google Sheets API**
```
1. Go to "APIs & Services" > "Library" (left sidebar)
2. Search: "Google Sheets API"
3. Click on "Google Sheets API" 
4. Click "ENABLE" button
5. Wait for confirmation ✅
```

### **2.2 Enable Google Drive API**
```
1. In the same "Library" page
2. Search: "Google Drive API"
3. Click on "Google Drive API"
4. Click "ENABLE" button  
5. Wait for confirmation ✅
```

## **👤 STEP 3: CREATE SERVICE ACCOUNT**

### **3.1 Navigate to Service Accounts**
```
1. Go to "APIs & Services" > "Credentials" (left sidebar)
2. Click "CREATE CREDENTIALS" (top)
3. Select "Service account"
```
### **3.2 Configure Service Account**
```
Service account details:
┌─────────────────────────────────────┐
│ Service account name: superstar-bot │
│ Service account ID: superstar-bot   │
│ Description: CSV to Sheets uploader │
└─────────────────────────────────────┘

Click "CREATE AND CONTINUE"
```
### **3.3 Skip Role Assignment (Optional)**
```
Grant this service account access to project:
┌─────────────────────────────────────┐
│ Select a role: [SKIP - Click CONTINUE] │
└─────────────────────────────────────┘

Click "CONTINUE" (no roles needed)
```
### **3.4 Skip User Access (Optional)**
```
Grant users access to this service account:
┌─────────────────────────────────────┐
│ [SKIP - Click DONE]                 │
└─────────────────────────────────────┘

Click "DONE"
```
## **🔑 STEP 4: GENERATE CREDENTIALS**

### **4.1 Find Your Service Account**
```
1. You'll see service accounts list
2. Find: superstar-bot@your-project.iam.gserviceaccount.com
3. Click on the EMAIL ADDRESS (not the pencil icon)
```
### **4.2 Create Key**
```
1. Click "KEYS" tab
2. Click "ADD KEY" dropdown
3. Select "Create new key"
4. Choose format: JSON ✅ (not P12)
5. Click "CREATE"
```
### **4.3 Download & Save JSON**
```
🔽 Browser will download: superstar-bot-xxxxx.json

⚠️  IMPORTANT: This file contains your credentials!
   • Save it safely
   • Don't commit to git
   • Don't share publicly
```

## **🏗️ STEP 5: SETUP IN GITLAB**

### **5.1 Open Your JSON File**
```bash
# Open the downloaded JSON file
cat superstar-bot-xxxxx.json
```

### **5.2 Copy JSON Content**
```json
{
  "type": "service_account",
  "project_id": "superstar-analysis-xxxxx",
  "private_key_id": "xxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\nxxxxx\n-----END PRIVATE KEY-----\n",
  "client_email": "superstar-bot@superstar-analysis-xxxxx.iam.gserviceaccount.com",
  "client_id": "xxxxx",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/superstar-bot%40superstar-analysis-xxxxx.iam.gserviceaccount.com"
}
```

### **5.3 Add to GitLab CI Variables**
```
1. Go to your GitLab project
2. Settings > CI/CD > Variables
3. Click "Add variable"

Variable details:
┌─────────────────────────────────────────────┐
│ Key: GOOGLE_SERVICE_ACCOUNT_JSON             │
│ Value: [PASTE ENTIRE JSON CONTENT HERE]     │
│ Type: Variable                               │
│ Environment scope: All                       │
│ ✅ Protect variable                          │
│ ✅ Mask variable                             │
│ ❌ Expand variable reference                 │
└─────────────────────────────────────────────┘

Click "Add variable"
```

## **✅ STEP 6: VERIFY SETUP**

### **6.1 Test Authentication**
Add this test job to your `.gitlab-ci.yml`:
```yaml
test_google_auth:
  stage: test
  image: python:3.9
  before_script:
    - pip install gspread google-auth
  script:
    - |
      python3 -c "
      import gspread
      from google.oauth2.service_account import Credentials
      import json
      import os
      
      # Test authentication
      creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
      scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
      creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=scope)
      gc = gspread.authorize(creds)
      
      print('✅ Authentication successful!')
      print(f'Service account email: {creds.service_account_email}')
      "
  only:
    - main
  tags:
    - dev
```

## **🔍 VISUAL SUMMARY**
```
🌐 Google Cloud Console
    ↓ Create Project
📁 Superstar-Analysis Project  
    ↓ Enable APIs
🔧 APIs: Sheets + Drive
    ↓ Create Service Account
👤 superstar-bot@project.iam.gserviceaccount.com
    ↓ Generate JSON Key
🔑 superstar-bot-xxxxx.json
    ↓ Copy JSON Content
📋 {service account credentials}
    ↓ Add to GitLab
🏗️  GitLab Project > CI/CD > Variables
    ↓ Environment Variable
🔐 GOOGLE_SERVICE_ACCOUNT_JSON = {credentials}
    ↓ Use in Pipeline
🚀 Python script authenticates & uploads
```

## **🛡️ SECURITY BEST PRACTICES**

### **✅ DO:**
- Store JSON in GitLab CI Variables (encrypted)
- Mark variable as "Protected" and "Masked"
- Use environment variables in code
- Delete downloaded JSON file after setup

### **❌ DON'T:**
- Commit JSON file to repository
- Share JSON content publicly
- Store in plain text files
- Email or message credentials

## **🔧 TROUBLESHOOTING**

### **Common Issues:**
**❌ "Invalid JSON format"**
```
• Ensure entire JSON is copied (including { })
• No extra spaces or characters
• Check for line breaks in private_key
```

**❌ "Authentication failed"**
```
• Verify APIs are enabled (Sheets + Drive)
• Check project ID matches JSON
• Ensure service account exists
```

**❌ "Permission denied"**
```
• Service account needs to share files with your email
• Or make spreadsheets public
• Check file sharing permissions
```

## **🎯 FINAL RESULT**
After setup, your pipeline will:

1. ✅ Authenticate using service account
2. ✅ Create Google Spreadsheet
3. ✅ Upload CSV data
4. ✅ Share spreadsheet (if configured)
5. ✅ Send Telegram with link

**Total cost: $0 forever** 🎉


```
test_google_auth:
  stage: test
  image: google/cloud-sdk:stable
  before_script:
    - echo "🐍 Setting up environment..."
    - python --version
    - pip --version
    - echo "📦 Installing Python dependencies..."
    - pip install --no-cache-dir gspread google-auth
  script:
    - |
      echo "🔐 Starting Google Sheets authentication test..."
      python <<EOF
      import os
      import json
      import gspread
      from google.oauth2.service_account import Credentials
      
      print("1️⃣ Checking credentials...")
      creds_json = os.getenv('TRENDYLYNE_GOOGLE_SA_JSON')
      if not creds_json:
          raise Exception("Missing service account JSON")
      
      try:
          print("2️⃣ Initializing client...")
          creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=[
              'https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive'
          ])
          gc = gspread.authorize(creds)
          
          print("3️⃣ Testing API access...")
          sheets = gc.openall(limit=1)
          print(f"✅ Success! Found {len(sheets)} spreadsheets")
          if sheets:
              print(f"First sheet: {sheets[0].title}")
      
      except Exception as e:
          print(f"❌ Failed: {str(e)}")
          exit(1)
      EOF
    - echo "✅ Google Sheets test completed"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: always
    - if: $CI_COMMIT_BRANCH != "main"
      when: manual
  tags:
    - dev
```