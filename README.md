# Email Scheduler Service

Standalone FastAPI service for scheduling and sending bulk emails. 

Stack: FastAPI + CronJob + Postgresql

## Features
- Schedule emails for future delivery
- Cancel scheduled emails
- Retry failed emails automatically
- RESTful API for integration with FastAPI
- PostgreSQL database for reliability

## Deployment

1. Deploy to Render: `render.yaml` included
2. Set up cron-job.org to ping `/trigger-email-check` every 5 minutes
3. Connect your Streamlit app to the scheduler API

## API Documentation

Once deployed, visit `/docs` for interactive API documentation.


- source venv/bin/activate
- python install -r requirements.txt

### RUN
- uvicorn app.main:app --host 0.0.0.0 --port $PORT