## **Django-Youtube**

An app to fetch the latest videos from Youtube, powered by Django, Celery and Redis.

### **How To Run**

**1. Clone the repo**

`git clone https://github.com/CyberDrudge/django_youtube.git`

**2. Install redis.**

`sudo apt-get install redis-server`

**3. Install requirements.**

`pip install -r requirements.txt`

**4. Load API Keys.**

`python manage.py loaddata --app keys keys/fixtures/keys.json`

PS: Loaded keys work as of now but might not work in the future. Please add your own keys for uninterrupted usage.
Follow https://developers.google.com/youtube/v3/getting-started to generate your own key and add it in ApiKey database.

**5. Run Servers (On separate terminals)**

`python manage.py runserver`

`celery -A django_youtube worker -l info`

`celery -A django_youtube beat -l info`


### **APIs Usage**

**1. List API**

Url: `http://localhost:8000/videos/`

**2. Search API**

Url: `http://localhost:8000/videos/search?query=<query>`

Params: `query`

Sample Url: `http://localhost:8000/videos/search?query=India`
