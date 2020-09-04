FROM python:3.7.4

WORKDIR /app
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "-u", "run.py"]