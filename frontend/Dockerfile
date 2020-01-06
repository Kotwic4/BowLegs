# build environment
FROM node:12.2.0-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
RUN npm install --silent
RUN npm install react-scripts@3.0.1 -g --silent
COPY src /app/src
COPY public /app/public
RUN npm run build

# production environment
FROM nginx:1.16.0-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/my.template
EXPOSE 80
CMD envsubst '$API_URL' < /etc/nginx/conf.d/my.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'
