FROM node:24-alpine AS builder
WORKDIR /app
COPY package.json ./
RUN npm install
COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
