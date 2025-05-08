#!/bin/bash

echo "🧹 Eliminando entorno virtual anterior..."
rm -rf venv

echo "🐍 Creando nuevo entorno virtual..."
python3 -m venv venv

echo "✅ Activando entorno virtual..."
source venv/bin/activate

echo "⬆️  Actualizando pip..."
pip install --upgrade pip

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Entorno listo. Para usarlo:"

echo "source venv/bin/activate"
