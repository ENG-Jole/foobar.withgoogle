def solution(input_list, target_value):
    # Easiest just to iterate through the entire list
    # Since generating the list of all strict partitions for
    # target_value greater than 50 is very very very slow
    # even with caching.
    # Otherwise I would have got all the strict partitions for
    # a target value and then match them with the input_list
    # and if there was no match, return [-1,-1].
    # Instead I just took advantage of enumerate and Python's fairly optimal
    # for loops to iterate through each possiblity
    for start_key, start_value in enumerate(input_list):
        for end_key, end_value in enumerate(input_list):
            range = input_list[start_key:end_key + 1]
            if sum(range) == target_value:
                return [start_key, end_key]

    no_partition = [-1, -1]
    return no_partition
