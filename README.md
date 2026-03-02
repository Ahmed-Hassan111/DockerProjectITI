# 🐳 Dockerized Data Analytics Pipeline

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A containerized Python data analytics application that fetches user data, performs cleaning ETL, and generates visualization insights. Built with Docker for portability and reproducibility.

## 🚀 Features
- **Automated Data Fetching:** Retrieves user data from public API.
- **Data Cleaning:** Handles missing values, drops sensitive columns, and normalizes formats.
- **Visualization:** Generates statistical plots (Age, Gender, Height/Weight correlations).
- **Containerized:** Runs in an isolated Docker environment for consistency.

## 🛠 Tech Stack
- **Language:** Python 3.10
- **Containerization:** Docker (Slim Image)
- **Libraries:** Pandas, Matplotlib, Seaborn, Requests
- **OS:** Linux (Ubuntu)

## 📂 Project Structure
.
├── Dockerfile           # Container build instructions
├── app.py               # Main analytics script
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation


## 🐳 Docker Configuration

### ▶️ Build the Image
docker build -t pydata-analytics:1.0 .

### ▶️ Run the Container
docker run -itd --name containerName pydata:1.0 sh
python app.py

📊 **Expected Output**
After running the container, the output/ directory will contain:
    cleaned_users.csv - Processed dataset
    images as visualization of each insight

✅ **Best Practices Applied**
    Lightweight Image: Uses python:3.10-slim to reduce size (~345MB).
    Layer Caching: Copies requirements.txt before code for faster builds.
    No Cache: pip install --no-cache-dir reduces image bloat.
    Environment Variables: Uses MPLBACKEND=Agg for headless plotting.

🧑‍💻 Author
Ahmed
Junior Data Engineer
