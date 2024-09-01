# Scraping Tool with FastAPI

This project is a web scraping tool built using the FastAPI framework. It scrapes product information from a target website and stores the data in a local JSON file or SQLite database. The tool supports multiple caching strategies and includes a simple authentication mechanism.

## Features

- Scrapes product name, price, and image from the target website.
- Supports limiting the number of pages to scrape.
- Uses proxy for scraping if provided.
- Stores scraped data in a local JSON file or SQLite database.
- Caches scraping results using Redis or in-memory caching.
- Notifies the user about the scraping status.
- Simple token-based authentication for the scraping endpoint.

## Project Structure


scraping_tool/ ├── main.py ├── scraper/ │ ├── init.py │ ├── scraper.py │ ├── storage.py │ ├── notifier.py │ ├── models.py │ ├── cache.py │ ├── decorators.py │ ├── factory.py │ ├── sqlite_storage.py └── data/ ├── products.json └── images/ └── requirements.txt


## Setup

### Prerequisites

- Python 3.7+
- Redis (if using Redis for caching)

### Installation

1. **Clone the repository**:
   ```sh
   git clone <repository_url>
   cd Inventory_Scraper

2. **Create a virtual environment**:

    ```sh
    python -m venv venv

3. **Activate the virtual environment**:

    *On Windows*:
    venv\Scripts\activate

    *On macOS/Linux*:
    ```sh
    source venv/bin/activate

4. **Install dependencies**:

    pip install -r requirements.txt

5. **Set the environment variable for the API token**:

    In Terminal:
    export API_TOKEN=your_static_token  # On macOS/Linux
    set API_TOKEN=your_static_token  # On Windows

### Running the Application
    Use uvicorn to run the FastAPI application:

    uvicorn main:app --reload

    The application will be available at http://127.0.0.1:8000.

## Usage

    Scraping Endpoint
    The /scrape endpoint allows you to scrape product information from the target website.

    Request
    Method: GET
    URL: http://127.0.0.1:8000/scrape
    Query Parameters:
    maxPages (int): The maximum number of pages to scrape (default: 5).
    proxy (str): The proxy string to use for scraping (optional).
    Headers:
    Authorization: Bearer <your_static_token>
    Example
    Using curl:

    curl -X GET "http://127.0.0.1:8000/scrape?maxPages=5&proxy=" -H "Authorization: Bearer your_static_token"

    Response
    The response will include the scraped product information and the total number of products scraped.

    {
    "products": [
        {
        "product_title": "Product 1",
        "product_price": 100.0,
        "path_to_image": "data/images/Product 1.jpg"
        },
        {
        "product_title": "Product 2",
        "product_price": 200.0,
        "path_to_image": "data/images/Product 2.jpg"
        }
    ],
    "total_scraped": 2
    }

## Customization
    Storage Strategy
    You can switch between different storage strategies (JSON or SQLite) by modifying the main.py file.

    # choose the storage strategy
    1. Factory.create_json_storage(file_path="scraper/data/products.json", cache_strategy=cache_strategy)

    2. Factory.create_sqlite_storage("data/products.db", cache_strategy)

    Caching Strategy
    You can switch between different caching strategies (Redis or in-memory) by modifying the main.py file.

    # Choose the cache strategy
    1. Factory.create_redis_cache()
    2. Factory.create_in_memory_cache()

    Notification Strategy
    You can switch between different notification strategies (console, email, or file) by modifying the main.py file.

    # Choose the notification strategy
    1. Factory.create_console_notifier()
    2. Factory.create_file_notifier("data/notifications.log")

## Contributing
    Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
    This project is licensed under the MIT License. See the LICENSE file for details.


### Summary

    This `README.md` file provides a comprehensive overview of the project, including setup instructions, usage examples, and customization options. It helps users understand how to install, run, and use the application, as well as how to switch between different storage, caching, and notification strategies.