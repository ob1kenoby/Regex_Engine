import sys
sys.setrecursionlimit(10000)


def split_strings(string, index):
    return make_short_string(string, index), make_long_string(string, index)


def make_short_string(string, index):
    return string[:index - 1] + string[index + 1:]  # string without the wildcard and the preceding character


def make_long_string(string, index):
    return string[:index] + string[index + 1:]  # string without the wildcard, but with the preceding character


def process_question_mark(pattern, string):
    if pattern.find('?') == -1:
        return process_asterisk(pattern, string)
    index = pattern.find('?')
    pattern_short, pattern_long = split_strings(pattern, index)
    return process_question_mark(pattern_short, string) or process_question_mark(pattern_long, string)


def process_asterisk(pattern, string):
    wildcard_index = pattern.find('*')
    if wildcard_index == -1:
        return process_plus(pattern, string)
    str_index = string.find(pattern[wildcard_index - 1])
    if str_index == -1:
        new_pattern = make_short_string(pattern, wildcard_index)  # remove unnecessary wildcard
        return process_plus(new_pattern, string)
    string_short, string_long = split_strings(string, str_index)
    return process_asterisk(pattern, string_short) or process_asterisk(pattern, string_long)


def process_plus(pattern, string):
    wildcard_index = pattern.find('+')
    if wildcard_index == -1:
        return check_length(pattern, string)
    if pattern[wildcard_index - 1] == '.':
        for letter in ''.join(set(string)):
            new_pattern = pattern[:wildcard_index - 1] + letter + pattern[wildcard_index:]
            found_match = process_plus(new_pattern, string)
            """
            found_match is needed to filter wrong patterns that appear in the loop.
            Examples:
                Original input:
                    n.+pe|noooope
                Pattern variants that are sent to recursion and their outcome:
                    nn+pe   False   will not return that
                    no+pe   True    will return that
                    np+pe           will not get to that
                    ne+pe           will not get to that    """
            if found_match:
                return found_match
    first_index = string.find(pattern[wildcard_index - 1])
    if first_index != -1:
        second_index = string.find(pattern[wildcard_index - 1], first_index + 1)
        if second_index != -1:
            string_long = make_long_string(string, first_index)
            return process_plus(pattern, string_long)
    regex_long = make_long_string(pattern, wildcard_index)
    return check_length(regex_long, string)


def check_length(pattern, string):
    if len(pattern) > 0:
        return check_anchors(pattern, string)
    return True


def count_backslashes(pattern):
    backslash_count = 0
    backslash = -1
    for i in range(len(pattern)):
        backslash = pattern.find('\\', backslash + 1)
        if backslash == -1:
            break
        else:
            backslash_count += 1
    return backslash_count


def check_anchors(pattern, string):
    backslashes = count_backslashes(pattern)
    if pattern[0] == '^' and pattern[-1] == '$':
        if len(pattern) - 2 == len(string):
            return regex_comparison(pattern[1:-1], string)
        return False
    elif pattern[0] == '^':
        return regex_comparison(pattern[1:], string)
    elif pattern[-1] == '$' and len(pattern) - 1 <= len(string):
        return regex_comparison(pattern[:-1], string[-(len(pattern[:-1])-backslashes):])
    return look_for_start(pattern, string)


def look_for_start(pattern, string):
    if regex_comparison(pattern, string):
        return True
    if len(string) >= len(pattern):
        return look_for_start(pattern, string[1:])
    return False


def regex_comparison(pattern, string):
    if len(pattern) == 0:
        return True
    elif len(pattern) > 0 and len(string) == 0:
        return False
    elif pattern[0] == '\\' and len(pattern) > 1:
        if pattern[1] == string[0]:
            return regex_comparison(pattern[2:], string[1:])
    elif pattern[0] == string[0] or pattern[0] == '.':
        return regex_comparison(pattern[1:], string[1:])
    return False


print(process_question_mark(*input().split('|')))
