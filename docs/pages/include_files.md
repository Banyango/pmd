# Include Files

Reuse template fragments using `{% include "file.pmd" %}`. Includes are resolved relative to the including template's directory.

Example

`header.pmd`:

```pmd
This is the header content.
```

`page.pmd`:

```pmd
{% include "header.pmd" %}

# Page Title

Content goes here using the same context.
```

Rendered result

When rendering `page.pmd`, the output will include the header content followed by the page body:

```text
This is the header content.

# Page Title

Content goes here using the same context.
```

Behavior

- Included files have access to the same rendering context as the parent template.
- Paths are resolved relative to the parent template's directory (the CLI and renderer set `base_path`).
- Avoid circular includes; they can cause infinite loops or errors.

## Using Includes in Python API

When using PMD programmatically, you must set the `base_path` when creating the renderer. **All include paths are resolved relative to this base path**, not relative to the file doing the including.

```python
from pathlib import Path
from pmd.parser import PmdParser
from pmd.renderer import PmdRenderer

# Parse your template
parser = PmdParser()
template = '{% include "header.pmd" %}\n\nMain content here.'
_, nodes = parser.parse(template)

# Set base_path - all includes resolve from here
renderer = PmdRenderer(
    context={"title": "My Page"},
    base_path=Path("./templates")  # header.pmd will be loaded from ./templates/header.pmd
)

output = renderer.render(nodes)
```

**Important**: Even in nested includes, all paths are from `base_path`. If `snippets/section.pmd` includes another file, it must use the full path from `base_path`:

```pmd
{# Inside templates/snippets/section.pmd #}
{% include "snippets/subsection.pmd" %}  {# NOT just "subsection.pmd" #}
```

See the [Using Includes](includes.md) page for comprehensive examples and patterns.

Tip: Use includes for headers, footers, and small shared components to keep templates DRY and maintainable.
