"""
eval(expression[, globals[, locals]])
    If provided, globals must be a dictionary. If provided, locals can be any mapping object.
"""


def eval_with_context(expression, context=None):
    global_dict = __builtins__
    if context:
        return eval(expression, global_dict, context)
    else:
        return eval(expression, global_dict)
