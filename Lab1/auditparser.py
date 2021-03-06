import re

regexes = {
  'open': re.compile('^[ \t]*<(item|custom_item|report|if|then|else|condition)[ \t>]'),
  'close': re.compile('^[ \t]*</(item|custom_item|report|if|then|else|condition)[ \t>]'),
  'info': re.compile('^[ \t]*(type|description|info|Note|Note #2|solution|reference|see_also|reg_option|value_type|value_data|reg_key|reg_item|check_type)[ \t]*:[ \t]*["\']*'),
}

def ParseAudit(content=None):
    global regexes
    lines = []
    audit = []
    stack = []

    if content is not None:
        lines = [l.strip() for l in content.split('\n')] 
        for n in range(len(lines)):
            if regexes['open'].match(lines[n]): 
                finds = regexes['open'].findall(lines[n])
                audit.append((n + 1, len(stack), lines[n]))
                stack.append(finds[0])
            elif regexes['close'].match(lines[n]): 
                finds = regexes['close'].findall(lines[n])
                audit.append((n + 1, len(stack), lines[n]))
                if len(stack) == 0:
                    msg = 'Ran out of stack closing tag: {} (line {})'
                    display(msg.format(finds[0], n), exit=1)
                elif finds[0] == stack[-1]:
                    stack = stack[:-1]
                else:
                    msg = 'Unbalanced tag: {} - {} (line {})'
                    display(msg.format(stack[-1], finds[0], n), exit=2)
            elif regexes['info'].match(lines[n]): 
                audit.append((n + 1, len(stack), lines[n]))

    return audit