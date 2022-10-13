FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx-setup.conf /etc/nginx/conf.d

CMD [ "nginx", "-g", "daemon off;" ]