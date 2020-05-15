FROM python:3.7

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY job_progress_histogram.py .
COPY args.py .
COPY s3.py .

EXPOSE 5006
CMD bokeh serve --allow-websocket-origin='*'  job_progress_barchart.py
