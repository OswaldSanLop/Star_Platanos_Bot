# Este archivo le dice a Docker cómo construir tu ambiente

# 1. Usa una imagen base oficial de Python (ligera)
FROM python:3.10-slim

# 2. Establece el directorio de trabajo dentro del contenedor (el equivalente a /app)
WORKDIR /app

# 3. Copia el archivo de requerimientos
COPY requirements.txt .

# 4. Instala las dependencias (por ahora, ninguna)
RUN pip install -r requirements.txt

# 5. Copia el resto de tu código (.py) al contenedor
COPY . .

# 6. Define el comando que se ejecutará (¡el punto de entrada!)
CMD ["python", "star_platanos.py"]