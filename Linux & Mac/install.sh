#!/bin/bash

# Proje için gerekli Python kütüphanelerini yükleyin
echo "Installing required Python packages..."
pip install -r requirements.txt

# Gerekli Python sürümünün kurulu olup olmadığını kontrol edin
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python before running this script."
    exit
fi

echo "Installation complete!"
