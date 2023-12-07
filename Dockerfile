FROM selenium/standalone-firefox
RUN  sudo apt-get update && sudo apt-get upgrade
RUN sudo apt-get install -y apt-utils wget pip git fish

RUN cd /home/seluser && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    sudo tar -xvzf geckodriver-v0.33.0-linux64.tar.gz && \
    sudo rm geckodriver-v0.33.0-linux64.tar.gz && \
    sudo mv geckodriver /usr/local/bin/ && \
    pip install --upgrade beautifulsoup4 selenium pyvirtualdisplay spintax && \
    git clone https://github.com/localhost-server/craigslist-poster.git /home/seluser/project && \
    sudo cp -r /usr/bin/python3 /usr/bin/python && \
    cd /home/seluser/project 

# # Make port 80 available to the world outside this container
EXPOSE 80

ENTRYPOINT ["python", "/home/seluser/project/main.py"]

