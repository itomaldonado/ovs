# OVS
#
# Version       latest
FROM library/python:2.7.9

RUN mkdir /home/python

# Adding all files.
ADD requirements.txt /home/python/
ADD app.py /home/python/
ADD templates/ /home/python/

# Installing all requirements
RUN pip install -r /home/python/requirements.txt

# Exposing port 80
EXPOSE 80

# Entry point
WORKDIR /home/python
ENTRYPOINT ["python", "app.py"]