# Use Python 3.12 slim
FROM python:3.12.1-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY app.py app.py
COPY rag.py rag.py
COPY db.py db.py
COPY data.csv data.csv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    matplotlib \
    openai \
    minsearch

# Expose Streamlit port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]