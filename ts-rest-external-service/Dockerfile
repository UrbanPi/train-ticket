FROM node

RUN mkdir -p /app
WORKDIR /app

ADD ./node_modules.tar.gz /app/node_modules
ADD ./package.json /app/

ADD ./rest-service-external.js /app/
#RUN npm install
CMD [ "npm", "start" ]

EXPOSE 16100