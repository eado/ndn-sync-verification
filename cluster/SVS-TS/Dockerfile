FROM node:23

WORKDIR /app

COPY . . 

RUN npm i && npm run build

ENV NDNTS_UPLINK=tcp://192.168.2.2:6363
