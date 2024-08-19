# Spanner

Spanner allows you to match a messy span to the original string and expand the span to the original string. It uses the Levenshtein distance to match the span.

## Usage

**Original String:** "I can tell you my qualities. I am a good student and I am a good person. Although people maybe not see me as such"
**Messy Span:** "god sudent and i am a g peron"

### Match Span

```python
from spanner import span_matching

original_string = "I can tell you my qualities. I am a good student and I am a good person. Although people maybe not see me as such"
messy_span = "god sudent and i am a g peron"
span_matching(original_string, messy_span)
```

**Output:**

```python
(7, 'good student and I am a good person.', 36, 73)
```

where: (edit_distance, matched_span, matched_span_start_index, matched_span_end_index)

### Expand Span

```python
from spanner import expand_span

original_string = "I can tell you my qualities. I am a good student and I am a good person. Although people maybe not see me as such"
matched_span_start_index = 7
matched_span_end_index = 43
expand_span(original_string, matched_span_start_index, matched_span_end_index)
```

**Output:**

```python
('I am a good student and I am a good person.', 29, 72)
```

where: (expanded_span, expanded_span_start_index, expanded_span_end_index)

## Applications

- Named Entity Recognition
- Automatic Speech Recognition
- Speech to Text
