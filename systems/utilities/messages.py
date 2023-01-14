from django.utils.html import strip_tags, mark_safe

def errors_to_html(errors):
    error_list = []
    for key, value in errors.items():
        # error_list.append('<b>{}</b> :'.format(key.title()))
        error_list.append(f"<strong>{key.title().replace('_', ' ')}</strong>, {strip_tags(value)}")

    error_str = '<br />'.join(error_list)

    return error_str

def ajax_response(code, message, data=None, **kwargs):
    message = {
        "is_success"    : code,
        "message"       : message,
        "data"          : data,
        **kwargs
    }
    
    return message