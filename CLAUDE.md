# CLAUDE.md - Agent Network Expander Template

## Project Overview

The Agent Network Expander Template is a specialized tool for analyzing and expanding multi-agent AI systems by identifying gaps and suggesting complementary orchestration and action agents through an iterative, interactive approval workflow.

## Purpose

This repository provides tooling to:
- Review existing multi-agent network configurations
- Intelligently suggest additional agents to enhance coordination, coverage, and capability
- Generate system prompts for recommended agents
- Map agent relationships and identify functional gaps
- Optimize multi-agent system architecture

## Repository Structure

```
.
├── slash-commands/          # Claude Code slash command definitions
│   ├── review-agent-network-iterative.md  # Interactive review mode
│   └── review-agent-network.md            # Batch analysis mode
├── scripts/                 # Python analysis scripts
│   ├── analyze_network_iterative.py       # Local iterative analyzer
│   └── analyze_network_local.py           # Local batch analyzer
├── findings/                # Generated analysis outputs (created during use)
│   ├── analysis-summary.md
│   ├── agent-network-analysis.md
│   └── system-prompts/
│       ├── orchestration/
│       └── action/
├── MODE_COMPARISON.md       # Detailed comparison of operating modes
├── USAGE_ITERATIVE.md       # Iterative mode usage guide
├── USAGE.md                 # General usage documentation
└── requirements.txt         # Python dependencies
```

## Operating Modes

### 1. Iterative Mode (Recommended)
- Suggests agents one at a time
- Allows individual approval/rejection of each suggestion
- Generates system prompts immediately for accepted agents
- Creates a summary of all decisions
- Best for interactive development and selective agent addition

### 2. Batch Mode
- Analyzes entire network and generates all suggestions at once
- Lists all recommendations in a single document
- Optionally generates all system prompts in bulk
- Best for comprehensive planning sessions and documentation

## Two Agent Layers

1. **Orchestration & Routing Layer**: Agents that coordinate workflows, manage priorities, route tasks, and handle system-level concerns
2. **Action Layer**: Specialized agents that perform specific tasks and operations

## Technology Stack

- **Language**: Python 3.8+
- **LLM Backend**:
  - Cloud: Anthropic Claude (via Claude Code CLI)
  - Local: Ollama (recommended model: qwen2.5:14b-instruct-q5_K_M)
- **Dependencies**: See requirements.txt

## Usage Patterns

### As Claude Code Slash Commands
Copy the slash command files from `slash-commands/` to your `.claude/commands/` directory:
- `/review-agent-network-iterative` for interactive mode
- `/review-agent-network` for batch mode

### As Standalone CLI Tool
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/analyze_network_iterative.py /path/to/agent/config
```

### Integration Options
- Standalone CLI tool for batch processing
- GitHub Action for periodic reviews
- Local development tool in ~/programs/
- Part of agent development workflow
- CI/CD pipeline integration

## Working with This Repository

### Development
When making changes to this repository:
- Test both iterative and batch modes
- Ensure slash commands remain compatible with Claude Code
- Update documentation when adding new features
- Consider backwards compatibility for existing users

### Testing
- Test with sample agent network configurations
- Verify both cloud (Claude) and local (Ollama) modes work correctly
- Test generated system prompts for quality and completeness

### Output Locations
The `findings/` directory is created during analysis runs and contains:
- Analysis summaries
- Agent network analysis documents
- Generated system prompts organized by layer (orchestration/action)

## Use Cases

- **Initial Architecture Design**: Identify required agents before building
- **System Expansion**: Find gaps in existing agent networks
- **Optimization**: Discover redundancies and missing coordination
- **Documentation**: Generate comprehensive agent network maps
- **Team Onboarding**: Help developers understand agent architecture
- **Architecture Health Checks**: Periodic reviews of agent system design

## Key Features

- Intelligent gap analysis of multi-agent systems
- Iterative approval workflow for selective agent addition
- Automatic system prompt generation
- Support for both cloud and local LLM backends
- Flexible deployment as slash command or CLI tool
- Separation of orchestration and action agent layers

## AI Assistant Guidelines

When working with this repository:

1. **Understanding Context**: This is a meta-tool for AI agent systems - it helps design and expand networks of AI agents
2. **Analysis Focus**: The core value is in intelligent gap identification and complementary agent suggestion
3. **Workflow Modes**: Respect the two distinct modes (iterative vs batch) and their different use cases
4. **System Prompts**: Generated system prompts should be high-quality and implementation-ready
5. **Documentation**: Keep usage guides synchronized with code functionality
6. **Testing**: Always test with realistic agent network scenarios

## Extension Points

This template is designed to be extended with:
- Additional analysis heuristics
- Support for different agent frameworks
- Alternative LLM backends
- Visualization tools
- Integration with agent orchestration platforms
- Custom agent suggestion strategies
- Domain-specific agent templates

## Related Concepts

- Multi-agent systems architecture
- Agent orchestration patterns
- Workflow coordination
- Task routing and delegation
- Agent capability mapping
- System architecture analysis
