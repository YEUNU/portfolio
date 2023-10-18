FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/YEUNU/portfolio.git .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "portfolio/manage.py", "runserver", "0.0.0.0:8993"]
