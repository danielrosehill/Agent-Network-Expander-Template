#!/usr/bin/env python3
"""
Local Multi-Agent Network Analyzer using Ollama

Analyzes multi-agent system configurations and suggests complementary
orchestration and action agents using local LLM inference via Ollama.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import ollama
except ImportError:
    print("Error: ollama package not installed. Install with: pip install ollama")
    sys.exit(1)


class AgentNetworkAnalyzer:
    """Analyzes multi-agent networks and suggests improvements."""

    def __init__(self, model: str = "qwen2.5:14b-instruct-q5_K_M"):
        """
        Initialize the analyzer.

        Args:
            model: Ollama model to use for analysis
        """
        self.model = model
        self.findings_dir = Path("findings")
        self.system_prompts_dir = self.findings_dir / "system-prompts"

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

    def create_analysis_prompt(self, context: str) -> str:
        """
        Create the analysis prompt for the LLM.

        Args:
            context: Context about the agent network

        Returns:
            Formatted prompt
        """
        prompt = """You are an expert AI agent network architect. Analyze the provided multi-agent system configuration and suggest complementary agents.

# Your Task

Based on the agent network context provided, identify gaps and suggest new agents at two levels:

1. **Orchestration & Routing Agents**: Coordinate workflows, manage priorities, route tasks
2. **Action Agents**: Perform specific tasks and operations

# Analysis Framework

## Current State Assessment
- What agents currently exist?
- How do they interact?
- What patterns emerge?

## Gap Analysis
- What coordination is missing?
- What capabilities are absent?
- What error handling is needed?
- What monitoring is lacking?

## Recommendations

### Orchestration & Routing Agents
For each suggested orchestration agent, provide:
- **Agent Name**: Clear, descriptive name
- **Purpose**: What coordination role it serves
- **Responsibilities**: Specific duties
- **Interfaces With**: Which agents it coordinates
- **Value Add**: Why this improves the network

### Action Agents
For each suggested action agent, provide:
- **Agent Name**: Clear, descriptive name
- **Purpose**: What task it performs
- **Capabilities**: Specific functions
- **Triggers**: What activates this agent
- **Outputs**: What it produces
- **Value Add**: Why this agent is needed

## Implementation Priority
Rank suggestions by impact and implementation effort.

# Context

"""
        prompt += context

        prompt += """

# Output Format

Provide your analysis in markdown format following this structure:

# Multi-Agent Network Analysis

## Executive Summary
[2-3 sentence overview]

## Current Agent Inventory
[List discovered agents]

## Agent Relationship Map
[Describe interactions]

## Recommendations

### Orchestration & Routing Agents
[Detailed suggestions]

### Action Agents
[Detailed suggestions]

## Implementation Priority
[Ranked list]

## Integration Considerations
[Implementation guidance]

Begin your analysis:"""

        return prompt

    def analyze_with_ollama(self, prompt: str) -> str:
        """
        Run analysis using Ollama.

        Args:
            prompt: Analysis prompt

        Returns:
            LLM response
        """
        print(f"Analyzing with Ollama model: {self.model}")
        print("This may take a few minutes...\n")

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 4000,
                }
            )
            return response['response']
        except Exception as e:
            return f"Error during analysis: {e}"

    def save_findings(self, analysis: str, directory: Path) -> Path:
        """
        Save analysis findings to file.

        Args:
            analysis: Analysis text
            directory: Base directory being analyzed

        Returns:
            Path to saved file
        """
        self.findings_dir.mkdir(parents=True, exist_ok=True)

        output_file = self.findings_dir / "agent-network-analysis.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Multi-Agent Network Analysis\n\n")
            f.write(f"**Analyzed Directory**: {directory.absolute()}\n")
            f.write(f"**Analysis Model**: {self.model}\n")
            f.write(f"**Generated**: {Path.cwd()}\n\n")
            f.write("---\n\n")
            f.write(analysis)

        return output_file

    def offer_system_prompts(self) -> bool:
        """
        Ask user if they want system prompts generated.

        Returns:
            True if user wants prompts
        """
        print("\n" + "="*60)
        print("Analysis complete!")
        print("="*60)
        print("\nWould you like to generate system prompts for the recommended agents?")
        print("1. Yes, generate all prompts")
        print("2. No, just the analysis is fine")
        print("3. Let me review first, I'll run again later")

        while True:
            choice = input("\nEnter choice (1-3): ").strip()
            if choice == "1":
                return True
            elif choice in ["2", "3"]:
                return False
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def generate_system_prompts(self, analysis: str):
        """
        Generate system prompts for recommended agents.

        Args:
            analysis: The analysis containing agent recommendations
        """
        print("\nGenerating system prompts...")

        # Create directories
        orchestration_dir = self.system_prompts_dir / "orchestration"
        action_dir = self.system_prompts_dir / "action"
        orchestration_dir.mkdir(parents=True, exist_ok=True)
        action_dir.mkdir(parents=True, exist_ok=True)

        prompt = f"""Based on this agent network analysis, generate detailed system prompts for each recommended agent.

For each agent, create a complete system prompt that includes:
- Role and purpose
- Specific responsibilities
- Input/output specifications
- Interaction protocols
- Error handling approach
- Success criteria

Analysis:
{analysis}

Generate system prompts in markdown format, one per agent. Separate each with "---AGENT---".
Format each prompt as:

# Agent: [Name]

## Role
[Description]

## Responsibilities
[List]

## Inputs
[Specification]

## Outputs
[Specification]

## Interaction Protocol
[How it works with other agents]

## Error Handling
[Approach]

## Success Criteria
[Metrics]

Begin generating system prompts:"""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "num_predict": 8000,
                }
            )

            prompts_text = response['response']

            # Split by agent separator
            agent_prompts = prompts_text.split("---AGENT---")

            # Save each prompt
            for i, agent_prompt in enumerate(agent_prompts, 1):
                agent_prompt = agent_prompt.strip()
                if not agent_prompt:
                    continue

                # Try to extract agent name from first line
                lines = agent_prompt.split('\n')
                name = f"agent-{i}"
                for line in lines[:3]:
                    if "Agent:" in line or "# Agent" in line:
                        name = line.split(":")[-1].strip().lower().replace(" ", "-")
                        name = "".join(c for c in name if c.isalnum() or c == "-")
                        break

                # Determine if orchestration or action (simple heuristic)
                is_orchestration = any(word in agent_prompt.lower()
                                      for word in ["orchestrat", "coordinat", "rout", "priorit"])

                target_dir = orchestration_dir if is_orchestration else action_dir
                output_file = target_dir / f"{name}.md"

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(agent_prompt)

                print(f"  Generated: {output_file.relative_to(self.findings_dir)}")

            print(f"\nSystem prompts saved to: {self.system_prompts_dir}")

        except Exception as e:
            print(f"Error generating system prompts: {e}")

    def run(self, directory: Path, generate_prompts: bool = False):
        """
        Run the complete analysis workflow.

        Args:
            directory: Directory to analyze
            generate_prompts: Whether to generate system prompts
        """
        print("="*60)
        print("Multi-Agent Network Analyzer (Local)")
        print("="*60)
        print(f"\nAnalyzing directory: {directory.absolute()}")
        print(f"Using model: {self.model}\n")

        # Discover agents
        print("Step 1: Discovering agent configuration files...")
        agent_files = self.discover_agents(directory)
        total = sum(len(files) for files in agent_files.values())
        print(f"  Found {total} agent-related files\n")

        if total == 0:
            print("No agent configuration files found.")
            print("Looking for: *agent*.json, *agent*.yaml, *.agent.*, *prompt*.md, etc.")
            return

        # Build context
        print("Step 2: Building analysis context...")
        context = self.build_context(directory, agent_files)
        print("  Context prepared\n")

        # Create prompt
        print("Step 3: Creating analysis prompt...")
        prompt = self.create_analysis_prompt(context)
        print("  Prompt ready\n")

        # Analyze
        print("Step 4: Running analysis with Ollama...")
        analysis = self.analyze_with_ollama(prompt)

        # Save findings
        print("\nStep 5: Saving findings...")
        output_file = self.save_findings(analysis, directory)
        print(f"  Saved to: {output_file}\n")

        # Offer to generate prompts
        if generate_prompts or self.offer_system_prompts():
            self.generate_system_prompts(analysis)

        print("\n" + "="*60)
        print("Analysis Complete!")
        print("="*60)
        print(f"\nReview findings at: {output_file}")
        print(f"Findings directory: {self.findings_dir.absolute()}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze multi-agent networks using local Ollama inference"
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
    parser.add_argument(
        "-p", "--prompts",
        action="store_true",
        help="Automatically generate system prompts without asking"
    )

    args = parser.parse_args()

    directory = Path(args.directory).resolve()

    if not directory.exists():
        print(f"Error: Directory not found: {directory}")
        sys.exit(1)

    if not directory.is_dir():
        print(f"Error: Not a directory: {directory}")
        sys.exit(1)

    # Check if Ollama is available
    try:
        ollama.list()
    except Exception as e:
        print("Error: Cannot connect to Ollama. Is it running?")
        print(f"  {e}")
        print("\nStart Ollama with: ollama serve")
        sys.exit(1)

    # Check if model is available
    try:
        models = ollama.list()
        model_names = [m['name'] for m in models.get('models', [])]
        if not any(args.model in name for name in model_names):
            print(f"Warning: Model '{args.model}' not found locally.")
            print(f"Available models: {', '.join(model_names)}")
            print(f"\nPull the model with: ollama pull {args.model}")
            response = input("\nContinue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    except Exception as e:
        print(f"Warning: Could not verify model availability: {e}")

    analyzer = AgentNetworkAnalyzer(model=args.model)
    analyzer.run(directory, generate_prompts=args.prompts)


if __name__ == "__main__":
    main()
