FROM python:3.11
WORKDIR /app
# Add /app to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY ./transaction_verification/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install reloadium
EXPOSE 50054
CMD reloadium run "order_queue/src/app.py"