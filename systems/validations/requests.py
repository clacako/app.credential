from requests import request


def is_ajax_request(request):
    if request == "XMLHttpRequest":
        return True
    
    return False