# Step 1 :
FROM node:20.19.1

# Step 2:
WORKDIR /USR/SRC/APP

# Step 3:
COPY package*.json .
RUN npm install

RUN npm install -g pm2

COPY . .

# Step 5:
EXPOSE 3000

# Step 6:
CMD ["pm2-runtime", "app.js"]