from typing import List


def extend_matches(groups: List[tuple]) -> List[tuple]:
    """Add new pairs based on existing ones"""
    # Collect all unique ids
    unique_ids = set()
    for x in groups:
        for y in x:
            unique_ids.add(y)

    # Create a dictionary of existing pairs
    pairs_dict = {x: {x} for x in unique_ids}
    for x in groups:
        for j in range(len(x)-1):
            united_pairs = pairs_dict[x[j]] | pairs_dict[x[j+1]]
            for z in united_pairs:
                pairs_dict[z].update(united_pairs)
    print(pairs_dict)
    # Create a list of new pairs

    new_pairs = [tuple(value) for value in pairs_dict.values()]

    # Drop self-pairs and duplicates
    new_pairs = {pair for pair in new_pairs if pair[0] < pair[1]}

    # Sort the list of new pairs
    new_pairs = sorted(new_pairs)

    return new_pairs
