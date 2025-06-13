# Step 1 :
FROM node:20.19.1

# Step 2:
WORKDIR /USR/SRC/APP

# Step 3:
COPY package*.json .
RUN npm install

COPY . .

# Step 5:
EXPOSE 3000

# Step 6:
CMD ["node", "app.js"]