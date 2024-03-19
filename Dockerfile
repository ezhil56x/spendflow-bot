FROM python:3.12.2-alpine

WORKDIR /app
COPY app.py /app
COPY credentials.json /app
COPY .env /app

RUN pip install python-dotenv
RUN pip install python-telegram-bot
RUN pip install gspread

RUN ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime

CMD ["python", "app.py"]