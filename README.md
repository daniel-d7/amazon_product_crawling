# Amazon Product Crawling

This project is an automated crawler for extracting product information from Amazon websites for different countries and zip codes. It uses Selenium for browser automation and supports checkpointing and Google Sheets integration.

## Features
- Crawl Amazon product data for multiple countries and zip codes
- Uses Selenium WebDriver with Chrome in headless mode
- Checkpointing to resume progress after interruption
- Multi-threaded crawling for efficiency
- Push results to Google Sheets

## Requirements
- Python 3.8+
- Google Service Account credentials (for Google Sheets integration)
- Chrome browser installed

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Prepare your input files in the `raw_input/` directory:
	- `zip_code.csv`: List of zip codes and countries to crawl
	- `asin_input.csv` or `asin.csv`: List of ASINs to process
2. (Optional) Set up your Google Service Account for `gspread` and share your target Google Sheet with the service account email.
3. Run the crawler:
```bash
python main.py
```
The crawler will log progress to `crawler.log` and checkpoint to `checkpoint.db`.

## File Structure
```
amazon_product_crawling/
├── main.py                  # Main entry point
├── modules/                 # Core modules
│   ├── crawl_for_zip.py     # Crawling logic per zip code
│   ├── set_zip_code.py      # Set zip code in browser
│   ├── init_checkpoint_db.py# Initialize checkpoint DB
│   ├── load_checkpoint.py   # Load checkpoint
│   ├── save_checkpoint.py   # Save checkpoint
│   ├── push_to_gsheet.py    # Push results to Google Sheets
│   └── __init__.py
├── raw_input/               # Input data
│   ├── zip_code.csv         # Zip codes and countries
│   ├── asin_input.csv       # ASINs to crawl
│   ├── asin.csv             # (Optional) More ASINs
│   └── input.xlsx           # (Optional) Excel input
├── checkpoint.db            # Checkpoint database (auto-generated)
├── crawler.log              # Log file (auto-generated)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Notes
- Make sure Chrome is installed and compatible with `webdriver-manager`.
- For Google Sheets, place your service account JSON in the project root or configure `gspread` accordingly.
- Checkpoints allow safe resumption after interruption; delete `checkpoint.db` to restart from scratch.