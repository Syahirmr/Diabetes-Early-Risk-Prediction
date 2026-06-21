# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency definitions
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./frontend/

# Build static assets (Tailwind & Alpine) using Vite
RUN npx vite build frontend

# Stage 2: Production
FROM nginx:alpine

# Copy built assets from builder stage to Nginx web root
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
