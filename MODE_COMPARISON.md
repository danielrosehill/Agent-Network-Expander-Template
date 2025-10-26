# Iterative vs Batch Mode Comparison

## Quick Decision Guide

**Choose Iterative Mode if you:**
- Want to implement agents progressively
- Prefer to make decisions one at a time
- Want to stop early once you have enough suggestions
- Are actively developing and want immediate system prompts
- Like interactive, hands-on workflows

**Choose Batch Mode if you:**
- Need comprehensive planning documentation
- Want to see all possibilities before deciding
- Are creating reports for team discussion
- Prefer to analyze first, implement later
- Want to explore multiple architectural directions

## Detailed Comparison

### Workflow

#### Iterative Mode
```
1. Analyze network
2. Present suggestion #1
3. User decides → Generate prompt if accepted
4. Present suggestion #2
5. User decides → Generate prompt if accepted
...
N. Generate summary of all decisions
```

**User experience**: Interactive, progressive, hands-on

#### Batch Mode
```
1. Analyze network
2. Generate complete analysis document
3. List all suggestions at once
4. (Optional) Generate all system prompts
5. User reviews document later
```

**User experience**: Comprehensive, documentation-focused

### Output Files

#### Iterative Mode Outputs

```
findings/
├── analysis-summary.md          # Decisions summary
└── system-prompts/              # Only for ACCEPTED agents
    ├── orchestration/
    │   ├── agent-1.md
    │   └── agent-2.md
    └── action/
        └── agent-3.md
```

**analysis-summary.md** contains:
- List of accepted agents (with prompt locations)
- List of rejected agents
- Full details of skipped agents (for later review)

#### Batch Mode Outputs

```
findings/
├── agent-network-analysis.md    # Complete analysis
└── system-prompts/              # Generated if requested
    ├── orchestration/           # ALL suggested agents
    │   ├── agent-1.md
    │   ├── agent-2.md
    │   ├── agent-3.md
    │   └── agent-4.md
    └── action/
        ├── agent-5.md
        ├── agent-6.md
        └── agent-7.md
```

**agent-network-analysis.md** contains:
- Executive summary
- Current agent inventory
- Relationship map
- All recommendations (orchestration + action)
- Implementation priorities
- Integration considerations

### Decision Making

#### Iterative Mode

**When**: During the analysis process
**How**: For each suggestion, choose:
- [y] Yes - Accept and generate prompt immediately
- [n] No - Reject
- [s] Skip - Maybe later (full details in summary)
- [q] Quit - Stop reviewing

**Advantage**: Make informed decisions with full context
**Result**: Only generate what you actually need

#### Batch Mode

**When**: After reviewing the complete document
**How**:
- Read entire analysis first
- Decide which agents to implement
- Either generate all prompts or cherry-pick specific ones

**Advantage**: See complete picture before deciding
**Result**: Comprehensive documentation for planning

### Use Case Examples

#### Iterative Mode Use Cases

**1. Active Development**
```bash
# You're actively building your agent network
python scripts/analyze_network_iterative.py .

# Review suggestions one-by-one
# Accept critical orchestration agents immediately
# System prompts ready to use right away
```

**2. Incremental Expansion**
```bash
# You implemented 2 agents last week
# Run analysis again to find new gaps
python scripts/analyze_network_iterative.py .

# Network has evolved, suggestions are different
# Accept what fits current priorities
```

**3. Time-Constrained Implementation**
```bash
# You only have time to implement 2-3 new agents
python scripts/analyze_network_iterative.py .

# Review until you have enough
# Choose [q] to quit early
# Come back later for more
```

#### Batch Mode Use Cases

**1. Architecture Planning**
```bash
# Planning next quarter's agent architecture
python scripts/analyze_network_local.py . --prompts

# Generate complete analysis document
# Share with team for discussion
# Prioritize as a group
```

**2. Documentation**
```bash
# Need to document current state and future directions
python scripts/analyze_network_local.py .

# Creates comprehensive analysis
# Useful for onboarding new team members
# Shows what's missing and why
```

**3. Exploration**
```bash
# Exploring different architectural approaches
python scripts/analyze_network_local.py scenario-a/
python scripts/analyze_network_local.py scenario-b/

# Compare full analyses side-by-side
# Decide on direction based on complete picture
```

### Command Comparison

#### Iterative Mode Commands

**Claude Code:**
```bash
/review-agent-network-iterative
```

**Local:**
```bash
# Basic usage
python scripts/analyze_network_iterative.py .

# With different model
python scripts/analyze_network_iterative.py . --model llama3.1:8b

# Specific directory
python scripts/analyze_network_iterative.py ~/projects/my-agents
```

#### Batch Mode Commands

**Claude Code:**
```bash
/review-agent-network
```

**Local:**
```bash
# Basic usage
python scripts/analyze_network_local.py .

# Auto-generate all system prompts
python scripts/analyze_network_local.py . --prompts

# With different model
python scripts/analyze_network_local.py . --model deepseek-r1:14b
```

### Performance

#### Iterative Mode

**Speed**: Slower overall (generates prompts on-demand)
- Analysis phase: ~30-60 seconds
- Per accepted agent: ~15-30 seconds to generate prompt
- Total time: Depends on how many you accept

**Resource usage**: Moderate
- Only generates prompts for accepted agents
- Can stop anytime to conserve resources

#### Batch Mode

**Speed**: Faster for complete analysis
- Analysis phase: ~60-120 seconds
- Optional prompt generation: ~2-5 minutes (all at once)
- Total time: Predictable and fixed

**Resource usage**: Higher if generating all prompts
- Generates everything upfront
- More efficient for generating many prompts

### Example Sessions

#### Iterative Mode Session

```
$ python scripts/analyze_network_iterative.py ~/my-agents

Analyzing: /home/user/my-agents
Found 15 agent files

Generated 7 suggestions

======= Suggestion 1/7 =======
🤖 TASK-ROUTER (Orchestration, CRITICAL)
Purpose: Route tasks to appropriate agents
[... details ...]

Your choice (y/n/s/q): y
✅ Accepted! Generated: findings/system-prompts/orchestration/task-router.md

======= Suggestion 2/7 =======
🤖 DUPLICATE-DETECTOR (Action, MEDIUM)
Purpose: Identify duplicate tasks
[... details ...]

Your choice (y/n/s/q): n
❌ Rejected

======= Suggestion 3/7 =======
🤖 HEALTH-MONITOR (Action, HIGH)
Purpose: Monitor agent health
[... details ...]

Your choice (y/n/s/q): y
✅ Accepted! Generated: findings/system-prompts/action/health-monitor.md

======= Suggestion 4/7 =======
🤖 RATE-LIMITER (Orchestration, LOW)
Purpose: Prevent API rate limit violations
[... details ...]

Your choice (y/n/s/q): q
🛑 Stopped early (reviewed 4/7)

✅ Accepted: 2 agents
❌ Rejected: 1 agent
⏭️ Skipped: 0 agents
📄 Summary: findings/analysis-summary.md
```

**Result**: 2 system prompts generated, decisions saved, partial review

#### Batch Mode Session

```
$ python scripts/analyze_network_local.py ~/my-agents --prompts

Analyzing: /home/user/my-agents
Found 15 agent files

Building context...
Creating analysis prompt...
Running analysis with Ollama...

Analysis complete!
Saved to: findings/agent-network-analysis.md

Generating system prompts for 7 agents...
  Generated: orchestration/task-router.md
  Generated: action/duplicate-detector.md
  Generated: action/health-monitor.md
  Generated: orchestration/rate-limiter.md
  Generated: action/audit-logger.md
  Generated: action/error-recovery.md
  Generated: orchestration/workflow-coordinator.md

Complete!
  Analysis: findings/agent-network-analysis.md
  Prompts: findings/system-prompts/
```

**Result**: Complete analysis document + 7 system prompts ready to review

## Recommendations by Scenario

### Scenario: Starting a New Agent Network

**Recommended**: Batch Mode
- Get comprehensive view of what you need
- Plan architecture holistically
- Document for stakeholders

### Scenario: Expanding Existing Network

**Recommended**: Iterative Mode
- Add agents incrementally
- Focus on current priorities
- Generate only what you'll implement now

### Scenario: Team Planning Session

**Recommended**: Batch Mode
- Generate analysis beforehand
- Share document with team
- Discuss all options together

### Scenario: Solo Development

**Recommended**: Iterative Mode
- Make decisions as you go
- Stop when you have enough work
- Come back later for more

### Scenario: Research/Exploration

**Recommended**: Batch Mode
- Explore all possibilities
- Compare different approaches
- Document findings

### Scenario: CI/CD Integration

**Recommended**: Batch Mode
- Automated, predictable output
- Complete documentation each run
- Track evolution over time

## Can I Use Both?

**Yes!** They complement each other:

### Combined Workflow

1. **Initial planning** - Use batch mode:
   ```bash
   python scripts/analyze_network_local.py .
   ```
   Review the complete analysis, understand all options

2. **Implementation** - Use iterative mode:
   ```bash
   python scripts/analyze_network_iterative.py .
   ```
   Accept/reject based on priorities from batch analysis
   Generate prompts only for what you'll implement now

3. **Periodic review** - Use batch mode:
   ```bash
   python scripts/analyze_network_local.py .
   ```
   Track how the network has evolved
   Document new gaps

4. **Incremental expansion** - Use iterative mode:
   ```bash
   python scripts/analyze_network_iterative.py .
   ```
   Add agents based on new gaps identified

## Summary

| Aspect | Iterative Mode | Batch Mode |
|--------|---------------|------------|
| **Decision timing** | During analysis | After analysis |
| **System prompts** | On-demand for accepted | All at once (optional) |
| **Output focus** | Decisions + selected prompts | Complete analysis |
| **Best for** | Active development | Planning & documentation |
| **Time investment** | Variable (can stop early) | Fixed (complete analysis) |
| **User involvement** | High (interactive) | Low (review afterward) |
| **Flexibility** | High (adapt as you go) | Low (all or nothing) |
| **Documentation** | Decision summary | Comprehensive analysis |

**Bottom line**: Default to **Iterative Mode** for most use cases. Use **Batch Mode** when you need comprehensive planning documentation or team collaboration.
