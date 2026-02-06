FROM node:25

WORKDIR /app

COPY package* .

RUN npm install

COPY . .

CMD ["node", "index.js"]