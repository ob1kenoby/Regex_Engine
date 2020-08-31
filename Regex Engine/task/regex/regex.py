import sys
sys.setrecursionlimit(10000)


def split_strings(string, index):
    return make_short_string(string, index), make_long_string(string, index)


def make_short_string(string, index):
    return string[:index - 1] + string[index + 1:]


def make_long_string(string, index):
    return string[:index] + string[index + 1:]


def process_question_mark(regex, string):
    if regex.find('?') == -1:
        return process_asterisk(regex, string)
    index = regex.find('?')
    regex_short, regex_long = split_strings(regex, index)
    return process_question_mark(regex_short, string) or process_question_mark(regex_long, string)


def process_asterisk(regex, string):
    reg_index = regex.find('*')
    if reg_index == -1:
        return process_plus(regex, string)
    str_index = string.find(regex[reg_index - 1])
    if str_index == -1:
        regex = make_short_string(regex, reg_index)
        return process_plus(regex, string)
    string_short, string_long = split_strings(string, str_index)
    return process_asterisk(regex, string_short) or process_asterisk(regex, string_long)


def process_plus(regex, string):
    reg_index = regex.find('+')
    if reg_index == -1:
        return check_length(regex, string)
    if regex[reg_index - 1] == '.':
        found_match = False
        for letter in ''.join(set(string)):
            found_match = process_plus(regex[reg_index - 2] + letter + regex[reg_index - 1], string)
            if found_match:
                return found_match
    str_index = string.find(regex[reg_index - 1])
    occurrences = [str_index]
    while str_index != -1:
        str_index = string.find(regex[reg_index - 1], str_index + 1)
        if str_index != -1:
            occurrences.append(str_index)
        if len(occurrences) > 1:
            break
    if len(occurrences) == 1:
        regex_long = make_long_string(regex, reg_index)
        return check_length(regex_long, string)
    string_long = make_long_string(string, occurrences[0])
    return process_plus(regex, string_long)


def look_for_start(regex, string):
    if regex_comparison(regex, string):
        return True
    if len(string) >= len(regex):
        return look_for_start(regex, string[1:])
    return False


def regex_comparison(regex, string):
    if len(regex) == 0:
        return True
    elif len(regex) > 0 and len(string) == 0:
        return False
    elif regex[0] == string[0] or regex[0] == '.':
        return regex_comparison(regex[1:], string[1:])
    return False


def check_anchors(regex, string):
    if regex[0] == '^' and regex[-1] == '$':
        if len(regex) - 2 == len(string):
            return regex_comparison(regex[1:-1], string)
        else:
            return False
    elif regex[0] == '^':
        return regex_comparison(regex[1:], string)
    elif regex[-1] == '$' and len(regex) - 1 <= len(string):
        return regex_comparison(regex[:-1], string[-len(regex[:-1]):])
    else:
        return look_for_start(regex, string)


def check_length(regex, string):
    if len(regex) > 0:
        return check_anchors(regex, string)
    return True


def check_metacharacters(regex, string):
    for case in ['?', '*', '+']:
        reg_index = regex.find[case]
        if reg_index != -1:
            str_index = string.find(regex[reg_index - 1])
            if str_index != -1:
                if case == '?':
                    regex, string = process_question_mark(regex, string)
                elif case == '*':
                    regex, string = process_asterisk(regex, string)
                elif case == '+':
                    regex, string = process_plus(regex, string)


print(process_question_mark(*input().split('|')))
