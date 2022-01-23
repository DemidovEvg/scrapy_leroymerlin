# 1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
# ● название;
# ● все фото;
# ● ссылка;
# ● цена.

# Реализуйте очистку и преобразование данных с помощью ItemLoader. 
# Цены должны быть в виде числового значения.

# Дополнительно:
# 2)Написать универсальный обработчик характеристик товаров, 
# который будет формировать данные вне зависимости от их типа и количества.

# 3)Реализовать хранение скачиваемых файлов в отдельных папках, 
# каждая из которых должна соответствовать собираемому товару

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlin_project.spiders.leroymerlin import leroymerlinSpider
from leroymerlin_project import settings

if __name__ == "__main__":
    source = leroymerlinSpider
    # ================================================
    # Выбор подпутей по которым будет собирать данные
    # ================================================
    url_sub_paths = ['lenty-svetodiodnye/?00320=0.5',
                    'modulnye-svetilniki/',
                    'fonari-nalobnye-i-ruchnye/?22088=Карманный+фонарик',
                    ]
    # ================================================
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(source, url_sub_paths=url_sub_paths)
    process.start()