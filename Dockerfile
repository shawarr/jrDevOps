FROM python:3.14-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
#runs app with production server
CMD ["gunicorn", "--bind", "0.0.0.0:5000","--workers", "2" ,"app:app"]