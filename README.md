# Agent Network Expander Template

A tool for analyzing and expanding multi-agent AI systems by identifying gaps and suggesting complementary orchestration and action agents through an **iterative, interactive approval workflow**.

## Overview

This repository provides tooling to review existing multi-agent network configurations and intelligently suggest additional agents to enhance coordination, coverage, and capability.

### Two Operating Modes

1. **Iterative Mode** (Recommended): Suggests agents one at a time, allowing you to approve/reject each suggestion individually
2. **Batch Mode**: Analyzes the entire network and generates all suggestions at once

📊 **See [MODE_COMPARISON.md](MODE_COMPARISON.md) for detailed comparison and recommendations.**

### Two Agent Layers

1. **Orchestration & Routing Layer**: Agents that coordinate workflows, manage priorities, route tasks, and handle system-level concerns
2. **Action Layer**: Specialized agents that perform specific tasks and operations

## What It Does

The Agent Network Expander analyzes your multi-agent system and:
- Maps existing agents and their relationships
- Identifies functional gaps and coordination needs
- Suggests complementary orchestration agents for better workflow management
- Recommends specialized action agents to fill capability gaps
- Generates detailed analysis documents with implementation priorities
- Optionally creates system prompts for recommended agents

## Usage

### Iterative Mode (Recommended)

#### Claude Code (Cloud)

```bash
# In your agent network directory
/review-agent-network-iterative
```

The command will:
1. Analyze your agent configuration
2. Present agent suggestions one at a time
3. Ask for your approval on each suggestion
4. Generate system prompts for accepted agents
5. Create a summary of all decisions

#### Local (Ollama)

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run iterative analysis
python scripts/analyze_network_iterative.py /path/to/agent/config

# Or analyze current directory
python scripts/analyze_network_iterative.py .
```

**Iterative workflow**:
- Review each suggestion individually
- Choose: Yes (add), No (reject), Skip (maybe later), or Quit (stop reviewing)
- System prompts generated immediately for accepted agents
- Summary saved with all decisions

### Batch Mode

#### Claude Code (Cloud)

```bash
/review-agent-network
```

#### Local (Ollama)

```bash
python scripts/analyze_network_local.py /path/to/agent/config
```

**Batch workflow**:
- Generates complete analysis document
- Lists all suggestions at once
- Optionally generates all system prompts in bulk
- Best for comprehensive planning sessions

## Deployment Options

### 1. As a Slash Command in Claude Code
- **Iterative**: Copy `slash-commands/review-agent-network-iterative.md` to `.claude/commands/`
- **Batch**: Copy `slash-commands/review-agent-network.md` to `.claude/commands/`
- Restart or reload Claude Code
- Access via `/review-agent-network-iterative` or `/review-agent-network`

### 2. As a Standalone CLI Tool
- Install the script globally or add to your PATH
- Use as a command-line utility for batch processing multiple agent networks
- Integrate into CI/CD pipelines for continuous agent architecture review

### 3. As a GitHub Action
- Schedule periodic reviews of agent network configurations
- Automatically generate pull requests with suggestions
- Track agent network evolution over time

### 4. As a Local Development Tool
- Keep in your tools directory (`~/programs/agent-network-expander/`)
- Use during agent system design and development
- Run analysis before major architecture changes

### 5. As Part of Agent Development Workflow
- Integrate into agent creation templates
- Run during agent network initialization
- Use for periodic architecture health checks

## Repository Structure

```
.
├── slash-commands/
│   ├── review-agent-network-iterative.md  # Interactive review mode
│   └── review-agent-network.md            # Batch analysis mode
├── scripts/
│   ├── analyze_network_iterative.py       # Local iterative analyzer
│   └── analyze_network_local.py           # Local batch analyzer
├── findings/                              # Generated analysis outputs
│   ├── analysis-summary.md                # Iterative mode summary
│   ├── agent-network-analysis.md          # Batch mode analysis
│   └── system-prompts/
│       ├── orchestration/
│       └── action/
└── requirements.txt                       # Python dependencies
```

## Requirements

### For Claude Code Version
- Claude Code CLI
- Active Anthropic API access

### For Local Version
- Python 3.8+
- Ollama installed and running
- Recommended model: `qwen2.5:14b-instruct-q5_K_M` (or similar 10GB+ model)

## Use Cases

- **Initial Architecture Design**: Identify what agents you need before building
- **System Expansion**: Find gaps in existing agent networks
- **Optimization**: Discover redundancies and missing coordination
- **Documentation**: Generate comprehensive agent network maps
- **Team Onboarding**: Help new developers understand agent architecture

## Contributing

Contributions welcome! This template is designed to be extended with:
- Additional analysis heuristics
- Support for different agent frameworks
- Alternative LLM backends
- Visualization tools
- Integration with agent orchestration platforms

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Author

Created by Daniel Rosehill
- Website: [danielrosehill.com](https://danielrosehill.com)
- Email: public@danielrosehill.com
