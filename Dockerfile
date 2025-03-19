FROM python:3.10

COPY ./ /app

WORKDIR /app

EXPOSE 8501

RUN pip install -r requirements.txt

CMD ["python", "-m","streamlit","run","run_streamlit.py"]