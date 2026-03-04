# AI Blog Generator

An AI-powered blog generation tool with a backend API and frontend interface.

## Project Structure

```
.
├── backend/          # Flask/FastAPI backend server
├── frontend/         # Frontend application
├── keys/             # Configuration and environment variables
└── requirements.txt  # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI_Blog_Generator
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
   - Copy your configuration to `keys/.env`
   - Add your API keys and settings (see `.env.example` if available)

### Running the Application

#### Backend
```bash
cd backend
python main.py
```

#### Frontend
```bash
cd frontend
python frontend.py
```

## Environment Variables

Create a `keys/.env` file with the following variables:
```
API_KEY=your_api_key_here
DATABASE_URL=your_database_url
DEBUG=False
```

**Note:** Never commit `keys/.env` to version control (already in `.gitignore`).

## Development

The `.gitignore` file excludes:
- `keys/.env` - Environment variables
- `.venv/` - Virtual environment
- `*.pyc` - Python cache files

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
