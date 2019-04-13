FROM python:3

RUN mkdir -p /opt/weather_bot
WORKDIR /opt/weather_bot

COPY . /opt/weather_bot/

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]