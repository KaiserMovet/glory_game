# syntax=docker/dockerfile:1

FROM 3.11.1-bullseye

WORKDIR /app

COPY req.txt req.txt
RUN pip3 install -r req.txt

COPY . .

CMD [ "python3", "main.py"]