from scraping.comic_scraping_title import scraping_title_komiku
from scraping.comic_scraping_image import scraping_image_komiku
from scraping.novel_scraping_title import scraping_title_bacalightnovel
from scraping.novel_scraping_content import scraping_content_bacalightnovel

scrapers = {
    "Komik": {
        "Title (Komikindo)": scraping_title_komiku.run_gui,
        "Image (Komiku)": scraping_image_komiku.run_gui,
    },
    "Novel": {
        "Title (Light Novel)": scraping_title_bacalightnovel.run_gui,
        "Content (Wuxia)": scraping_content_bacalightnovel.run_gui,
    }
}
