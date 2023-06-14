FROM python:latest

ADD main.py .

RUN pip install python-telegram-bot
RUN pip install currencyapicom
RUN pip install python-telegram-bot[job-queue]

EXPOSE 443 # 80 88

CMD ["python", "./main.py"]
