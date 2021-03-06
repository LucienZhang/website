FROM node:13 as builder
WORKDIR /app
COPY . .
RUN yarn install && yarn build

FROM nginx
RUN mkdir -p /data/app_static/home && \
    rm /etc/nginx/nginx.conf
COPY --from=builder /app/docs/.vuepress/dist /data/app_static/home

EXPOSE 80
VOLUME [ "/etc/nginx/nginx.conf" ]
CMD ["nginx", "-g", "daemon off;"]
