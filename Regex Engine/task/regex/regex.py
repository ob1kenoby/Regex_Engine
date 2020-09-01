import sys
sys.setrecursionlimit(100000)


def split_strings(string, pattern):
    return make_short_string(string, pattern), make_long_string(string, pattern)


def make_short_string(pattern, index):
    return pattern[:index - 1] + pattern[index + 1:]


def make_long_string(pattern, index):
    return pattern[:index] + pattern[index + 1:]


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
    elif pattern[0] == string[0] or pattern[0] == '.':
        return regex_comparison(pattern[1:], string[1:])
    return False


def check_anchors(pattern, string):
    if pattern[0] == '^' and pattern[-1] == '$':
        if len(pattern) - 2 == len(string):
            return regex_comparison(pattern[1:-1], string)
        else:
            return False
    elif pattern[0] == '^':
        return regex_comparison(pattern[1:], string)
    elif pattern[-1] == '$' and len(pattern) - 1 <= len(string):
        return regex_comparison(pattern[:-1], string[-len(pattern[:-1]):])
    else:
        return look_for_start(pattern, string)


def check_length(pattern, string):
    if len(pattern) > 0:
        return check_anchors(pattern, string)
    return True


def process_asterisk(pattern, string):
    wildcard_index = pattern.find('*')
    if wildcard_index == -1:
        return check_length(pattern, string)
    wildcard_symbol = pattern[wildcard_index - 1]
    string_index = string.find(wildcard_symbol)
    if string_index == -1:
        pattern = make_short_string(pattern, wildcard_index)
        return check_length(pattern, string)
    string_short, string_long = split_strings(string, string_index)
    return process_asterisk(pattern, string_short) or process_asterisk(pattern, string_long)


def process_plus(pattern, string):
    wildcard_index = pattern.find('+')
    if wildcard_index == -1:
        return process_asterisk(pattern, string)
    wildcard_symbol = pattern[wildcard_index - 1]
    new_pattern = pattern[:wildcard_index] + wildcard_symbol + '*' + pattern[wildcard_index + 1:]
    return process_plus(new_pattern, string)


def process_question_mark(pattern, string):
    wildcard_index = pattern.find('?')
    if wildcard_index == -1:
        return process_plus(pattern, string)
    pattern_short, pattern_long = split_strings(pattern, wildcard_index)
    return process_question_mark(pattern_short, string) or process_question_mark(pattern_long, string)


print(process_question_mark(*input().split('|')))
