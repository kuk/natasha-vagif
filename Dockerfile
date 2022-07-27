FROM python:3.9.13-slim

RUN pip install --no-cache-dir aiogram==2.21

COPY main.py .
CMD python main.py
