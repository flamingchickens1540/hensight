# Hensight

Hensight is a display platform used to display FRC team data on a portable screen.

## Usage

```bash
pip install tba-api-v3client flask schedule numpy statbotics tbapy
python main.py
```

### Rust backend

#### Environment variables
Can all be set inline or in the .env
- TEAM_NUMBER, Optional (defaults to 1540)
- EVENT_KEY
- TBA_API_KEY
- NEXUS_API_KEY

```bash
# With EVENT_KEY set in .env
cargo run
# setting EVENT_KEY inline
EVENT_KEY="2024cc" cargo run
```

### Format

```bash
# Frontend
bun i
bun prettier . --write
# Rust Backend
cargo fmt
```
