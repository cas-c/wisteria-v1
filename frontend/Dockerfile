FROM node:20-slim

WORKDIR /app

# Install deps first (layer caching — same idea as the Python Dockerfile)
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Next.js dev server with hot reload
CMD ["npm", "run", "dev"]
