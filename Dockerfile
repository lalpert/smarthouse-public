FROM python:3.7-stretch
# Set the timezone
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./webpage webpage
CMD ["python", "webpage/app.py"]
