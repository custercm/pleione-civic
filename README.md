# Pleione Civic AI Assistant

Pleione is a minimal, self-upgrading AI assistant that safely generates code in sandboxed directories before merging to production. It integrates with LM Studio for local AI inference.

## Features

- 🤖 Local AI integration via LM Studio (port 1234)
- 🛡️ Sandboxed code generation for safety
- 🧪 Automated testing framework
- 🌐 Web-based chat interface with auto-implement buttons
- 🔄 Self-upgrading capabilities
- ⚡ One-click code implementation
- 🚀 Fully automated: Generate → Test → Implement
- 🛡️ **Safe Self-Modification**: Pleione can update herself safely with comprehensive testing

## Requirements

- **Python 3.10+**
- **LM Studio** running on localhost:1234 with a loaded model
- **FastAPI** and dependencies (auto-installed)

## Quick Start

### 1. Install Dependencies
```bash
./setup.sh
```

### 2. Start LM Studio
- Download and install [LM Studio](https://lmstudio.ai/)
- Load your preferred model
- Start the local server on port 1234 (default)

### 3. Run Pleione
```bash
./run.sh
```

### 4. Access Web Interface
Open your browser to: `http://localhost:8000/frontend/index.html`

### 5. Try the Demo
Run the demo to see how auto-implementation works:
```bash
./demo.sh
```

## How Auto-Implementation Works

1. **Generate Code**: Ask Pleione via chat to create a feature
2. **Automatic Testing**: Pleione creates the code AND tests, then runs them
3. **One-Click Implementation**: If tests pass, click "🚀 Auto-Implement Code"
4. **Manual Review Option**: Or click "👀 Review Code First" to check before implementing

### Shell Commands
```bash
# Auto-implement any code in sandbox (with git backup)
./implement.sh

# Git-based safe self-update management
./safe-update.sh

# Run a demonstration
./demo.sh

# Manual git operations
git log --oneline          # See all commits
git reset --hard HEAD~1    # Rollback 1 commit
git reset --hard <commit>  # Go to specific commit
```

## 🛡️ Git-Based Safe Self-Modification System

Pleione can safely update her own code using **git for bulletproof backups**:

### **How It Works:**
1. **Auto-Detection**: Frontend detects self-update requests (UI fixes, backend changes)
2. **Git Backup**: Automatically commits current state to git before any changes
3. **Context Loading**: Reads relevant files (HTML, JS, Python) for smart updates
4. **Staging Environment**: Creates isolated copy with proposed changes
5. **Comprehensive Testing**: Runs all tests + API tests + integration tests
6. **Git Commits**: All changes tracked and committed to git history
7. **Easy Rollback**: One-command rollback to any previous commit

### **Safety Features:**
- ✅ **Git Version Control**: Every change is tracked and recoverable
- ✅ **Comprehensive Testing**: API, integration, and unit tests
- ✅ **Automatic Git Backups**: Every update creates git commit
- ✅ **One-Command Rollback**: `git reset --hard HEAD~1` to undo
- ✅ **Complete History**: See exactly what changed and when
- ✅ **No File Loss**: Git prevents accidental deletion or corruption
- ✅ **Manual Approval**: Final deployment requires confirmation

### **Self-Update Example:**
```
You: "Fix the UI button alignment and make them blue"
Pleione: 🛡️ Self-update detected! 
         💾 Creating git backup...
         📖 Reading current frontend files...
         🏗️ Creating staging environment...
         🧪 Running comprehensive tests...
         ✅ All tests passed!
         📦 Safe update package ready
         💡 Rollback with: git reset --hard abc123f
```

## Project Structure

```
pleione-civic/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_runner.py       # Test execution engine
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── models/
│   │   └── llm_connector.py # LM Studio integration
│   ├── sandbox/             # Generated code (safe zone)
│   └── tests/              # Automated tests
├── frontend/
│   ├── index.html          # Web chat interface
│   └── chat.js             # Frontend JavaScript
├── setup.sh               # Initial setup script
├── run.sh                 # Start the application
├── stop.sh                # Stop all processes
├── upgrade.sh             # Self-upgrade process
└── requirements.txt       # Python dependencies
```

## API Endpoints

- `POST /api/chat` - Send prompts to AI assistant
- `GET /` - API information
- `GET /frontend/` - Static web interface

## Usage Examples

1. **Generate a new feature:**
   ```
   "Create a function to calculate fibonacci numbers with tests"
   ```

2. **Fix a bug:**
   ```
   "Fix the bug in the user authentication module"
   ```

3. **Add tests:**
   ```
   "Write comprehensive tests for the payment processing function"
   ```

## Safety Features

- All generated code is placed in `backend/sandbox/` for review
- Automated testing before any code integration
- Manual approval required for merging to production
- Isolated execution environment

## Configuration

### LM Studio Settings
- **URL:** `http://localhost:1234/v1/chat/completions`
- **Model:** Uses whatever model is currently loaded
- **Temperature:** 0.7 (adjustable in `llm_connector.py`)

### Port Configuration
- **Backend API:** 8000
- **LM Studio:** 1234
- **Frontend:** Served via backend

## Troubleshooting

### "Cannot connect to LM Studio"
- Ensure LM Studio is running
- Verify a model is loaded and server is started
- Check that port 1234 is not blocked

### "Module not found" errors
- Run `./setup.sh` to install dependencies
- Ensure Python 3.10+ is installed

### Frontend not loading
- Verify backend is running on port 8000
- Check browser console for errors
- Try accessing `http://localhost:8000/frontend/index.html` directly

## Development

### Running Tests
```bash
python backend/test_runner.py
```

### Manual Testing
```bash
# Start in development mode with auto-reload
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Adding Features
1. Generate code via chat interface
2. Review generated code in `backend/sandbox/`
3. Run tests to verify functionality
4. Manually merge to production code

## Contributing

Pleione is designed to be self-improving. Use the chat interface to request new features or bug fixes, review the generated code, and merge approved changes.

## License

MIT License - Feel free to modify and distribute.
