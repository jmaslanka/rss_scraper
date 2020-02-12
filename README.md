# Rss_scraper
Scraping exchange rates from ECB

## Technologies:
- Django 2.2
- Python 3.8
- Django REST Framework 3.10
- Celery + RabbitMQ
 
## Requirements
- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Commands
To run the project:
```
git clone git@github.com:jmaslanka/rss_scraper.git
cd rss_scraper
cp .env.example .env
docker-compose build
docker-compose up
```
