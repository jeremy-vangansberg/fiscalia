import asyncio
import logging
from src.data_extraction.web_scraper import WebScraper
from src.config.settings import settings

# Configuration du logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

async def main():
    """Script principal pour le scraping des données"""
    try:
        scraper = WebScraper()
        await scraper.scrape_data()
    except Exception as e:
        logger.error(f"Erreur lors du scraping: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 