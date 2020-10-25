FROM nginx
COPY ./nginx.conf /etc/nginx/conf.d/armbook.conf
COPY ./armbook.pem /etc/nginx/
COPY ./armbook.key /etc/nginx/
ADD ./armbook /usr/share/nginx/html/armbook
# why in the actual shit is this needed and why doesn't nginx
# have decent permissions
RUN chmod -R 755 /usr/share/nginx/html/armbook
