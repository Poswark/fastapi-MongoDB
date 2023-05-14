FROM python:alpine3.18

RUN mkdir /app
WORKDIR /app
COPY . .

RUN apk add --no-cache gcc musl-dev linux-headers bash curl vim 
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

EXPOSE 5000