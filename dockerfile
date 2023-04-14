FROM python:3.11

#Set a directory for the app
WORKDIR /usr/src/app

#Copy all the files to the container
COPY . .

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Expose the port
EXPOSE 5000

#run the command
CMD [ "python", "app.py" ]