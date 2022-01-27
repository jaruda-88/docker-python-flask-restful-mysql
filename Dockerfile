FROM python:3.9.5

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app

EXPOSE 5040

ENTRYPOINT ["python3"]

CMD ["app.py"]