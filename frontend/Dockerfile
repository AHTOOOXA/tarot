FROM node:18

WORKDIR /home/node/app

COPY package.json yarn.lock ./

RUN yarn install

COPY . /home/node/app