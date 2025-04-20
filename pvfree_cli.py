import csv
import requests
import threading
import queue
import sys
import logging
import urllib
import datetime

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG) 

# Create a queue to store the status codes and reasons
STATUS_QUEUE = queue.Queue()


def push_record_to_api(row, api_url, headers, status_queue):
    response = requests.post(api_url, json=row, headers=headers)
    status_queue.put((response.status_code, response.reason))


def push_records_to_api(csvfile, api_url, model, user, headers, status_queue):
    failures = []
    reader = csv.DictReader(csvfile)
    # skip units header and the sandia header
    next(reader)
    next(reader)
    threads = []
    for row in reader:
        if model == 'cecmodule':
            row = cecmodule_handler(row)
        if 'error' in row:
            failures.append(row)
            continue
        row['created_by'] = user
        row['modified_by'] = user
        thread = threading.Thread(
            target=push_record_to_api,
            args=(row, api_url, headers, status_queue))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    return failures


def cecmodule_handler(kwargs):

    # handle BIPV
    bipv = kwargs['BIPV'] == 'Y'
    kwargs['BIPV'] = bipv
    LOGGER.debug('BIPV = %r', bipv)

    # handle date
    timestamp = kwargs['Date']
    try:
        timestamp = datetime.strptime(timestamp, '%m/%d/%Y')
    except (ValueError, TypeError) as exc:
        LOGGER.exception(exc)
        return {'error': 'date error', 'exc_info': exc, 'data': kwargs}
    kwargs['Date'] = datetime.strftime(timestamp, '%Y-%m-%d')
    LOGGER.debug('Date = %s', timestamp.isoformat())

    # handle Length and Width
    if not kwargs['Length']:
        kwargs['Length'] = None
    if not kwargs['Width']:
        kwargs['Width'] = None

    return kwargs

if __name__ == "__main__":
    if len(sys.argv) < 6:
        LOGGER.error('insufficient args: pass username,'
                     ' api_key, api_url, model, & csv_file_path.')
        sys.exit(1)
    LOGGER.info('running script: %s', sys.argv[0])
    username = sys.argv[1]  # mikofski
    api_key = sys.argv[2]
    api_base = sys.argv[3]  # "http://127.0.0.1:8000"
    model = sys.argv[4]  # cecmodule --> /api/v1/cecmodule/
    csv_file_path = sys.argv[5]  # "deploy/libraries/CEC Modules.csv"

    try:
        schema = requests.get(urllib.parse.urljoin(api_base, '/api/v1'))
        schema = schema.json()
    except Exception as exc_info:
        LOGGER.error('api_base not found on server or response not JSON')
        LOGGER.exception(exc_info=exc_info)
        sys.exit(2)

    try:
        model_schema = schema[model]
    except KeyError as exc_info:
        LOGGER.error('model must be in [cecmodule, pvinverter, pvmodule]')
        LOGGER.exception(exc_info=exc_info)
        sys.exit(3)
    api_url = urllib.parse.urljoin(api_base, model_schema['list_endpoint'])

    try:
        users = requests.get(
            urllib.parse.urljoin(api_base, '/api/v1/user'),
            params={'username': username})
        users = users.json()
    except Exception as exc_info:
        LOGGER.error("username was not found on the server or response not JSON")
        LOGGER.exception(exc_info=exc_info)
        sys.exit(4)
    else:
        user = users['objects'][-1]['resource_uri']
    headers = {
        "Authorization": f"ApiKey {username}:{api_key}",
        "Content-Type": "application/json"
    }

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            failures = push_records_to_api(
                csvfile, api_url, model, user, headers, STATUS_QUEUE)
    except Exception as exc_info:
        LOGGER.error("maybe the file wasn't found or something else bad?")
        LOGGER.exception(exc_info=exc_info)
        sys.exit(5)
    else:
        LOGGER.info(failures)

    # Process the queue after all threads have finished
    while not STATUS_QUEUE.empty():
        status_code, reason = STATUS_QUEUE.get()
        LOGGER.info(f"Status code: {status_code}, Reason: {reason}")
    sys.exit(0)
