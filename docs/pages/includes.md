# Using Includes in Python API

PMD's include functionality allows you to compose templates from reusable snippets, making it easy to build modular, maintainable prompt libraries. This page covers how to use includes programmatically through the Python API.

## Basic Include Usage

### Setting Up the Renderer

The key to using includes is setting the `base_path` parameter when creating a `PmdRenderer`. This tells PMD where to resolve relative include paths:

```python
from pathlib import Path
from pmd.parser import PmdParser
from pmd.renderer import PmdRenderer

# Define base path for includes
template_dir = Path("./templates")

# Parse your main template
parser = PmdParser()
template_content = """
{% include "header.pmd" %}

Main content here.

{% include "footer.pmd" %}
"""

metadata, nodes = parser.parse(template_content)

# Create renderer with base_path
renderer = PmdRenderer(
    context={"app_name": "MyApp"},
    base_path=template_dir
)

# Render - includes will be resolved relative to base_path
output = renderer.render(nodes)
```

## Creating Reusable Snippets

### Example: Prompt Building Blocks

Create a library of reusable prompt components:

**templates/snippets/system_role.pmd**:
```pmd
You are {{role}}, a helpful AI assistant.
```

**templates/snippets/task_context.pmd**:
```pmd
## Task Context

User: {{user_name}}
Session: {{session_id}}
Timestamp: {{timestamp}}
```

**templates/snippets/output_format.pmd**:
```pmd
## Output Requirements

- Provide responses in {{format}} format
- Keep responses {{length}}
- Use {{tone}} tone
```

### Using the Snippets

```python
from pathlib import Path
from pmd.parser import PmdParser
from pmd.renderer import PmdRenderer

# Main template that composes snippets
main_template = """
{% include "snippets/system_role.pmd" %}

{% include "snippets/task_context.pmd" %}

## User Request

{{user_request}}

{% include "snippets/output_format.pmd" %}
"""

# Parse and render
parser = PmdParser()
_, nodes = parser.parse(main_template)

renderer = PmdRenderer(
    context={
        "role": "technical expert",
        "user_name": "Alice",
        "session_id": "sess_123",
        "timestamp": "2024-01-19T10:30:00Z",
        "user_request": "Explain quantum computing",
        "format": "markdown",
        "length": "concise",
        "tone": "professional"
    },
    base_path=Path("./templates")
)

prompt = renderer.render(nodes)
print(prompt)
```

## Dynamic Include Loading

### PmdComposer

Include complex prompts dynamically using `PmdComposer`:

```python
from pathlib import Path
from pmd.composer import PmdComposer

# Usage
manager = PmdComposer(Path("./templates"))

# Compose a complex prompt from multiple snippets
prompt = manager.compose_prompt(
    snippets=[
        "snippets/system_role.pmd",
        "snippets/task_context.pmd",
        "snippets/chain_of_thought.pmd",
        "snippets/output_format.pmd"
    ],
    context={
        "role": "data scientist",
        "user_name": "Bob",
        "task": "Analyze customer churn",
        "format": "JSON",
        "tone": "analytical"
    }
)
```

## Conditional Snippet Loading

### Using Conditionals with Includes

```python
# Template with conditional includes
template = """
{% include "snippets/system_role.pmd" %}

{% if use_examples %}
{% include "snippets/few_shot_examples.pmd" %}
{% endif %}

## Task

{{task}}

{% if detailed_output %}
{% include "snippets/detailed_format.pmd" %}
{% else %}
{% include "snippets/brief_format.pmd" %}
{% endif %}
"""

parser = PmdParser()
_, nodes = parser.parse(template)

# Render with detailed mode
renderer = PmdRenderer(
    context={
        "role": "assistant",
        "use_examples": True,
        "task": "Summarize the article",
        "detailed_output": True
    },
    base_path=Path("./templates")
)

prompt = renderer.render(nodes)
```

## Nested Includes

Includes can reference other includes, creating a hierarchy of snippets. **Important**: All include paths are always resolved relative to the `base_path` set in the renderer, not relative to the file doing the including.

### Understanding Base Path Resolution

Given this directory structure:

```
templates/
  main.pmd
  snippets/
    complete_prompt.pmd
    header_section.pmd
    system_role.pmd
    safety_guidelines.pmd
    body_section.pmd
    footer_section.pmd
```

**templates/snippets/complete_prompt.pmd**:
```pmd
{% include "snippets/header_section.pmd" %}

{% include "snippets/body_section.pmd" %}

{% include "snippets/footer_section.pmd" %}
```

**templates/snippets/header_section.pmd**:
```pmd
{% include "snippets/system_role.pmd" %}

{% include "snippets/safety_guidelines.pmd" %}
```

Notice that even though `header_section.pmd` is in the `snippets/` directory, it **still uses `"snippets/system_role.pmd"`** in its include statement, not just `"system_role.pmd"`. This is because all paths are resolved from `base_path`.

### Example: Nested Include Rendering

```python
from pathlib import Path
from pmd.parser import PmdParser
from pmd.renderer import PmdRenderer

# Parse the main template
parser = PmdParser()
_, nodes = parser.parse('{% include "snippets/complete_prompt.pmd" %}')

# Set base_path to templates/
renderer = PmdRenderer(
    context={"role": "assistant"},
    base_path=Path("./templates")
)

# All includes are resolved from ./templates/
# - snippets/complete_prompt.pmd -> ./templates/snippets/complete_prompt.pmd
# - snippets/header_section.pmd -> ./templates/snippets/header_section.pmd
# - snippets/system_role.pmd -> ./templates/snippets/system_role.pmd
output = renderer.render(nodes)
```

### Deep Nesting Example

You can nest includes as deeply as needed:

**templates/layouts/full_prompt.pmd**:
```pmd
{% include "sections/preamble.pmd" %}

{% include "sections/main_content.pmd" %}

{% include "sections/conclusion.pmd" %}
```

**templates/sections/preamble.pmd**:
```pmd
{% include "components/header.pmd" %}

{% include "components/instructions.pmd" %}
```

**templates/components/header.pmd**:
```pmd
{% include "atoms/logo.pmd" %}

{% include "atoms/title.pmd" %}
```

```python
# All paths resolve from base_path, no matter how deep the nesting
parser = PmdParser()
_, nodes = parser.parse('{% include "layouts/full_prompt.pmd" %}')

renderer = PmdRenderer(
    context={"title": "My Prompt"},
    base_path=Path("./templates")
)

output = renderer.render(nodes)
```

### Why Base Path Matters

This design makes your templates portable and predictable:

```python
# ✅ CORRECT: All paths from base_path
# templates/snippets/section.pmd contains:
{% include "snippets/subsection.pmd" %}

# ❌ WRONG: Don't use relative paths from the current file
# templates/snippets/section.pmd should NOT contain:
{% include "subsection.pmd" %}  # This won't work!
```

### Practical Tip: Organizing Nested Structures

Use consistent path prefixes to make nested includes clear:

```
templates/
  prompts/
    agent/
      researcher.pmd    -> includes "components/agent/..."
      analyzer.pmd      -> includes "components/agent/..."
  components/
    agent/
      role.pmd          -> includes "atoms/agent/..."
      tools.pmd         -> includes "atoms/agent/..."
  atoms/
    agent/
      identity.pmd
      capabilities.pmd
```

This structure makes it obvious that all includes use the full path from `templates/`.

## Error Handling

Always handle include errors gracefully:

```python
from pathlib import Path
from pmd.parser import PmdParser
from pmd.renderer import PmdRenderer


def safe_render(template_content: str, context: dict, base_path: Path) -> str:
    """Safely render a template with error handling."""
    try:
        parser = PmdParser()
        _, nodes = parser.parse(template_content)

        renderer = PmdRenderer(context=context, base_path=base_path)
        return renderer.render(nodes)

    except FileNotFoundError as e:
        # Handle missing include files
        print(f"Warning: Include file not found - {e}")
        return template_content  # Return unrendered template

    except Exception as e:
        # Handle other rendering errors
        print(f"Error rendering template: {e}")
        return ""


# Usage
result = safe_render(
    '{% include "optional_snippet.pmd" %}\nMain content.',
    context={},
    base_path=Path("./templates")
)
```

## Best Practices

### 1. Organize Snippets by Purpose

```
templates/
  snippets/
    system/
      role_definitions.pmd
      safety_guidelines.pmd
    formatting/
      json_output.pmd
      markdown_output.pmd
    examples/
      few_shot_classification.pmd
      few_shot_extraction.pmd
    sections/
      header.pmd
      footer.pmd
```

### 2. Use Descriptive Naming

```python
# Good: Clear, descriptive names
{% include "snippets/system/expert_role.pmd" %}
{% include "snippets/formatting/structured_json_output.pmd" %}

# Avoid: Vague names
{% include "snippets/s1.pmd" %}
{% include "snippets/format.pmd" %}
```

### 3. Keep Snippets Focused

Each snippet should have a single, clear purpose:

```pmd
# Good: Focused snippet
# file: role_definition.pmd
You are a {{role}} with expertise in {{domain}}.
```

```pmd
# Avoid: Mixing multiple concerns
# file: everything.pmd
You are a {{role}}.
Task: {{task}}
Output format: {{format}}
```

### 4. Document Snippet Context Requirements

Add metadata to snippets documenting required context variables:

```pmd
---
name: role-definition
version: 1.0.0
required_context:
  - role
  - domain
  - expertise_level
---

You are a {{role}} with {{expertise_level}} expertise in {{domain}}.
```

### 5. Cache Parsed Templates

Parse templates once, render many times:

```python
class OptimizedRenderer:
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
        self.parser = PmdParser()
        self.parsed_cache = {}

    def get_nodes(self, template_content: str):
        cache_key = hash(template_content)

        if cache_key not in self.parsed_cache:
            _, nodes = self.parser.parse(template_content)
            self.parsed_cache[cache_key] = nodes

        return self.parsed_cache[cache_key]

    def render(self, template_content: str, context: dict) -> str:
        nodes = self.get_nodes(template_content)
        renderer = PmdRenderer(context=context, base_path=self.template_dir)
        return renderer.render(nodes)
```

## Real-World Example: Multi-Agent System

```python
from pathlib import Path
from pmd.parser import PmdParser
from pmd.renderer import PmdRenderer


class AgentPromptBuilder:
    """Build prompts for different agent types using snippets."""

    def __init__(self, snippets_dir: Path):
        self.snippets_dir = snippets_dir
        self.parser = PmdParser()

    def build_agent_prompt(
            self,
            agent_type: str,
            task: str,
            context: dict
    ) -> str:
        """Build a prompt for a specific agent type."""

        # Map agent types to snippet combinations
        snippet_map = {
            "researcher": [
                "roles/researcher.pmd",
                "capabilities/web_search.pmd",
                "output/structured_findings.pmd"
            ],
            "analyzer": [
                "roles/analyzer.pmd",
                "capabilities/data_analysis.pmd",
                "output/insights_report.pmd"
            ],
            "writer": [
                "roles/writer.pmd",
                "capabilities/content_creation.pmd",
                "output/polished_text.pmd"
            ]
        }

        snippets = snippet_map.get(agent_type, [])

        # Build the main template
        template = "\n\n".join([
            f'{{% include "{snippet}" %}}'
            for snippet in snippets
        ])

        template += f"\n\n## Current Task\n\n{task}"

        # Render
        _, nodes = self.parser.parse(template)
        renderer = PmdRenderer(
            context=context,
            base_path=self.snippets_dir
        )

        return renderer.render(nodes)


# Usage
builder = AgentPromptBuilder(Path("./agent_snippets"))

# Build a researcher agent prompt
researcher_prompt = builder.build_agent_prompt(
    agent_type="researcher",
    task="Find the latest developments in quantum computing",
    context={
        "expertise": "quantum physics",
        "sources": ["arxiv", "google scholar"],
        "depth": "comprehensive"
    }
)

# Build an analyzer agent prompt
analyzer_prompt = builder.build_agent_prompt(
    agent_type="analyzer",
    task="Analyze customer feedback trends",
    context={
        "data_source": "customer_reviews.json",
        "analysis_type": "sentiment",
        "output_format": "executive_summary"
    }
)
```
