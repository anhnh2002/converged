How should I structure prompts for Nano-Banana? (Prompt anatomy)
Good image prompts have a consistent structure. Use the following prompt anatomy to get precise, repeatable results:

Prompt anatomy (recommended order)
Action / Goal — what do you want the model to do? (e.g., “Edit this selfie to create a professional headshot” or “Generate a product lifestyle photo combining these two images”).
Subject(s) — who or what is in the image? Be specific about identity, age, number of people, items, etc.
Attributes — visual characteristics: clothing, facial expressions, eye color, hair, props.
Environment & Lighting — location, time of day, mood lighting, focal length, lens hints (“35mm portrait”).
Style & Finish — photographic style (cinematic, studio, film grain, hyperreal), or art style (oil painting, vector, comic).
Constraints / Safety — anything to avoid (no logos, no nudity, no medical text).
Consistency token (optional) — short phrase that you reuse to maintain character recognition across multiple prompts (e.g., “Use the ‘Luna scarf’ character reference”).
Hints for character consistency (practical steps)
Use a “reference phrase”: include a short, unique phrase tied to the subject (e.g., “character token: ‘Maya-blue-jacket’”) in every prompt. The model will more reliably link edits to the same character if you reuse this phrase.
Include anchored details: specify distinctive, immutable features (e.g., “left eyebrow scar, green birthmark on right cheek”) so the model has fixed anchors to maintain.
Maintain pose and framing when possible: if you want true continuity, keep the camera angle/pose description similar across prompts.
Start from the same original image: for editing workflows, always supply the same source image as the anchor. When you must change photos, include the original image as an extra input and explain the transformation.
What are common failure modes and how do I fix them?
Failure: identity drift (subject looks different)
Cause: the model over-generalized a requested style or misinterpreted a constraint. Fixes: add an explicit “preserve” clause, attach the original image as a reference, or perform edits in smaller steps and validate intermediate outputs.

Failure: inconsistent props or hands
Cause: hands and small accessories are historically tricky for many image models. Fixes: include micro-constraints (“preserve watch on right wrist”), provide a detailed close-up reference for small items, or run a final targeted correction step focusing only on the problematic element.

Failure: lighting or shadows look unnatural
Cause: large edits (background swap or major relighting) can create mismatches. Fixes: ask the model to match “directional light from top-left, soft shadows” or provide the desired lighting reference image.