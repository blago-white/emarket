FROM python

WORKDIR /app

COPY . .

CMD ["python", "index.py"]
