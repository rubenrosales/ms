# Base image
FROM node:16

# Set working directory
WORKDIR /app

# Install app dependencies
COPY package*.json ./
RUN npm install
# Copy app source code
COPY . .

# Build the app
RUN npm run build

# Expose port 3000 for the app
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
