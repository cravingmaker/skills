# Diagrams for instruction decisions

Read this when a non-obvious branch, loop, or choice is easier to follow as a diagram. Use a list for a linear recipe, a table for reference, and a code block for code. A diagram earns its place by preventing a real wrong turn, rather than decorating instructions.

Keep questions, actions, states, commands, and entry/exit points distinguishable. Use semantic labels instead of anonymous step numbers. Label each conditional edge with its actual predicate and show the completion or recovery path. For Graphviz, diamonds suit decisions, boxes actions, ellipses states, plaintext literal commands, and double circles entry/exit. Reserve warning shapes for an actual stop boundary. These are presentation conventions, rather than instructions to run the commands shown.

Use a supported renderer already available for the task and check that the rendered labels and paths remain legible. Keep source-derived text escaped and any renderer or network dependency explicit. Do not import an upstream renderer, install tools, or open a server merely to finish an instruction edit. Keep an accessible text account when the diagram carries a material branch.
