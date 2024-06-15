# Web-scraper that bypasses Cloudflare

This scraper is used to extract data from 538 URLs on a research platform called CABI Digital Library. The website uses anti-bot mechanism and services such as cloudflare to obstruct we data extractors from saving the world.

This scraper was bot with interactions, like mouse movements, scrolling, etc in order to mimick a human. It was also built with the ability to change useragent for every requests in order to mask as another user.

Without this scraper



With this scraper



#### SETUP
- Install python
- Open your terminal and navigate to the root directory of this project
- Create your virtual environment
```python
python -m venv venv
```
- Activate your virtual environment (windows only)
```python
venv/source/activate
```
- Install necessary packages
```python
pip install -r requirements.txt
```
- Run the script
```python
python main.py
```