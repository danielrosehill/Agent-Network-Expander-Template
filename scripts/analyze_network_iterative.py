#!/usr/bin/env python3
"""
Iterative Multi-Agent Network Analyzer using Ollama

Analyzes multi-agent system configurations and suggests complementary agents
one at a time, with user approval for each suggestion.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    import ollama
except ImportError:
    print("Error: ollama package not installed. Install with: pip install ollama")
    sys.exit(1)


class IterativeAgentAnalyzer:
    """Analyzes multi-agent networks and suggests improvements iteratively."""

    def __init__(self, model: str = "qwen2.5:14b-instruct-q5_K_M", batch_mode: bool = False):
        """
        Initialize the analyzer.

        Args:
            model: Ollama model to use for analysis
            batch_mode: If True, use batch processing instead of iterative
        """
        self.model = model
        self.batch_mode = batch_mode
        self.findings_dir = Path("findings")
        self.system_prompts_dir = self.findings_dir / "system-prompts"
        self.decisions = {
            "accepted": [],
            "rejected": [],
            "skipped": []
        }

    def discover_agents(self, directory: Path) -> Dict[str, List[Path]]:
        """
        Discover agent configuration files in the directory.

        Args:
            directory: Directory to search

        Returns:
            Dictionary mapping file types to lists of paths
        """
        agent_files = {
            "json": [],
            "yaml": [],
            "md": [],
            "txt": [],
            "other": []
        }

        # Common patterns for agent configs
        patterns = [
            "*agent*.json",
            "*agent*.yaml",
            "*agent*.yml",
            "*.agent.*",
            "*prompt*.md",
            "*system*.md",
            "agents/**/*",
            "prompts/**/*",
            ".claude/**/*"
        ]

        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                if file_path.is_file():
                    ext = file_path.suffix.lower().lstrip('.')
                    if ext in agent_files:
                        agent_files[ext].append(file_path)
                    else:
                        agent_files["other"].append(file_path)

        return agent_files

    def read_file_safe(self, file_path: Path, max_size: int = 100000) -> Optional[str]:
        """
        Safely read a file with size limit.

        Args:
            file_path: Path to file
            max_size: Maximum file size in bytes

        Returns:
            File contents or None if error/too large
        """
        try:
            if file_path.stat().st_size > max_size:
                return f"[File too large: {file_path.stat().st_size} bytes]"
            return file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return f"[Error reading file: {e}]"

    def build_context(self, directory: Path, agent_files: Dict[str, List[Path]]) -> str:
        """
        Build context string from discovered files.

        Args:
            directory: Base directory
            agent_files: Discovered agent files

        Returns:
            Context string for LLM
        """
        context = f"# Agent Network Analysis Context\n\n"
        context += f"**Directory**: {directory.absolute()}\n\n"

        total_files = sum(len(files) for files in agent_files.values())
        context += f"**Total agent-related files found**: {total_files}\n\n"

        # Add file inventory
        context += "## File Inventory\n\n"
        for file_type, files in agent_files.items():
            if files:
                context += f"### {file_type.upper()} Files ({len(files)})\n"
                for file_path in files[:10]:  # Limit to first 10 of each type
                    rel_path = file_path.relative_to(directory)
                    context += f"- `{rel_path}`\n"
                if len(files) > 10:
                    context += f"- ... and {len(files) - 10} more\n"
                context += "\n"

        # Add sample file contents
        context += "## Sample File Contents\n\n"
        sample_count = 0
        max_samples = 5

        for file_type, files in agent_files.items():
            if sample_count >= max_samples:
                break
            for file_path in files[:2]:  # Up to 2 samples per type
                if sample_count >= max_samples:
                    break
                rel_path = file_path.relative_to(directory)
                content = self.read_file_safe(file_path)
                context += f"### File: `{rel_path}`\n\n"
                context += f"```{file_type}\n{content[:2000]}\n```\n\n"
                sample_count += 1

        return context

    def generate_agent_suggestions(self, context: str) -> List[Dict[str, str]]:
        """
        Generate a prioritized list of agent suggestions.

        Args:
            context: Context about the agent network

        Returns:
            List of agent suggestion dictionaries
        """
        prompt = f"""You are an expert AI agent network architect. Analyze the provided multi-agent system and suggest complementary agents.

# Context
{context}

# Your Task

Generate a prioritized list of 5-10 agent suggestions that would enhance this network. Include both:
1. Orchestration & Routing Agents (coordinate workflows, manage priorities)
2. Action Agents (perform specific tasks)

For each suggestion, provide in JSON format:

{{
  "name": "agent-name",
  "type": "orchestration" or "action",
  "priority": "critical" or "high" or "medium" or "low",
  "purpose": "One sentence description",
  "rationale": "2-3 sentences explaining why this agent is needed",
  "responsibilities": ["responsibility 1", "responsibility 2", "responsibility 3"],
  "interfaces": "Which existing agents/systems this interacts with",
  "value": "Specific benefit this brings to the network"
}}

Output ONLY a valid JSON array of suggestions, ordered by priority (critical first, low last).
Begin:"""

        print(f"Analyzing with {self.model}...")
        print("Generating agent suggestions...\n")

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 3000,
                }
            )

            response_text = response['response'].strip()

            # Try to extract JSON array
            start = response_text.find('[')
            end = response_text.rfind(']') + 1

            if start >= 0 and end > start:
                json_text = response_text[start:end]
                suggestions = json.loads(json_text)
                return suggestions
            else:
                print("Warning: Could not parse JSON response. Using fallback.")
                return []

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print("Response:", response_text[:500])
            return []
        except Exception as e:
            print(f"Error during analysis: {e}")
            return []

    def present_suggestion(self, agent: Dict[str, str], index: int, total: int) -> None:
        """
        Present an agent suggestion to the user.

        Args:
            agent: Agent suggestion dictionary
            index: Current index (1-based)
            total: Total number of suggestions
        """
        print("\n" + "="*70)
        print(f"Agent Suggestion {index}/{total}")
        print("="*70)
        print(f"\n🤖 {agent['name'].upper()}")
        print(f"   Type: {agent['type'].capitalize()}")
        print(f"   Priority: {agent['priority'].upper()}\n")
        print(f"📋 Purpose:")
        print(f"   {agent['purpose']}\n")
        print(f"💡 Rationale:")
        print(f"   {agent['rationale']}\n")
        print(f"🔧 Key Responsibilities:")
        for resp in agent.get('responsibilities', []):
            print(f"   • {resp}")
        print(f"\n🔗 Interfaces With:")
        print(f"   {agent['interfaces']}\n")
        print(f"✨ Value:")
        print(f"   {agent['value']}\n")

    def get_user_decision(self) -> str:
        """
        Get user's decision about the current agent suggestion.

        Returns:
            User decision: 'yes', 'no', 'skip', or 'stop'
        """
        print("-" * 70)
        print("What would you like to do?")
        print("  [y] Yes - Add this agent and generate system prompt")
        print("  [n] No - Reject this agent")
        print("  [s] Skip - Review this agent later")
        print("  [q] Quit - Stop reviewing suggestions")
        print("-" * 70)

        while True:
            choice = input("\nYour choice (y/n/s/q): ").strip().lower()

            if choice in ['y', 'yes']:
                return 'yes'
            elif choice in ['n', 'no']:
                return 'no'
            elif choice in ['s', 'skip']:
                return 'skip'
            elif choice in ['q', 'quit', 'stop']:
                return 'stop'
            else:
                print("Invalid choice. Please enter y, n, s, or q.")

    def generate_system_prompt(self, agent: Dict[str, str]) -> str:
        """
        Generate a detailed system prompt for an agent.

        Args:
            agent: Agent specification

        Returns:
            Generated system prompt
        """
        prompt = f"""Generate a detailed, production-ready system prompt for this AI agent:

**Agent Name**: {agent['name']}
**Type**: {agent['type']}
**Purpose**: {agent['purpose']}
**Rationale**: {agent['rationale']}
**Responsibilities**: {', '.join(agent.get('responsibilities', []))}
**Interfaces**: {agent['interfaces']}
**Value**: {agent['value']}

Create a comprehensive system prompt that includes:

1. **Role Definition**: Clear statement of the agent's role
2. **Core Responsibilities**: Detailed list of duties
3. **Operational Context**: How this agent fits in the network
4. **Input Specifications**: What inputs the agent expects
5. **Output Specifications**: What outputs the agent produces
6. **Interaction Protocols**: How it communicates with other agents
7. **Error Handling**: How it handles failures
8. **Success Criteria**: How to measure effectiveness
9. **Guidelines**: Operational principles and best practices

Format the prompt in clear markdown. Make it ready to use immediately.
Begin:"""

        try:
            print(f"   Generating system prompt for {agent['name']}...")
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "num_predict": 2000,
                }
            )
            return response['response'].strip()
        except Exception as e:
            return f"# {agent['name']}\n\nError generating prompt: {e}"

    def save_agent_prompt(self, agent: Dict[str, str], prompt_content: str) -> Path:
        """
        Save agent system prompt to file.

        Args:
            agent: Agent specification
            prompt_content: Generated prompt content

        Returns:
            Path to saved file
        """
        # Determine directory based on agent type
        if agent['type'] == 'orchestration':
            target_dir = self.system_prompts_dir / "orchestration"
        else:
            target_dir = self.system_prompts_dir / "action"

        target_dir.mkdir(parents=True, exist_ok=True)

        # Create filename
        filename = agent['name'].lower().replace(' ', '-').replace('_', '-')
        filename = ''.join(c for c in filename if c.isalnum() or c == '-')
        output_file = target_dir / f"{filename}.md"

        # Write file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {agent['name']}\n\n")
            f.write(f"**Type**: {agent['type'].capitalize()}\n")
            f.write(f"**Priority**: {agent['priority'].capitalize()}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(prompt_content)

        return output_file

    def save_summary(self, directory: Path) -> Path:
        """
        Save analysis summary and decisions.

        Args:
            directory: Directory that was analyzed

        Returns:
            Path to summary file
        """
        self.findings_dir.mkdir(parents=True, exist_ok=True)
        summary_file = self.findings_dir / "analysis-summary.md"

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# Agent Network Expansion Summary\n\n")
            f.write(f"**Analyzed Directory**: {directory.absolute()}\n")
            f.write(f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Model Used**: {self.model}\n\n")
            f.write("---\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Accepted**: {len(self.decisions['accepted'])} agents\n")
            f.write(f"- **Rejected**: {len(self.decisions['rejected'])} agents\n")
            f.write(f"- **Skipped**: {len(self.decisions['skipped'])} agents\n\n")

            if self.decisions['accepted']:
                f.write("## Accepted Agents\n\n")
                for agent in self.decisions['accepted']:
                    f.write(f"### {agent['name']}\n")
                    f.write(f"- **Type**: {agent['type']}\n")
                    f.write(f"- **Priority**: {agent['priority']}\n")
                    f.write(f"- **Purpose**: {agent['purpose']}\n\n")

            if self.decisions['rejected']:
                f.write("## Rejected Agents\n\n")
                for agent in self.decisions['rejected']:
                    f.write(f"- **{agent['name']}** ({agent['type']}): {agent['purpose']}\n")
                f.write("\n")

            if self.decisions['skipped']:
                f.write("## Skipped Agents (Review Later)\n\n")
                for agent in self.decisions['skipped']:
                    f.write(f"### {agent['name']}\n")
                    f.write(f"- **Type**: {agent['type']}\n")
                    f.write(f"- **Priority**: {agent['priority']}\n")
                    f.write(f"- **Purpose**: {agent['purpose']}\n")
                    f.write(f"- **Rationale**: {agent['rationale']}\n\n")

        return summary_file

    def run_iterative(self, directory: Path):
        """
        Run iterative analysis workflow.

        Args:
            directory: Directory to analyze
        """
        print("="*70)
        print("Multi-Agent Network Analyzer (Iterative Mode)")
        print("="*70)
        print(f"\nAnalyzing: {directory.absolute()}")
        print(f"Model: {self.model}\n")

        # Discovery
        print("Step 1: Discovering agent configurations...")
        agent_files = self.discover_agents(directory)
        total = sum(len(files) for files in agent_files.values())
        print(f"  Found {total} agent-related files\n")

        if total == 0:
            print("⚠️  No agent configuration files found.")
            print("    Looking for: *agent*.json, *agent*.yaml, *.agent.*, *prompt*.md, etc.")
            return

        # Build context
        print("Step 2: Building analysis context...")
        context = self.build_context(directory, agent_files)
        print("  Context prepared\n")

        # Generate suggestions
        print("Step 3: Generating agent suggestions...")
        suggestions = self.generate_agent_suggestions(context)

        if not suggestions:
            print("⚠️  Could not generate suggestions. Check model availability.")
            return

        print(f"  Generated {len(suggestions)} suggestions\n")
        print("="*70)
        print("Beginning Interactive Review")
        print("="*70)

        # Review each suggestion
        for i, agent in enumerate(suggestions, 1):
            self.present_suggestion(agent, i, len(suggestions))

            decision = self.get_user_decision()

            if decision == 'yes':
                print(f"\n✅ Accepting {agent['name']}...")
                prompt_content = self.generate_system_prompt(agent)
                output_file = self.save_agent_prompt(agent, prompt_content)
                print(f"   Saved to: {output_file.relative_to(Path.cwd())}")
                self.decisions['accepted'].append(agent)

            elif decision == 'no':
                print(f"\n❌ Rejecting {agent['name']}")
                self.decisions['rejected'].append(agent)

            elif decision == 'skip':
                print(f"\n⏭️  Skipping {agent['name']} (will include in summary)")
                self.decisions['skipped'].append(agent)

            elif decision == 'stop':
                print(f"\n🛑 Stopping review process")
                print(f"   Reviewed {i} of {len(suggestions)} suggestions")
                break

        # Save summary
        print("\n" + "="*70)
        print("Saving Summary")
        print("="*70)
        summary_file = self.save_summary(directory)
        print(f"\n📄 Summary saved to: {summary_file}")

        # Final stats
        print("\n" + "="*70)
        print("Analysis Complete!")
        print("="*70)
        print(f"\n✅ Accepted: {len(self.decisions['accepted'])}")
        print(f"❌ Rejected: {len(self.decisions['rejected'])}")
        print(f"⏭️  Skipped: {len(self.decisions['skipped'])}")

        if self.decisions['accepted']:
            print(f"\n📁 System prompts: {self.system_prompts_dir.absolute()}")

        print(f"📄 Full summary: {summary_file.absolute()}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Iteratively analyze multi-agent networks with user approval"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory containing agent configuration (default: current directory)"
    )
    parser.add_argument(
        "-m", "--model",
        default="qwen2.5:14b-instruct-q5_K_M",
        help="Ollama model to use (default: qwen2.5:14b-instruct-q5_K_M)"
    )

    args = parser.parse_args()

    directory = Path(args.directory).resolve()

    if not directory.exists():
        print(f"❌ Error: Directory not found: {directory}")
        sys.exit(1)

    if not directory.is_dir():
        print(f"❌ Error: Not a directory: {directory}")
        sys.exit(1)

    # Check Ollama
    try:
        ollama.list()
    except Exception as e:
        print("❌ Error: Cannot connect to Ollama. Is it running?")
        print(f"   {e}")
        print("\n   Start Ollama with: ollama serve")
        sys.exit(1)

    # Check model
    try:
        models = ollama.list()
        model_names = [m['name'] for m in models.get('models', [])]
        if not any(args.model in name for name in model_names):
            print(f"⚠️  Warning: Model '{args.model}' not found locally.")
            print(f"   Available models: {', '.join(model_names)}")
            print(f"\n   Pull with: ollama pull {args.model}")
            response = input("\n   Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    except Exception as e:
        print(f"⚠️  Warning: Could not verify model: {e}")

    analyzer = IterativeAgentAnalyzer(model=args.model)
    analyzer.run_iterative(directory)


if __name__ == "__main__":
    main()
