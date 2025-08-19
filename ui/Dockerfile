# Dockerfile v0.1.0
FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --production
COPY . .
CMD ["npm", "run", "dev"]
