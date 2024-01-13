FROM python:alpine
RUN pip install "uvicorn[standard]" fastapi bs4 unidecode tokens requests
WORKDIR /usr/scr/app
COPY . .
EXPOSE 8000
ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]