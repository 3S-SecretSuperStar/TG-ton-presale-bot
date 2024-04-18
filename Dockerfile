FROM python:3.12

ARG DEBIAN_FRONTEND=noninteractive

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

# Set display port to avoid crash
ENV DISPLAY=:99

# Set the working directory in the container
WORKDIR /app

# Copy the Python code into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir psycopg2-binary selenium webdriver_manager schedule python-dotenv

# Run the Python script
CMD ["python", "app.py"]


# Use the official Python image as base image
# FROM python:3.12

# ARG DEBIAN_FRONTEND=noninteractive


# # COPY requirements.txt requirements.txt

# RUN apt-get update && apt-get install -y wget curl gnupg
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# RUN apt-get update && apt-get install -y google-chrome-stable

# # set display port to avoid crash

# ENV DISPLAY=:99

# # Set the working directory in the container
# WORKDIR /app

# # Copy the Python code into the container
# COPY . .

# # Install dependencies
# RUN  pip install --upgrade pip

# RUN pip install --no-cache-dir psycopg2-binary selenium webdriver_manager schedule python-dotenv

# #RUN pip install --no-cache-dir -r requirements.txt

# # # Set environment variables
# # ENV DB_HOST=localhost \
# #     DB_DATABASE=presalebot \
# #     DB_USER=postgres \
# #     DB_PASSWORD=presalebot \

# # Expose the port if needed
# # EXPOSE 8080

# # Run the Python script
# CMD ["python", "app.py"]
