## Project Structure

```
amazon-affiliate-scraper/
├── services/
│   ├── scraper-service/
│   │   ├── src/
│   │   │   ├── scrapers/
│   │   │   │   ├── amazon_scraper.py
│   │   │   │   └── base_scraper.py
│   │   │   ├── models/
│   │   │   │   └── product.py
│   │   │   ├── utils/
│   │   │   │   ├── rate_limiter.py
│   │   │   │   └── proxy_manager.py
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── data-service/
│   │   ├── src/
│   │   │   ├── storage/
│   │   │   │   ├── csv_handler.py
│   │   │   │   └── image_downloader.py
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── api-gateway/
│       ├── src/
│       │   ├── routes/
│       │   │   └── scraper_routes.py
│       │   └── main.py
│       ├── requirements.txt
│       └── Dockerfile
├── shared/
│   ├── config/
│   │   └── settings.py
│   └── messaging/
│       └── queue_manager.py
├── data/
│   ├── csv/
│   └── images/
├── docker-compose.yml
└── README.md
```

## Critical Analysis & First Principles

**Legal Considerations:**
- Amazon's robots.txt and Terms of Service restrict automated scraping
- You'll need to use Amazon's Product Advertising API instead for compliance
- Direct scraping violates their terms and can result in IP bans

**Technical Challenges:**
- Anti-bot measures (CAPTCHAs, rate limiting, IP blocking)
- Dynamic content loading requiring browser automation
- Affiliate link generation requires API access
- Image copyright considerations

## Implementation Steps

### Step 1: Set Up Amazon Product Advertising API
```python
# services/scraper-service/src/scrapers/amazon_api.py
import boto3
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest

class AmazonAPIClient:
    def __init__(self, access_key, secret_key, partner_tag, host, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.partner_tag = partner_tag
        self.host = host
        self.region = region
        
    def get_bestsellers(self, category, max_items=50):
        # Implementation using Product Advertising API
        pass
```

### Step 2: Product Data Model
```python
# shared/models/product.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Product:
    asin: str
    title: str
    price: float
    rating: float
    review_count: int
    image_url: str
    affiliate_url: str
    category: str
    rank: int
    description: Optional[str] = None
    features: List[str] = None
```

### Step 3: Data Processing Service
```python
# services/data-service/src/storage/csv_handler.py
import csv
import pandas as pd
from typing import List
from shared.models.product import Product

class CSVHandler:
    def __init__(self, output_path: str):
        self.output_path = output_path
        
    def save_products(self, products: List[Product]):
        df = pd.DataFrame([product.__dict__ for product in products])
        df.to_csv(self.output_path, index=False)
        
    def append_products(self, products: List[Product]):
        # Append to existing CSV
        pass
```

### Step 4: Image Download Service
```python
# services/data-service/src/storage/image_downloader.py
import aiohttp
import asyncio
from pathlib import Path

class ImageDownloader:
    def __init__(self, download_path: str):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
    async def download_image(self, url: str, filename: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(self.download_path / filename, 'wb') as f:
                        f.write(content)
```

### Step 5: Microservice Communication
```python
# shared/messaging/queue_manager.py
import redis
import json
from typing import Dict, Any

class MessageQueue:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
        
    def publish(self, channel: str, message: Dict[Any, Any]):
        self.redis_client.publish(channel, json.dumps(message))
        
    def subscribe(self, channel: str):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        return pubsub
```

### Step 6: Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
      
  scraper-service:
    build: ./services/scraper-service
    environment:
      - REDIS_URL=redis://redis:6379
      - AMAZON_ACCESS_KEY=${AMAZON_ACCESS_KEY}
      - AMAZON_SECRET_KEY=${AMAZON_SECRET_KEY}
    depends_on:
      - redis
      
  data-service:
    build: ./services/data-service
    environment:
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
      
  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8000:8000"
    depends_on:
      - scraper-service
      - data-service
```

## Alternative Approaches

**Option 1: Use Amazon's Official APIs**
- Product Advertising API for product data
- Associates Program for affiliate links
- Compliant but requires approval

**Option 2: Third-party Data Providers**
- Services like Keepa, Jungle Scout APIs
- More expensive but legally compliant
- Better data quality and reliability

**Option 3: Manual Curation**
- Manually select bestselling products
- Use Amazon's bestseller lists as reference
- Slower but completely compliant

## Recommended Implementation Path

1. **Start with Amazon Product Advertising API** - Apply for API access through Amazon Associates
2. **Build data pipeline** - Focus on data processing and storage first
3. **Add rate limiting and error handling** - Essential for production use
4. **Implement monitoring** - Track API usage, success rates, errors
5. **Add data validation** - Ensure data quality before storage

The direct scraping approach has significant legal and technical risks. The API-based approach, while requiring approval, provides a sustainable and compliant solution for affiliate marketing data collection.

----


## Project Structure
Here's a detailed explanation of each line in the project structure with comments:

```
amazon-affiliate-scraper/                   # Root project directory
├── src/                                    # Main source code directory
│   ├── __init__.py                         # Makes 'src' a Python package
│   ├── config/                             # Configuration management
│   │   ├── __init__.py                     # Makes 'config' a Python package
│   │   └── settings.py                     # Application settings (delays, URLs, API keys)
│   ├── scrapers/                           # Web scraping logic
│   │   ├── __init__.py                     # Makes 'scrapers' a Python package
│   │   ├── base_scraper.py                 # Abstract base class for all scrapers
│   │   └── amazon_scraper.py               # Amazon-specific scraping implementation
│   ├── data_handlers/                      # Data processing and storage
│   │   ├── __init__.py                     # Makes 'data_handlers' a Python package
│   │   ├── csv_handler.py                  # CSV file operations (read/write/update)
│   │   └── image_downloader.py             # Downloads and saves product images
│   ├── api/                                # REST API layer
│   │   ├── __init__.py                     # Makes 'api' a Python package
│   │   ├── app.py                          # FastAPI application setup and configuration
│   │   └── routes.py                       # API endpoints and request handlers
│   └── utils/                              # Utility functions and helpers
│       ├── __init__.py                     # Makes 'utils' a Python package
│       ├── logger.py                       # Logging configuration and setup
│       └── helpers.py                      # Common utility functions
├── data/                                   # Data storage directory
│   ├── products.csv                        # CSV file storing scraped product data
│   └── images/                             # Directory for downloaded product images
├── logs/                                   # Application logs directory
├── tests/                                  # Unit and integration tests
│   ├── __init__.py                         # Makes 'tests' a Python package
│   └── test_scraper.py                     # Test cases for scraper functionality
├── requirements.txt                        # Python dependencies list
├── docker-compose.yml                      # Multi-container Docker application definition
├── Dockerfile                              # Docker image build instructions
└── README.md                               # Project documentation and setup guide
```

## Detailed Breakdown by Directory:

### **Root Level Files:**
- **`requirements.txt`**: Lists all Python packages needed (FastAPI, BeautifulSoup, etc.)
- **`docker-compose.yml`**: Defines how to run the app in containers with volumes and ports
- **`Dockerfile`**: Instructions to build a Docker image of the application
- **`README.md`**: Documentation explaining how to install, configure, and use the project

### **`src/` Directory (Main Application Code):**
- **`__init__.py`**: Empty file that tells Python this directory contains importable modules
- **Purpose**: Contains all the business logic and application code

### **`src/config/` Directory (Configuration Management):**
- **`settings.py`**: Centralized configuration file containing:
  - Scraping delays and timeouts
  - File paths for data storage
  - API server settings
  - User agent strings for web requests
  - Amazon categories to scrape

### **`src/scrapers/` Directory (Web Scraping Logic):**
- **`base_scraper.py`**: Abstract class defining common scraping functionality:
  - HTTP request handling with retries
  - User agent rotation
  - Rate limiting between requests
  - Error handling and logging
- **`amazon_scraper.py`**: Amazon-specific implementation:
  - Parses Amazon search result pages
  - Extracts product titles, prices, ratings, images
  - Generates affiliate links
  - Handles Amazon's specific HTML structure

### **`src/data_handlers/` Directory (Data Processing):**
- **`csv_handler.py`**: Manages CSV file operations:
  - Saves scraped products to CSV
  - Loads existing products from CSV
  - Handles duplicate removal
  - Manages data formatting
- **`image_downloader.py`**: Downloads product images:
  - Downloads images from URLs
  - Saves images with sanitized filenames
  - Handles image format conversion
  - Manages local image storage

### **`src/api/` Directory (REST API Layer):**
- **`app.py`**: FastAPI application setup:
  - Creates the main FastAPI instance
  - Configures API metadata (title, description)
  - Sets up startup/shutdown events
  - Includes route handlers
- **`routes.py`**: API endpoint definitions:
  - `/scrape/{category}` - Triggers scraping for a category
  - `/products` - Returns all scraped products
  - `/products/{category}` - Returns products by category
  - Background task management

### **`src/utils/` Directory (Utility Functions):**
- **`logger.py`**: Logging configuration:
  - Sets up file and console logging
  - Configures log formats and levels
  - Creates daily log files
  - Manages log rotation
- **`helpers.py`**: Common utility functions:
  - String sanitization
  - URL validation
  - Data transformation helpers
  - Common validation functions

### **`data/` Directory (Data Storage):**
- **`products.csv`**: Main data file storing:
  - Product titles and descriptions
  - Prices and ratings
  - Image URLs and local paths
  - Affiliate links
  - Category information
- **`images/`**: Directory containing:
  - Downloaded product images
  - Organized by product or category
  - Various image formats (JPG, PNG, etc.)

### **`logs/` Directory (Application Logs):**
- Contains daily log files with:
  - Scraping activity records
  - Error messages and stack traces
  - API request logs
  - Performance metrics

### **`tests/` Directory (Testing):**
- **`test_scraper.py`**: Test cases for:
  - Scraper functionality
  - Data validation
  - API endpoints
  - Error handling scenarios

## **File Naming Conventions:**
- **Snake_case**: Used for Python files (`amazon_scraper.py`)
- **Lowercase**: Used for directories (`data_handlers/`)
- **Descriptive names**: Each file clearly indicates its purpose
- **Separation of concerns**: Each file has a single responsibility

## **Architecture Benefits:**
- **Modularity**: Each component can be developed and tested independently
- **Scalability**: Easy to add new scrapers or data handlers
- **Maintainability**: Clear separation makes debugging easier
- **Testability**: Each module can be unit tested separately
- **Deployment**: Docker setup allows easy deployment anywhere

This structure follows Python best practices and microservice architecture principles, making the codebase professional and maintainable.

Here's a one-line command to create the entire project structure:

## For Linux/macOS (Bash):
```bash
mkdir -p amazon-affiliate-scraper/{src/{config,scrapers,data_handlers,api,utils},data/images,logs,tests} && cd amazon-affiliate-scraper && touch src/__init__.py src/config/{__init__.py,settings.py} src/scrapers/{__init__.py,base_scraper.py,amazon_scraper.py} src/data_handlers/{__init__.py,csv_handler.py,image_downloader.py} src/api/{__init__.py,app.py,routes.py} src/utils/{__init__.py,logger.py,helpers.py} tests/{__init__.py,test_scraper.py} data/products.csv requirements.txt docker-compose.yml Dockerfile README.md
```

## For Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Path "amazon-affiliate-scraper\src\config", "amazon-affiliate-scraper\src\scrapers", "amazon-affiliate-scraper\src\data_handlers", "amazon-affiliate-scraper\src\api", "amazon-affiliate-scraper\src\utils", "amazon-affiliate-scraper\data\images", "amazon-affiliate-scraper\logs", "amazon-affiliate-scraper\tests" -Force; Set-Location amazon-affiliate-scraper; New-Item -ItemType File -Path "src\__init__.py", "src\config\__init__.py", "src\config\settings.py", "src\scrapers\__init__.py", "src\scrapers\base_scraper.py", "src\scrapers\amazon_scraper.py", "src\data_handlers\__init__.py", "src\data_handlers\csv_handler.py", "src\data_handlers\image_downloader.py", "src\api\__init__.py", "src\api\app.py", "src\api\routes.py", "src\utils\__init__.py", "src\utils\logger.py", "src\utils\helpers.py", "tests\__init__.py", "tests\test_scraper.py", "data\products.csv", "requirements.txt", "docker-compose.yml", "Dockerfile", "README.md" -Force
```

## For Windows (Command Prompt):
```cmd
mkdir amazon-affiliate-scraper\src\config amazon-affiliate-scraper\src\scrapers amazon-affiliate-scraper\src\data_handlers amazon-affiliate-scraper\src\api amazon-affiliate-scraper\src\utils amazon-affiliate-scraper\data\images amazon-affiliate-scraper\logs amazon-affiliate-scraper\tests && cd amazon-affiliate-scraper && type nul > src\__init__.py && type nul > src\config\__init__.py && type nul > src\config\settings.py && type nul > src\scrapers\__init__.py && type nul > src\scrapers\base_scraper.py && type nul > src\scrapers\amazon_scraper.py && type nul > src\data_handlers\__init__.py && type nul > src\data_handlers\csv_handler.py && type nul > src\data_handlers\image_downloader.py && type nul > src\api\__init__.py && type nul > src\api\app.py && type nul > src\api\routes.py && type nul > src\utils\__init__.py && type nul > src\utils\logger.py && type nul > src\utils\helpers.py && type nul > tests\__init__.py && type nul > tests\test_scraper.py && type nul > data\products.csv && type nul > requirements.txt && type nul > docker-compose.yml && type nul > Dockerfile && type nul > README.md
```

## Alternative: Python Script (Cross-platform)
Create a file called `create_structure.py` and run it:

```python
import os

structure = {
    'amazon-affiliate-scraper': {
        'src': {
            '__init__.py': '',
            'config': {
                '__init__.py': '',
                'settings.py': ''
            },
            'scrapers': {
                '__init__.py': '',
                'base_scraper.py': '',
                'amazon_scraper.py': ''
            },
            'data_handlers': {
                '__init__.py': '',
                'csv_handler.py': '',
                'image_downloader.py': ''
            },
            'api': {
                '__init__.py': '',
                'app.py': '',
                'routes.py': ''
            },
            'utils': {
                '__init__.py': '',
                'logger.py': '',
                'helpers.py': ''
            }
        },
        'data': {
            'products.csv': '',
            'images': {}
        },
        'logs': {},
        'tests': {
            '__init__.py': '',
            'test_scraper.py': ''
        },
        'requirements.txt': '',
        'docker-compose.yml': '',
        'Dockerfile': '',
        'README.md': ''
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)

create_structure('.', structure)
print("Project structure created successfully!")
```

Then run:
```bash
python create_structure.py
```

The **Linux/macOS bash command** is the most concise single-line option. After running it, you'll have the complete directory structure with all empty files ready for implementation.

## Implementation Steps

### 1. Environment Setup

**requirements.txt:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
pandas==2.1.3
Pillow==10.1.0
fake-useragent==1.4.0
python-dotenv==1.0.0
aiofiles==23.2.1
pytest==7.4.3
```

### 2. Configuration

**src/config/settings.py:**
```python
import os
from typing import List

class Settings:
    # Scraping settings
    REQUEST_DELAY = 2  # seconds between requests
    MAX_RETRIES = 3
    TIMEOUT = 30
    
    # Data settings
    CSV_FILE_PATH = "data/products.csv"
    IMAGES_DIR = "data/images"
    
    # API settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # User agents rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
    
    # Amazon categories to scrape
    CATEGORIES = [
        "electronics",
        "books",
        "home-kitchen",
        "clothing"
    ]

settings = Settings()
```

### 3. Base Scraper

**src/scrapers/base_scraper.py:**
```python
import time
import random
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from fake_useragent import UserAgent
from src.utils.logger import get_logger
from src.config.settings import settings

class BaseScraper(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.logger = get_logger(__name__)
        
    def get_headers(self) -> Dict[str, str]:
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def make_request(self, url: str, retries: int = 0) -> Optional[requests.Response]:
        if retries >= settings.MAX_RETRIES:
            self.logger.error(f"Max retries exceeded for {url}")
            return None
            
        try:
            time.sleep(random.uniform(1, settings.REQUEST_DELAY))
            response = self.session.get(
                url, 
                headers=self.get_headers(),
                timeout=settings.TIMEOUT
            )
            response.raise_for_status()
            return response
            
        except requests.RequestException as e:
            self.logger.warning(f"Request failed for {url}: {e}")
            return self.make_request(url, retries + 1)
    
    @abstractmethod
    def scrape_products(self, category: str) -> List[Dict]:
        pass
```

### 4. Amazon Scraper

**src/scrapers/amazon_scraper.py:**
```python
import re
from typing import Dict, List
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from src.scrapers.base_scraper import BaseScraper

class AmazonScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.amazon.com"
        
    def scrape_products(self, category: str, pages: int = 3) -> List[Dict]:
        products = []
        
        for page in range(1, pages + 1):
            url = f"{self.base_url}/s?k=best+sellers+{category}&page={page}"
            response = self.make_request(url)
            
            if not response:
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for container in product_containers:
                product = self._extract_product_data(container)
                if product:
                    products.append(product)
                    
        return products
    
    def _extract_product_data(self, container) -> Dict:
        try:
            # Title
            title_elem = container.find('h2', class_='a-size-mini')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Price
            price_elem = container.find('span', class_='a-price-whole')
            price = price_elem.get_text(strip=True) if price_elem else "N/A"
            
            # Rating
            rating_elem = container.find('span', class_='a-icon-alt')
            rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
            
            # Image URL
            img_elem = container.find('img', class_='s-image')
            image_url = img_elem.get('src') if img_elem else None
            
            # Product URL
            link_elem = container.find('h2').find('a') if container.find('h2') else None
            product_url = urljoin(self.base_url, link_elem.get('href')) if link_elem else None
            
            # Generate affiliate link (placeholder)
            affiliate_link = self._generate_affiliate_link(product_url) if product_url else None
            
            return {
                'title': title,
                'price': price,
                'rating': rating,
                'image_url': image_url,
                'product_url': product_url,
                'affiliate_link': affiliate_link,
                'category': category
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting product data: {e}")
            return None
    
    def _generate_affiliate_link(self, product_url: str) -> str:
        # Add your Amazon affiliate tag here
        affiliate_tag = "your-affiliate-tag"
        if '?' in product_url:
            return f"{product_url}&tag={affiliate_tag}"
        else:
            return f"{product_url}?tag={affiliate_tag}"
```

### 5. Data Handlers

**src/data_handlers/csv_handler.py:**
```python
import pandas as pd
import os
from typing import List, Dict
from src.config.settings import settings
from src.utils.logger import get_logger

class CSVHandler:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.csv_path = settings.CSV_FILE_PATH
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
    
    def save_products(self, products: List[Dict]) -> bool:
        try:
            df = pd.DataFrame(products)
            
            # Check if file exists to append or create new
            if os.path.exists(self.csv_path):
                existing_df = pd.read_csv(self.csv_path)
                df = pd.concat([existing_df, df], ignore_index=True)
                # Remove duplicates based on product_url
                df = df.drop_duplicates(subset=['product_url'], keep='last')
            
            df.to_csv(self.csv_path, index=False)
            self.logger.info(f"Saved {len(products)} products to {self.csv_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving products to CSV: {e}")
            return False
    
    def load_products(self) -> List[Dict]:
        try:
            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path)
                return df.to_dict('records')
            return []
        except Exception as e:
            self.logger.error(f"Error loading products from CSV: {e}")
            return []
```

**src/data_handlers/image_downloader.py:**
```python
import os
import requests
from urllib.parse import urlparse
from typing import Optional
from src.config.settings import settings
from src.utils.logger import get_logger

class ImageDownloader:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.images_dir = settings.IMAGES_DIR
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        os.makedirs(self.images_dir, exist_ok=True)
    
    def download_image(self, image_url: str, product_title: str) -> Optional[str]:
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Generate filename
            parsed_url = urlparse(image_url)
            extension = os.path.splitext(parsed_url.path)[1] or '.jpg'
            filename = f"{self._sanitize_filename(product_title)}{extension}"
            filepath = os.path.join(self.images_dir, filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"Downloaded image: {filename}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error downloading image {image_url}: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        # Remove invalid characters for filename
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:50]  # Limit length
```

### 6. API Layer

**src/api/app.py:**
```python
from fastapi import FastAPI, BackgroundTasks
from src.api.routes import router
from src.utils.logger import get_logger

app = FastAPI(
    title="Amazon Affiliate Scraper",
    description="Microservice for scraping Amazon products for affiliate marketing",
    version="1.0.0"
)

app.include_router(router)

logger = get_logger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Amazon Affiliate Scraper API started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Amazon Affiliate Scraper API stopped")
```

**src/api/routes.py:**
```python
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List, Dict
from src.scrapers.amazon_scraper import AmazonScraper
from src.data_handlers.csv_handler import CSVHandler
from src.data_handlers.image_downloader import ImageDownloader
from src.config.settings import settings

router = APIRouter()

@router.post("/scrape/{category}")
async def scrape_category(category: str, background_tasks: BackgroundTasks):
    if category not in settings.CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    background_tasks.add_task(scrape_and_save, category)
    return {"message": f"Scraping started for category: {category}"}

@router.get("/products")
async def get_products() -> List[Dict]:
    csv_handler = CSVHandler()
    products = csv_handler.load_products()
    return products

@router.get("/products/{category}")
async def get_products_by_category(category: str) -> List[Dict]:
    csv_handler = CSVHandler()
    products = csv_handler.load_products()
    filtered_products = [p for p in products if p.get('category') == category]
    return filtered_products

async def scrape_and_save(category: str):
    scraper = AmazonScraper()
    csv_handler = CSVHandler()
    image_downloader = ImageDownloader()
    
    # Scrape products
    products = scraper.scrape_products(category)
    
    # Download images
    for product in products:
        if product.get('image_url'):
            local_path = image_downloader.download_image(
                product['image_url'], 
                product['title']
            )
            product['local_image_path'] = local_path
    
    # Save to CSV
    csv_handler.save_products(products)
```

### 7. Utilities

**src/utils/logger.py:**
```python
import logging
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(
            f'logs/scraper_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
```

### 8. Docker Setup

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  scraper-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment