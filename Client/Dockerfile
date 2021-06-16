FROM base_image
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
ENV PYTHONPATH=/opt/liboqs-python
COPY app.py /
CMD ["python", "/app.py"]