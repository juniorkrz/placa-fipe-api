FROM python:alpine
WORKDIR /usr/scr/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]