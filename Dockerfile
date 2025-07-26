# Gunakan base image yang mendukung Selenium + Chrome
FROM python:3.10-slim

# Install dependencies untuk Chrome & SeleniumBase
RUN apt-get update && apt-get install -y \
    curl unzip wget gnupg2 fonts-liberation libappindicator3-1 \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    xdg-utils libu2f-udev libvulkan1 \
    chromium chromium-driver \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set Chrome & Chromedriver path untuk SeleniumBase
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file
COPY . .

# Pastikan startup.sh bisa dieksekusi
RUN chmod +x startup.sh

# Expose port Flask
EXPOSE 5000

# Jalankan startup.sh
CMD ["./startup.sh"]
