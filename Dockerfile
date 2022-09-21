FROM continuumio/miniconda3:latest
RUN apt update && apt install python3 && apt install ffmpeg && apt install git
RUN pip install git+https://github.com/openai/whisper.git
RUN pip install python-telegram-bot --pre
RUN pip install python-dotenv
ADD ./bot.py /app/bot.py
WORKDIR /app
CMD python bot.py