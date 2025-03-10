FROM golang:1.23

WORKDIR /app
COPY . . 

RUN go mod init example.com/main && go mod tidy && go build
