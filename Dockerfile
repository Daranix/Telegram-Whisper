FROM python:3.9-slim
ADD ./bot.py /app/bot.py
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update && apt-upgrade -y && apt-get install git 
RUN pip install --upgrade pip
RUN pip install --upgrade "jax[cpu]"
RUN pip install -r requirements.txt
CMD python bot.py