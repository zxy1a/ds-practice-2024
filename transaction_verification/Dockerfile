FROM python:3.11
WORKDIR /app
COPY ./transaction_verification/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install reloadium
EXPOSE 50052
CMD reloadium run "transaction_verification/src/app.py"