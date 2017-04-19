FROM nginx:1.10.3
RUN rm /etc/nginx/nginx.conf
ADD nginx.conf /etc/nginx/.

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
