from flask_apscheduler import APScheduler

scheduler = APScheduler()

def register_scheduler(app):
    global scheduler
    scheduler.init_app(app)
    scheduler.start()
    return scheduler