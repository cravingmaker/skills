# UI prototype

Read this for a decision about layout, information order, density, controls, or interaction.

## Place the comparison in context

Use realistic header, navigation, data volume, and states. When the question changes an existing page, prefer a temporary rendering branch in that page's established route. Keep its data, parameters, and authentication contract intact.

Use a new clearly named prototype route only when there is no suitable page or the authorized write scope requires isolation. An isolated artifact can reproduce surrounding context with fixtures instead of mutating the live app.

## Make alternatives observable

When comparison will settle the decision, start with three structurally different variants or fewer if enough. Beyond five is usually noise. Change hierarchy, layout, or the primary interaction rather than only color and copy.

Give each variant a name. Hold data and relevant viewport conditions constant. A URL parameter such as `?variant=B` and a visible switcher make the same alternative easy to revisit.

If using a floating switcher:

- Show the current variant and labelled previous/next controls.
- Keep keyboard cycling out of focused inputs, textareas, and editable fields.
- Separate prototype controls visually from the design being judged.
- Keep the entire experiment out of production delivery.

Keep shared data plumbing where useful while allowing each variant to change structure. Use stubs for mutations; a visual comparison does not need to send a real transaction.

## Observe the actual UI

Use supported host preview or browser tools to render each relevant variant and drive its key interaction. Check the density, awkward states, and relevant viewport. Use an existing project runner only if required; do not add a server ceremony for an artifact the host can already render.

Record what was inspected and what was unavailable. A source diff cannot establish the rendered result; a static image cannot establish behavior.

Return the artifact or route, variant keys, observations, trade-offs, and a recommendation bounded by the evidence. Preserve the chosen idea and the alternatives at the authorized location. A later production build needs its own implementation and validation; do not silently promote the prototype.
