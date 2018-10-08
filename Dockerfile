FROM python:2.7.15-stretch
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./webpage webpage
CMD ["python", "webpage/app.py"]
