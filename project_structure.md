# Project Structure

PythonProject/
├── main.py                  # Agent entry point and graph definition
├── agent/
│   ├── __init__.py
│   └── tools.py             # get_n_random_words, translate_words, etc.
├── clanki/                  # Node.js MCP server for Anki
│   ├── src/
│   ├── build/
│   │   └── index.js         # Compiled MCP server
│   └── package.json
├── words/                   # JSON word lists per language + difficulty
│   ├── spanish.json
│   ├── german.json
│   └── ...
├── .env                     # Secret keys (git ignored)
├── .env.example             # Template for .env
├── .gitignore
├── requirements.txt
└── README.md