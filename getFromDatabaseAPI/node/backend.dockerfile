FROM node:lts-alpine 

COPY . /app

WORKDIR /app

RUN npm ci 

ENTRYPOINT [ "npm","run", "start" ]