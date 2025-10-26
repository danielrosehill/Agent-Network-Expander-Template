# Usage Guide

## Two Modes Available

This tool offers two ways to analyze and expand your agent network:

| Feature | **Iterative Mode** | **Batch Mode** |
|---------|-------------------|----------------|
| **Best for** | Progressive implementation | Comprehensive planning |
| **Workflow** | One suggestion at a time | All suggestions at once |
| **Decision making** | Approve/reject as you go | Review document, then decide |
| **System prompts** | Generated immediately for accepted agents | Optional bulk generation |
| **Control** | Stop anytime | Complete analysis first |
| **Output** | Decisions summary + prompts | Full analysis document |
| **Recommended for** | Most use cases, active development | Planning sessions, documentation |

**Quick recommendation**: Start with **Iterative Mode** for most use cases. Use Batch Mode when you need comprehensive planning documentation.

📖 **Detailed Guide**: See [USAGE_ITERATIVE.md](USAGE_ITERATIVE.md) for a complete walkthrough of iterative mode.

---

## Quick Start

### Iterative Mode (Recommended)

**Using Claude Code:**
```bash
# Copy the command
mkdir -p ~/.claude/commands
cp slash-commands/review-agent-network-iterative.md ~/.claude/commands/

# Run in your agent network directory
/review-agent-network-iterative
```

**Using Local Ollama:**
```bash
# First time setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run analysis
python scripts/analyze_network_iterative.py /path/to/agent/network
```

See [USAGE_ITERATIVE.md](USAGE_ITERATIVE.md) for detailed walkthrough.

### Batch Mode

**Using Claude Code:**
```bash
# Copy the command
mkdir -p ~/.claude/commands
cp slash-commands/review-agent-network.md ~/.claude/commands/

# Run in your agent network directory
/review-agent-network
```

**Using Local Ollama:**
```bash
python scripts/analyze_network_local.py /path/to/agent/network
```

---

## Setup for Local Analysis (Ollama)

### Prerequisites

1. **Install Ollama** (if not already installed):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull the recommended model**:
   ```bash
   ollama pull qwen2.5:14b-instruct-q5_K_M
   ```

3. **Set up Python environment**:
   ```bash
   cd /path/to/agent-network-expander
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Running Local Analysis

**Iterative mode:**
```bash
python scripts/analyze_network_iterative.py /path/to/agent/network
python scripts/analyze_network_iterative.py .  # Current directory
python scripts/analyze_network_iterative.py . --model llama3.1:8b  # Different model
```

**Batch mode:**
```bash
python scripts/analyze_network_local.py /path/to/agent/network
python scripts/analyze_network_local.py . --prompts  # Auto-generate all prompts
```

## What Gets Analyzed

The tools look for:
- `*agent*.json` - JSON agent configurations
- `*agent*.yaml` / `*agent*.yml` - YAML agent configurations
- `*.agent.*` - Files with .agent. in the name
- `*prompt*.md` - Markdown prompt files
- `*system*.md` - System prompt files
- Files in `agents/` directories
- Files in `prompts/` directories
- Files in `.claude/` directories (slash commands, agent configs)

## Output Structure

After analysis, you'll find:

```
findings/
├── agent-network-analysis.md           # Main analysis document
└── system-prompts/                     # Generated system prompts
    ├── orchestration/                  # Coordination agents
    │   ├── task-router.md
    │   ├── priority-manager.md
    │   └── ...
    └── action/                         # Task execution agents
        ├── data-processor.md
        ├── validator.md
        └── ...
```

## Analysis Report Contents

The generated `agent-network-analysis.md` includes:

1. **Executive Summary** - High-level overview
2. **Current Agent Inventory** - What agents exist
3. **Agent Relationship Map** - How agents interact
4. **Recommendations**
   - Orchestration & Routing Agents
   - Action Agents
5. **Implementation Priority** - What to build first
6. **Integration Considerations** - How to implement

## Example Workflow

### Initial Design Phase
```bash
# Create your agent config directory
mkdir my-agent-network
cd my-agent-network

# Add initial agent ideas
echo "# Agent 1: Data Fetcher" > agents/data-fetcher.md

# Analyze to discover gaps
python ../scripts/analyze_network_local.py .

# Review findings
cat findings/agent-network-analysis.md
```

### Expansion Phase
```bash
# You've built some agents, now analyze for gaps
cd my-existing-network
python ~/programs/agent-network-expander/scripts/analyze_network_local.py .

# Generate system prompts for new agents
# (choose option 1 when prompted)
```

### CI/CD Integration
```bash
# Add to your CI pipeline
- name: Analyze Agent Network
  run: |
    pip install -r requirements.txt
    python scripts/analyze_network_local.py . --prompts
    git add findings/
    git commit -m "Update agent network analysis"
```

## Model Selection

### Recommended Models

For **best results** (if you have the VRAM):
```bash
ollama pull qwen2.5:14b-instruct-q5_K_M  # 10GB, excellent reasoning
```

For **balanced performance**:
```bash
ollama pull llama3.1:8b-instruct-q6_K    # 6.6GB, good quality
```

For **quick analysis**:
```bash
ollama pull llama3.2:3b                   # 2GB, fast but simpler
```

For **specialized reasoning**:
```bash
ollama pull deepseek-r1:14b              # 10GB, deep reasoning
```

### Using Different Models

```bash
# Specify model with -m flag
python scripts/analyze_network_local.py . -m llama3.1:8b
python scripts/analyze_network_local.py . -m deepseek-r1:14b
python scripts/analyze_network_local.py . -m qwen2.5:32b
```

## Advanced Usage

### Batch Analysis
```bash
# Analyze multiple agent networks
for dir in ~/projects/*/agents; do
    python scripts/analyze_network_local.py "$dir"
done
```

### Custom Output Location
```bash
# The script creates findings/ in the current working directory
cd /path/to/output
python /path/to/scripts/analyze_network_local.py /path/to/agent/config
```

### Integration with Git
```bash
# Track analysis evolution
git add findings/
git commit -m "Agent network analysis - $(date +%Y-%m-%d)"
git tag "analysis-$(date +%Y%m%d)"
```

## Troubleshooting

### "Cannot connect to Ollama"
```bash
# Start Ollama service
ollama serve

# Or check if already running
ps aux | grep ollama
```

### "Model not found"
```bash
# List available models
ollama list

# Pull missing model
ollama pull qwen2.5:14b-instruct-q5_K_M
```

### "No agent files found"
The analyzer looks for specific patterns. Ensure your agent configs use recognizable naming:
- Include "agent" in filenames: `my-agent.json`
- Use standard extensions: `.json`, `.yaml`, `.md`
- Organize in agent directories: `agents/`, `prompts/`

### Analysis is too generic
Try:
- Use a larger model: `--model qwen2.5:32b`
- Ensure your agent configs have detailed descriptions
- Add more context files to your agent directory

## Tips for Best Results

1. **Document existing agents** - Add clear descriptions to agent configs
2. **Use consistent naming** - Makes discovery more reliable
3. **Include relationship info** - Document how agents interact
4. **Specify capabilities** - Be explicit about what each agent does
5. **Review and iterate** - Run analysis multiple times as you build
6. **Track over time** - Commit analysis reports to see evolution

## Getting Help

- Check the main README.md for overview
- Review example agent configs in `/examples` (if available)
- Open an issue on GitHub for bugs or suggestions
