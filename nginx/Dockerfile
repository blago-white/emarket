FROM nginx

RUN mkdir /emarket-statics/
RUN mkdir /emarket-statics/static
RUN mkdir /emarket-statics/uploads

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/
