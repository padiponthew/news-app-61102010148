from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"

OPEN_WEATHER_KEY = '67c6bb5bee400575c729a4abea0512a5'

NEWS_API_URL = 'https://newsapi.org/v2/everything?q={0}&apiKey={1}'

NEWS_API_KEY = '6d6cb8604acf448dbc7cf966a6983ba2'

@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    
    weather = get_weather(city, OPEN_WEATHER_KEY)
    news = 'covid'
    news = get_news(news, NEWS_API_KEY)
    return render_template("home.html", weather=weather, news=news)


def get_weather(city,API_KEY):
    try:
        query = quote(city)
        url = OPEN_WEATHER_URL.format(query, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        weather = None

        if parsed.get('weather'):
    
            description = parsed['weather'][0]['description']
            temperature = parsed['main']['temp']
        
            icon =  parsed['weather'][0]['icon']
            url_icon = f"http://openweathermap.org/img/wn/{icon}@2x.png"

            city = parsed['name']
            country = parsed['sys']['country']

            weather = {'description': description,
                    'temperature': temperature,
                    'city': city,
                    'country': country,
                    'url_icon': url_icon,
                    }
        return weather

    except:
        weather = {'description': "city not found",
                    }
    return weather

@app.route('/Cnews')
def Cnews():
    news = request.args.get('news')
    if not news:
        news = 'covid'
    
    news = get_news(news, NEWS_API_KEY)

    return render_template("Cnews.html", news=news)

def get_news(news,API_KEY):
    try:
        query = quote(news)
        url = NEWS_API_URL.format(query, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        news = None

        if parsed.get('articles'):
            countNews = len(parsed['articles'])

            titleList = []
            descriptionList = []
            urlList = []
            urlToImageList = []
            for i in range(countNews):
                title = parsed['articles'][i]['title']
                titleList.append(title)

                description = parsed['articles'][i]['description']
                descriptionList.append(description)

                url = parsed['articles'][i]['url']
                urlList.append(url)

                urlToImage = parsed['articles'][i]['urlToImage']
                urlToImageList.append(urlToImage)

            news = {'countNews': countNews,
                    'titleList': titleList,
                    'descriptionList': descriptionList,
                    'urlList': urlList,
                    'urlToImageList': urlToImageList,
                    }
        return news
    except:
        news = None
        return news

