from margarita.parser import MargaritaParser
from margarita.renderer import MargaritaRenderer

template = """
You are a helpful assistant.

Task: {{task}}

{% if context %}
Context:
{{context}}
{% endif %}

Please provide a detailed response.
"""

# Parse the template
parser = MargaritaParser()
metadata, nodes = parser.parse(template)

# Create a renderer with context
renderer = MargaritaRenderer(
    context={"task": "Summarize the key points", "context": "User is researching AI agents"}
)

# Render the output
prompt = renderer.render(nodes)
print(prompt)
