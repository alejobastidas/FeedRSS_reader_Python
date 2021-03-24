from feed_reader import app
from feed_reader.routes import update
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(update, 'cron', hour='1', minute='30')
scheduler.start()


if __name__ == '__main__':
    app.run(debug=True)




