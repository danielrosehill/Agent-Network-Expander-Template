# Iterative Mode Usage Guide

The iterative mode provides an interactive, one-at-a-time review process for agent suggestions, allowing you to make decisions as you go rather than reviewing everything at once.

## Why Use Iterative Mode?

**Use Iterative Mode when you want to:**
- Make decisions progressively rather than all at once
- Generate system prompts only for agents you actually want
- Stop early if you've found enough suggestions
- Have more control over the expansion process
- Avoid information overload from batch analysis

**Use Batch Mode when you want to:**
- See the complete picture before making decisions
- Do comprehensive planning sessions
- Generate documentation for team review
- Analyze multiple possible directions

## Quick Start

### Claude Code (Cloud)

1. Copy the slash command to your commands directory:
   ```bash
   cp slash-commands/review-agent-network-iterative.md ~/.claude/commands/
   ```

2. Navigate to your agent network directory:
   ```bash
   cd ~/projects/my-agent-network
   ```

3. Run the command:
   ```bash
   /review-agent-network-iterative
   ```

### Local (Ollama)

1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

2. Set up the Python environment (first time only):
   ```bash
   cd /path/to/agent-network-expander
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the analyzer:
   ```bash
   python scripts/analyze_network_iterative.py /path/to/your/agent/network
   ```

## Workflow Walkthrough

### Phase 1: Discovery & Analysis

The tool automatically:
1. Searches for agent configuration files
2. Analyzes existing agents
3. Identifies gaps and opportunities
4. Generates prioritized suggestions (critical → high → medium → low)

Example output:
```
Multi-Agent Network Analyzer (Iterative Mode)
Analyzing: /home/user/projects/my-agents
Model: qwen2.5:14b-instruct-q5_K_M

Step 1: Discovering agent configurations...
  Found 15 agent-related files

Step 2: Building analysis context...
  Context prepared

Step 3: Generating agent suggestions...
  Generated 8 suggestions

Beginning Interactive Review
```

### Phase 2: Interactive Review

For each suggestion, you'll see:

```
======================================================================
Agent Suggestion 1/8
======================================================================

🤖 TASK-PRIORITY-ROUTER
   Type: Orchestration
   Priority: CRITICAL

📋 Purpose:
   Route incoming tasks to appropriate agents based on priority and capability

💡 Rationale:
   Currently, the network lacks a centralized routing mechanism, causing
   ad-hoc task distribution and potential bottlenecks. This agent would
   provide intelligent routing based on agent availability and task urgency.

🔧 Key Responsibilities:
   • Analyze incoming tasks and determine priority levels
   • Match tasks with available agents based on capabilities
   • Manage task queues and prevent overload

🔗 Interfaces With:
   All existing action agents, monitoring system

✨ Value:
   Improves response times by 40%, prevents agent overload, enables
   better load balancing across the network

----------------------------------------------------------------------
What would you like to do?
  [y] Yes - Add this agent and generate system prompt
  [n] No - Reject this agent
  [s] Skip - Review this agent later
  [q] Quit - Stop reviewing suggestions
----------------------------------------------------------------------

Your choice (y/n/s/q):
```

### Your Options

**[y] Yes** - Accept this agent:
```
✅ Accepting TASK-PRIORITY-ROUTER...
   Generating system prompt for task-priority-router...
   Saved to: findings/system-prompts/orchestration/task-priority-router.md
```

The tool immediately:
- Generates a comprehensive system prompt
- Saves it to the appropriate directory
- Tracks it as "accepted"

**[n] No** - Reject this agent:
```
❌ Rejecting TASK-PRIORITY-ROUTER
```

The tool:
- Records the rejection
- Moves to the next suggestion
- Includes in final summary (so you remember what you considered)

**[s] Skip** - Maybe later:
```
⏭️ Skipping TASK-PRIORITY-ROUTER (will include in summary)
```

The tool:
- Saves full details to the summary
- Lets you review it later
- Useful for "interesting but not urgent" agents

**[q] Quit** - Stop reviewing:
```
🛑 Stopping review process
   Reviewed 3 of 8 suggestions
```

The tool:
- Stops immediately
- Saves everything reviewed so far
- Generates summary with partial results

### Phase 3: Summary

After review, you get a comprehensive summary:

```
======================================================================
Saving Summary
======================================================================

📄 Summary saved to: findings/analysis-summary.md

======================================================================
Analysis Complete!
======================================================================

✅ Accepted: 3
❌ Rejected: 2
⏭️ Skipped: 1

📁 System prompts: /path/to/findings/system-prompts
📄 Full summary: /path/to/findings/analysis-summary.md
```

## Output Files

### analysis-summary.md

```markdown
# Agent Network Expansion Summary

**Analyzed Directory**: /home/user/projects/my-agents
**Analysis Date**: 2025-10-26 14:30:00
**Model Used**: qwen2.5:14b-instruct-q5_K_M

---

## Summary
- ✅ Accepted: 3 agents
- ❌ Rejected: 2 agents
- ⏭️ Skipped: 1 agents

## Accepted Agents

### Task Priority Router
- **Type**: orchestration
- **Priority**: critical
- **Purpose**: Route incoming tasks based on priority and capability
- **System Prompt**: findings/system-prompts/orchestration/task-priority-router.md

### Error Recovery Agent
- **Type**: action
- **Priority**: high
- **Purpose**: Automatically recover from common failure scenarios
- **System Prompt**: findings/system-prompts/action/error-recovery-agent.md

### Monitoring Dashboard Agent
- **Type**: action
- **Priority**: medium
- **Purpose**: Provide real-time visibility into network health
- **System Prompt**: findings/system-prompts/action/monitoring-dashboard-agent.md

## Rejected Agents
- **Redundant Logger** (action): Already have comprehensive logging

## Skipped Agents (Review Later)

### Load Balancer
- **Type**: orchestration
- **Priority**: high
- **Purpose**: Distribute workload evenly across agents
- **Rationale**: Would prevent bottlenecks during high-load periods by
  intelligently distributing tasks based on current agent utilization
```

### Generated System Prompts

Each accepted agent gets a production-ready system prompt:

```
findings/system-prompts/
├── orchestration/
│   └── task-priority-router.md
└── action/
    ├── error-recovery-agent.md
    └── monitoring-dashboard-agent.md
```

Example prompt structure:
```markdown
# Task Priority Router

**Type**: Orchestration
**Priority**: Critical
**Generated**: 2025-10-26 14:32:15

---

## Role

You are the Task Priority Router, responsible for intelligently routing
incoming tasks to appropriate agents based on priority, capability, and
current network load.

## Core Responsibilities

1. **Task Analysis**: Evaluate each incoming task to determine...
2. **Priority Assessment**: Assign priority levels based on...
3. **Agent Matching**: Match tasks with capable agents using...
[... detailed prompt continues ...]
```

## Example Session

Let's walk through a complete session:

```bash
$ python scripts/analyze_network_iterative.py ~/my-agents

Multi-Agent Network Analyzer (Iterative Mode)
Analyzing: /home/user/my-agents
Model: qwen2.5:14b-instruct-q5_K_M

Step 1: Discovering agent configurations...
  Found 12 agent-related files

Step 2: Building analysis context...
  Context prepared

Step 3: Generating agent suggestions...
  Generated 6 suggestions

======================================================================
Agent Suggestion 1/6
======================================================================

🤖 WORKFLOW-COORDINATOR
   Type: Orchestration
   Priority: CRITICAL

📋 Purpose: Orchestrate multi-step workflows across agents
💡 Rationale: Current agents work independently; workflows are manual
🔧 Key Responsibilities:
   • Define and execute multi-step workflows
   • Coordinate handoffs between agents
   • Track workflow state and progress
🔗 Interfaces With: All action agents
✨ Value: Enables complex automated workflows

Your choice (y/n/s/q): y

✅ Accepting WORKFLOW-COORDINATOR...
   Generating system prompt...
   Saved to: findings/system-prompts/orchestration/workflow-coordinator.md

======================================================================
Agent Suggestion 2/6
======================================================================

🤖 DUPLICATE-TASK-DETECTOR
   Type: Action
   Priority: MEDIUM

📋 Purpose: Identify and merge duplicate tasks
💡 Rationale: Would prevent redundant work
🔧 Key Responsibilities:
   • Compare incoming tasks with queue
   • Identify semantic duplicates
   • Merge or flag duplicates
🔗 Interfaces With: Task queue, workflow coordinator
✨ Value: Reduces wasted processing by ~15%

Your choice (y/n/s/q): n

❌ Rejecting DUPLICATE-TASK-DETECTOR

======================================================================
Agent Suggestion 3/6
======================================================================

🤖 HEALTH-MONITOR
   Type: Action
   Priority: HIGH

📋 Purpose: Monitor agent health and availability
💡 Rationale: No current health monitoring exists
🔧 Key Responsibilities:
   • Ping agents regularly
   • Track response times
   • Alert on failures
🔗 Interfaces With: All agents
✨ Value: Prevents cascading failures

Your choice (y/n/s/q): y

✅ Accepting HEALTH-MONITOR...
   Generating system prompt...
   Saved to: findings/system-prompts/action/health-monitor.md

======================================================================
Agent Suggestion 4/6
======================================================================

🤖 RATE-LIMITER
   Type: Orchestration
   Priority: LOW

📋 Purpose: Prevent API rate limit violations
💡 Rationale: Protect external API integrations
🔧 Key Responsibilities:
   • Track API call rates
   • Queue requests when approaching limits
   • Distribute calls over time
🔗 Interfaces With: External API agents
✨ Value: Prevents service disruptions

Your choice (y/n/s/q): s

⏭️ Skipping RATE-LIMITER (will include in summary)

======================================================================
Agent Suggestion 5/6
======================================================================

🤖 AUDIT-LOGGER
   Type: Action
   Priority: MEDIUM

📋 Purpose: Comprehensive audit trail of all actions
💡 Rationale: Compliance and debugging
🔧 Key Responsibilities:
   • Log all agent actions
   • Store in queryable format
   • Enable audit queries
🔗 Interfaces With: All agents
✨ Value: Compliance, debugging, analytics

Your choice (y/n/s/q): q

🛑 Stopping review process
   Reviewed 5 of 6 suggestions

Saving Summary
📄 Summary saved to: findings/analysis-summary.md

======================================================================
Analysis Complete!
======================================================================

✅ Accepted: 2
❌ Rejected: 1
⏭️ Skipped: 1

📁 System prompts: /home/user/my-agents/findings/system-prompts
📄 Full summary: /home/user/my-agents/findings/analysis-summary.md
```

## Tips for Effective Use

### 1. Review in Order
The tool presents suggestions in priority order (critical first). Trust this ordering unless you have specific needs.

### 2. Use "Skip" Liberally
If you're unsure, skip it. You can review skipped agents later from the summary without regenerating everything.

### 3. Stop When Satisfied
You don't need to review all suggestions. Stop when you have enough agents to work with.

### 4. Run Multiple Times
As your network evolves, run the analyzer again. It will suggest different agents based on new gaps.

### 5. Customize System Prompts
The generated prompts are starting points. Edit them to match your specific needs and architecture.

### 6. Track Over Time
Commit the `findings/` directory to git to track how your network evolves:
```bash
git add findings/
git commit -m "Agent network analysis - added workflow coordinator and health monitor"
```

## Advanced Usage

### Different Models

Use a different Ollama model:
```bash
python scripts/analyze_network_iterative.py . --model llama3.1:8b
python scripts/analyze_network_iterative.py . --model deepseek-r1:14b
```

### Re-analyzing After Changes

After implementing suggested agents:
```bash
# Implement the agents you accepted
# ... time passes ...

# Run again to find new gaps
python scripts/analyze_network_iterative.py .
```

The tool will analyze the updated network and suggest new complementary agents.

### Combining with Batch Mode

1. Run batch mode for comprehensive analysis:
   ```bash
   python scripts/analyze_network_local.py .
   ```

2. Review the full analysis document

3. Run iterative mode for implementation:
   ```bash
   python scripts/analyze_network_iterative.py .
   ```

4. Accept/reject based on your batch analysis review

## Troubleshooting

### "No agent files found"
- Ensure your agent configs use standard naming: `*agent*.json`, `*agent*.yaml`, `*.md`
- Check that files are in recognizable locations: `agents/`, `prompts/`, `.claude/`

### "Model not found"
```bash
# List available models
ollama list

# Pull the recommended model
ollama pull qwen2.5:14b-instruct-q5_K_M
```

### "Cannot connect to Ollama"
```bash
# Start Ollama
ollama serve

# Or check if already running
ps aux | grep ollama
```

### Suggestions seem generic
- Use a larger model: `--model qwen2.5:32b`
- Add more detail to your existing agent configurations
- Include documentation about agent relationships

## Next Steps

After running the iterative analyzer:

1. **Review the summary** at `findings/analysis-summary.md`
2. **Implement accepted agents** using the generated system prompts
3. **Revisit skipped agents** when you have capacity
4. **Re-run analysis** periodically as your network grows
5. **Track evolution** by committing findings to version control
