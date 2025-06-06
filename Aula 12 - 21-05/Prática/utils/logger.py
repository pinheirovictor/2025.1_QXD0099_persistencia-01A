import logging

def log_request(request, response):
    logging.info(f"{request.method} {request.url} - Status: {response.status_code}")
