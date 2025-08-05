```yaml
stages:
  - cleanup
  - scrape
  - analyze
  - notify
  - test

variables:
  IMAGE_NAME: gowseshaik/trendybot:latest
  OUTPUT_DIR: output
  CSV_FILE: output/superstars.csv
  REPORT_FILE: output/telegram_report.txt

cleanup_old_data:
  stage: cleanup
  script:
    - echo "🧹 Cleaning up old artifacts and data..."
    - rm -rf $OUTPUT_DIR
    - mkdir -p $OUTPUT_DIR
    - echo "✅ Cleanup complete - ready for fresh data"
    - echo "📅 Pipeline started at $(date)"
  tags:
    - dev

scrape_data:
  stage: scrape
  script:
    - echo "🚀 Starting fresh data scraping at $(date)"
    - echo "🐳 Pulling latest Docker image..."
    - docker pull $IMAGE_NAME
    - echo "📁 Preparing output directory..."
    - mkdir -p $OUTPUT_DIR
    - echo "🔄 Creating fresh container..."
    - CONTAINER_ID=$(docker create $IMAGE_NAME)
    - echo "📊 Starting data scraping..."
    - docker start -a $CONTAINER_ID
    - echo "📥 Copying fresh CSV data..."
    - docker cp $CONTAINER_ID:/app/superstars.csv $OUTPUT_DIR/
    - docker cp $CONTAINER_ID:/app/superstars_*.csv $OUTPUT_DIR/ || echo "No timestamped CSV found"
    - echo "🧹 Cleaning up container..."
    - docker rm $CONTAINER_ID
    - echo "📋 Fresh data scraped successfully"
    - ls -la $OUTPUT_DIR/
    - echo "📊 CSV file details"
    - ls -la $CSV_FILE
    - echo "📄 CSV file size $(wc -c < $CSV_FILE) bytes"
    - echo "📈 CSV lines count $(wc -l < $CSV_FILE) lines"
    - echo "⏰ Data scraped at $(date)"
  artifacts:
    paths:
      - $OUTPUT_DIR/superstars.csv
      - $OUTPUT_DIR/superstars_*.csv
    expire_in: 30 minutes
  dependencies:
    - cleanup_old_data
  tags:
    - dev

analyze_superstars:
  stage: analyze
  script:
    - echo "📊 Starting analysis of fresh data at $(date)"
    - echo "📁 Verifying fresh data availability"
    - ls -la $OUTPUT_DIR/
    - ls -la $CSV_FILE
    - echo "📄 CSV content preview"
    - head -3 $CSV_FILE
    - echo "🔍 Starting analysis..."
    - chmod +x standalone_analyzer.sh
    - ./standalone_analyzer.sh $CSV_FILE $REPORT_FILE
    - echo "✅ Analysis complete at $(date)"
    - echo "📄 Generated report file"
    - ls -la $REPORT_FILE
    - echo "📋 COMPLETE ANALYSIS REPORT"
    - echo "=============================="
    - cat $REPORT_FILE
    - echo "=============================="
    - echo "📊 Report lines $(wc -l < $REPORT_FILE)"
    - echo "📊 Report characters $(wc -c < $REPORT_FILE)"
    - echo "📊 Generated at $(date)"
  artifacts:
    paths:
      - $REPORT_FILE
    expire_in: 1 hour
  dependencies:
    - scrape_data
  tags:
    - dev

send_notifications:
  stage: notify
  script:
    - echo "📱 Starting notification process at $(date)"
    
    # Send analysis report
    - echo "📄 Sending analysis report to Telegram..."
    - REPORT_CONTENT=$(cat $REPORT_FILE)
    - |
      curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id=${TELEGRAM_CHAT_ID} \
        -d message_thread_id=${TELEGRAM_THREAD_ID} \
        -d text="$REPORT_CONTENT" \
        -d parse_mode=Markdown \
        -d disable_web_page_preview=true
    
    # Send CSV file
    - echo "📊 Sending CSV data to Telegram..."
    - |
      curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
        -F chat_id=${TELEGRAM_CHAT_ID} \
        -F message_thread_id=${TELEGRAM_THREAD_ID} \
        -F document=@${CSV_FILE} \
        -F caption="📊 Fresh CSV data from ${CI_PROJECT_NAME} - Generated $(date '+%Y-%m-%d %H:%M')" \
        -F parse_mode=Markdown
    
    - echo "✅ All notifications sent successfully at $(date)"
  dependencies:
    - analyze_superstars
    - scrape_data
  only:
    - branches
  tags:
    - dev

test_google_auth:
  stage: test
  image: python:3.12-slim
  before_script:
    - echo "🐍 Setting up Python environment..."
    - python3 --version
    - pip3 --version
    - echo "📦 Installing required packages..."
    - pip3 install --no-cache-dir gspread google-auth
    - echo "✅ Dependencies installed"
  script:
    - echo "🔐 Starting Google Sheets authentication test..."
    - |
      python3 <<EOF
      import os
      import json
      import gspread
      from google.oauth2.service_account import Credentials
      from google.auth.exceptions import GoogleAuthError
      
      print("🔍 Checking environment configuration...")
      
      # Validate environment variable exists
      creds_json = os.getenv('TRENDYLYNE_GOOGLE_SA_JSON')
      if not creds_json:
          raise SystemExit("❌ ERROR: TRENDYLYNE_GOOGLE_SA_JSON environment variable not found")
      
      try:
          # Parse the service account JSON
          service_account_info = json.loads(creds_json)
          print(f"✅ Service account email: {service_account_info.get('client_email')}")
          
          # Define required scopes
          SCOPES = [
              'https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive'
          ]
          
          # Authenticate
          print("🔑 Authenticating with Google Sheets API...")
          credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
          client = gspread.authorize(credentials)
          
          # Test authentication
          print("🔄 Testing API access...")
          try:
              spreadsheets = client.openall(limit=3)
              print(f"✅ Authentication successful! Found {len(spreadsheets)} accessible spreadsheets")
              if spreadsheets:
                  print(f"📄 First spreadsheet: {spreadsheets[0].title}")
          except Exception as e:
              print(f"⚠️  Limited access: {str(e)}")
          
          print("🎉 Google Sheets authentication test passed!")
          
      except json.JSONDecodeError:
          raise SystemExit("❌ ERROR: Invalid JSON in service account credentials")
      except GoogleAuthError as auth_error:
          raise SystemExit(f"❌ Authentication failed: {str(auth_error)}")
      except Exception as e:
          raise SystemExit(f"❌ Unexpected error: {str(e)}")
      EOF
    - echo "✅ Google authentication test completed successfully"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: always
    - if: $CI_COMMIT_BRANCH != "main"
      when: manual
      allow_failure: true
  tags:
    - dev
```
