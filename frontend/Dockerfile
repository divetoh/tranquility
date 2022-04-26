FROM node:16 as build-stage

WORKDIR /app

COPY package*.json /app/
RUN npm install

ARG VUE_APP_DOMAIN
ENV VUE_APP_DOMAIN=$VUE_APP_DOMAIN

ARG VUE_APP_DEMOMODE
ENV VUE_APP_DEMOMODE=$VUE_APP_DEMOMODE

COPY ./ /app/
RUN npm run build

FROM nginx:1.21 as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
