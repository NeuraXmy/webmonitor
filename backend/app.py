from webmonitor import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(port=23456, host='0.0.0.0', use_reloader=False)