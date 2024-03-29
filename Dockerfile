FROM python:3.8.5

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y
RUN pip3 install --upgrade pip
RUN pip install flasgger
RUN pip install cryptography
RUN pip install flask_cors
RUN pip install pyjwt
# RUN pip install PyMySQL
# RUN pip install mysql-connector-python
RUN pip install jarudaDB==0.0.3
RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app

EXPOSE 5000

#ENTRYPOINT ["python3"]
#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5040"]
#CMD ["python3", "app.py"]
CMD ["/bin/bash", "run.sh"]