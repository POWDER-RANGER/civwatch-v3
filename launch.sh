#!/bin/bash
set -e

echo "🚀 CivWatch v3.0 - Unified RF Observability Platform"
echo "================================================"

# Install dependencies
echo "📦 Installing requirements..."
pip install -r requirements.txt --quiet

# Start database
echo "🗄️  Starting Postgres..."
echo "Using SQLite fallback for seamless demo (Postgres optional)"

# Wait for DB
echo "⏳ Waiting for database..."
sleep 8

# Initialize DB if needed
echo "🛠️  Ensuring database schema..."
python -c '
from storage.database import init_db
init_db()
' 2>/dev/null || echo "Database init skipped (will run on first start)"

# Launch the app
echo "🌐 Starting FastAPI server..."
echo "📍 Dashboard available at http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload