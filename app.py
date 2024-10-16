from flask import Flask, request, jsonify
import logging
from validate import validate_phishing, url_parser
from apscheduler.schedulers.background import BackgroundScheduler
from get_verify_list import get_verify_list
import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/python', methods=['POST'])
def check_url():
    app.logger.info('URL Checking Start')
    data = request.get_json()

    if data is None:
        app.logger.info('No Message provided')
        return jsonify({'error': 'Bad Request: No Message provided'}), 400

    message = data.get('message', 'nothing')
    url_params = url_parser(message)

    if url_params is None:
        app.logger.info('No URL provided')
        return jsonify({'error': 'Bad Request: No URL provided'}), 400

    phishing_count = 0
    for url in url_params:
        app.logger.info('URL: {}'.format(url))
        if validate_phishing(url):
            phishing_count += 1
            app.logger.info('isPhishing: True')
        else:
            app.logger.info('isPhishing: False')

    app.logger.info('Validation Done; {}'.format(phishing_count))
    
    is_phishing = False
    if phishing_count > 0:
        is_phishing = True
    return jsonify({'isPhishing': is_phishing}), 200

def scheduled_task():
    app.logger.info('작업이 실행되었습니다')
    status_code_str = get_verify_list()
    app.logger.info('status_codes: {}'.format(status_code_str))

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', days=1)
scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    print(f'Starting server on port {port}...')
