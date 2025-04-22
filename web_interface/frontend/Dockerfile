# Etapa 1: build com node slim
FROM node:18-slim AS build

WORKDIR /app
COPY . .

# Garante instalação limpa e compatível
RUN rm -rf node_modules package-lock.json
RUN npm install
RUN npm run build

# Etapa 2: nginx para servir build
FROM nginx:1.25-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
