from flask import Flask, request, jsonify
import logging
from validate import validate_phishing
from apscheduler.schedulers.background import BackgroundScheduler
from get_verify_list import get_verify_list
import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/check-url', methods=['GET'])
def check_url():
    app.logger.info('URL Checking Start')
    url_param = request.args.get('url')
    app.logger.info('URL: {}'.format(url_param))

    if url_param is None:
        app.logger.info('ERROR: No URL Param')
        return jsonify({"error": "Bad Request: URL param Required"}), 400

    is_phishing = validate_phishing(url_param)
    app.logger.info('Validation Done; {}'.format(is_phishing))
    return jsonify({"URL": url_param, "isPhishing": is_phishing})

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
