FROM nginx:latest
RUN rm /etc/nginx/nginx.conf
ADD nginx.conf /etc/nginx/.

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
