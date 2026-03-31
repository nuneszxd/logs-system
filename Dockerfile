FROM python:3.11

WORKDIR /app

ENV TZ=America/Sao_Paulo

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "-u", "-m", "app.routes" ]