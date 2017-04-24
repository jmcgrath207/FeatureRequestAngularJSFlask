FROM nginx:1.10.3
RUN rm /etc/nginx/nginx.conf
ADD nginx.conf /etc/nginx/.

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# all logs default to /dev/stdout for docker nginx
#docker logs --tail 50 --follow --timestamps featurerequestpythonflask_nginx_1
#https://blog.docker.com/2015/04/tips-for-deploying-nginx-official-image-with-docker/