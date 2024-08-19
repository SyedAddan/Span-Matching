import jellyfish
from typing import Optional

def span_matching(review: str, span: str, method: str = "lev", log: bool = False) -> tuple[int, str, int, int]:
    review_words = review.split(" ")
    span_words = span.split(" ")
    
    len_review = len(review)
    len_review_words = len(review_words)
    len_span = len(span)
    len_span_words = len(span_words)
    
    min_distance = float('inf')
    min_span_start = 0
    min_span_end = len_review
    
    if log:
        print(f"Review: {review}")
        print(f"Span: {span}")
    
    if method == "lev":
        span_method = jellyfish.levenshtein_distance
    elif method == "dam":
        span_method = jellyfish.damerau_levenshtein_distance
    elif method == "ham":
        span_method = jellyfish.hamming_distance
    else:
        span_method = jellyfish.levenshtein_distance
    
    # 1st Pass
    if log:
        print("1st Pass")
        print("Word by Word Window Matching!")
        print()
    for i in range(len_review_words - len_span_words + 1):
        review_span = " ".join(review_words[i:i + len_span_words])
        current_distance = span_method(span.lower(), review_span.lower())
        if log:
            print(f"Review Span: {review_span}, Distance: {current_distance}")
        if current_distance < min_distance:
            if log:
                print(f"New Min Distance: {current_distance}")
            min_distance = current_distance
            min_span_start = review.find(review_span)
            min_span_end = min_span_start + len(review_span)

    # 2nd Pass
    if log:
        print()
        print()
        print("2nd Pass")
        print("Trailing and Leading Character by Character Window Matching!")
        print()
    characters_to_check = int(len_span / 4)
    
    # Trailing characters check
    if log:
        print("Trailing Characters Check")
        print()
    for i in range(characters_to_check):
        review_span = review[max(0, min_span_start - i - 1):min_span_end - i - 1]
        current_distance = span_method(span.lower(), review_span.lower())
        if log:
            print(f"Review Span: {review_span}, Distance: {current_distance}")
        if current_distance < min_distance:
            if log:
                print(f"New Min Distance: {current_distance}")
            min_distance = current_distance
            min_span_start = max(0, min_span_start - i - 1)
            min_span_end = min_span_end - i - 1

    # Leading characters check
    if log:
        print()
        print("Leading Characters Check")
        print()
    for i in range(characters_to_check):
        review_span = review[min_span_start + i:min(min_span_end + i, len_review)]
        current_distance = span_method(span.lower(), review_span.lower())
        if log:
            print(f"Review Span: {review_span}, Distance: {current_distance}")
        if current_distance < min_distance:
            if log:
                print(f"New Min Distance: {current_distance}")
            min_distance = current_distance
            min_span_start = min_span_start + i
            min_span_end = min(min_span_end + i, len_review)

    # 3rd Pass
    if log:
        print()
        print()
        print("3rd Pass")
        print("Avoiding word cutting by checking for the closest space character from the start and end of the span!")
        print()
    
    # Starting character check
    if log:
        print("Starting Character Check")
        print()
    while min_span_start > 0 and review[min_span_start - 1] != " ":
        min_span_start -= 1
    if log:
        print(f"Span: {review[min_span_start:min_span_end]}")
    
    # Ending character check
    if log:
        print()
        print("Ending Character Check")
        print()
    while min_span_end < len_review and review[min_span_end] != " ":
        min_span_end += 1
    if min_span_end < len_review:
        min_span_end += 1  # Move to the end of the word
    if log:
        print(f"Span: {review[min_span_start:min_span_end]}")
    
    return min_distance, review[min_span_start:min_span_end].strip(), min_span_start, min_span_end

def expand_span(review: str, start_idx: int, end_idx: int, version: int = 1, max_additional_words: int = 10, log: bool = False) -> Optional[str | tuple[str, int, int]]:
    if version == 1: 
        # Define stopping points
        stopping_points = {'.', '!', '?', ';', '\n'}
        
        # Split review into words and spaces to handle word boundaries
        words = review.split(" ")
        total_word_count = len(words)
        
        if log:
            print(f"Words: {words}")
            print(f"Total word count: {total_word_count}")
        
        # Find the word index of the start and end positions
        char_count = 0
        word_start_idx = word_end_idx = 0
        for i, word in enumerate(words):
            char_count += len(word)
            if char_count >= start_idx and word_start_idx == 0:
                word_start_idx = i
            if char_count >= end_idx:
                word_end_idx = i - 1
                break
            char_count += 1

        if log:
            print(f"Word start index: {word_start_idx}")
            print(f"Word end index: {word_end_idx}")
            print(f"Span Starting word: {words[word_start_idx]}")
            print(f"Span Ending word: {words[word_end_idx]}")
        
        # Calculate the number of words to expand on both sides
        expansion_word_count = max(1, total_word_count // 4)
        if log:
            print(f"Exapnsion word count: {expansion_word_count}")

        # Initialize the new start and end indices
        new_word_start_idx = word_start_idx
        new_word_end_idx = word_end_idx

        # Expand backwards
        for _ in range(expansion_word_count):
            if new_word_start_idx == 0:
                if log:
                    print(f"Start of review reached!")
                break
            new_word_start_idx -= 1
            if log:
                print(f"Checking word: {words[new_word_start_idx]}")
            if any(p in words[new_word_start_idx] for p in stopping_points):
                new_word_start_idx += 1
                if log:
                    print(f"This word has a stopping point: {words[new_word_start_idx]}")
                break

        special_break = False
        
        if any(p in words[new_word_end_idx] for p in stopping_points):
            new_word_end_idx += 1
            special_break = True
        
        # Expand forwards
        for _ in range(expansion_word_count):
            if special_break:
                break
            if new_word_end_idx >= len(words) - 1:
                if log:
                    print(f"End of review reached!")
                break
            new_word_end_idx += 1
            if log:
                print(f"Checking word: {words[new_word_end_idx]}")
            if any(p in words[new_word_end_idx] for p in stopping_points):
                if log:
                    print(f"This word has a stopping point: {words[new_word_end_idx]}")
                new_word_end_idx += 1
                break
        if log:
            print(f"New word start index: {new_word_start_idx}")
            print(f"New word end index: {new_word_end_idx}")

        # Convert word indices back to character indices
        new_start_idx = sum(len(words[i]) + 1 for i in range(new_word_start_idx))
        new_end_idx = sum(len(words[i]) + 1 for i in range(new_word_end_idx)) - 1

        return review[new_start_idx: new_end_idx].strip(), new_start_idx, new_end_idx 
    elif version == 2:
        substring = review[start_idx:end_idx]
        # Find the starting index of the substring in the full string
        start_index = review.find(substring)
        if start_index == -1:
            return ""
        
        # Count the number of words in the substring
        words_in_substring = len(substring.split())

        # Initialize indices to expand the substring to full sentences
        left_index = start_index
        right_index = start_index + len(substring)
        
        # Expand to the left to the beginning of the sentence or the start of the string
        while left_index > 0 and review[left_index - 1] != '.':
            left_index -= 1
        
        # Expand to the right to the end of the sentence or the end of the string
        while right_index < len(review) and review[right_index] != '.':
            right_index += 1
        
        # Include the character right after the period to complete the sentence
        if right_index < len(review) and review[right_index] == '.':
            right_index += 1
        
        # Extract the context
        context = review[left_index:right_index].strip()
        words_in_context = len(context.split())
        
        # Ensure that the context does not exceed the substring length by more than 10 words
        if words_in_context > words_in_substring + max_additional_words:
            # Split the context into words and reconstruct to fit the word limit
            words_list = context.split()
            if words_in_substring + max_additional_words < len(words_list):
                end_index = words_in_substring + max_additional_words
                context = ' '.join(words_list[:end_index])
        
        return context