FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install -y python python-ensurepip
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash
RUN apt-get install -y nodejs
COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt
COPY . .

RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install 
COPY . .
EXPOSE 8080

CMD ["node", "bin/www"]

# RUN pip install pandas
# RUN pip install numpy
# RUN pip install scikit-learn==1.2.2
# RUN pip install matplotlib
# RUN pip install seaborn
# RUN pip install sastrawi
# RUN pip install nltk
# RUN pip install scikit-multilearn
# RUN python -m nltk.downloader stopwords
# RUN python -m nltk.downloader punkt




