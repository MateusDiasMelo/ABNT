FROM node:18-alpine

WORKDIR /app

# Copia package files
COPY package*.json ./

# Instala dependências
RUN npm install

# Copia código
COPY . .

# Expõe porta
EXPOSE 5173

# Comando padrão
CMD ["npm", "run", "dev", "--", "--host"]
