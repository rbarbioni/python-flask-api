FROM python:3.6-slim

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install pipenv

ADD Pipfile* ./
RUN pipenv install --system --skip-lock

ADD . .

EXPOSE 5000

CMD [ "python", "main.py" ]