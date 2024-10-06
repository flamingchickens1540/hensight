# Hensight

Hensight is a display platform used to display FRC team data on a portable screen.

## Usage

### Python backend

```bash
pip install tba-api-v3client flask schedule numpy statbotics tbapy
python main.py
```

### Rust backend

```bash
# with all required env vars set in .env
cargo run
# setting EVENT_KEY inline
EVENT_KEY="2024cc" cargo run
# setting TEAM_NUMBER inline (optional, defaults to 1540)
TEAM_NUMBER="1540" cargo run
```

### Format

```bash
# frontend
bun i
bun prettier . --write
# rust backend
cargo fmt
```
