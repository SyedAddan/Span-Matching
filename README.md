# Span Matching

This .py file helps you find messy spans in a string and find their starting and ending indices.

## Usage

**Original String:** "I am a good student and I am a good person."
**Messy Span:** "god sudent and i am a g peron"

```python
from spanner import span_matching

original_string = "I am a good student and I am a good person."
messy_span = "god sudent and i am a g peron"
span_matching(original_string, messy_span)
```

**Output:**

```python
(7, 'good student and I am a good person.', 7, 43)
```

where: (edit_distance, matched_span, start_index, end_index)
