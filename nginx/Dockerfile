FROM nginx

RUN mkdir /emarket-statics/ && mkdir /emarket-statics/static && mkdir /emarket-statics/uploads
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
