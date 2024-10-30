FROM node:18

WORKDIR /home/node/app

COPY package.json yarn.lock ./

RUN yarn cache clean && \
    yarn install --frozen-lockfile

COPY . /home/node/app
