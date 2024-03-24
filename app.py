from flask import Flask, render_template
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
# Imported the create_database function from database.py
from database import create_database

app = Flask(__name__)

# Function to connect to the database
#This function connect_to_database takes the name of the SQLite database file as input, connects to the database, and returns the connection object.
def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    return conn

# Function to check for low stock items and expiring items
#This function check_items takes the database connection object as input.
#It fetches items that have a quantity less than 10 (low stock) and items that have an expiry date within the next 7 days (expiring items)
def check_items(conn):
    cursor = conn.cursor()

    # Check for low stock items
    cursor.execute("SELECT * FROM items WHERE quantity < ?", (10,))
    low_stock_items = cursor.fetchall()

    # Check for expiring items within 7 days
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=7)
    cursor.execute("SELECT * FROM items WHERE expiry_date <= ?", (expiry_date,))
    expiring_items = cursor.fetchall()

    return low_stock_items, expiring_items

# Function to send email notification
#This function send_email_notification sends an email notification.
#It takes the sender's email, sender's password, receiver's email, email subject, and email body as input.
#It creates an email message with the provided information, connects to the SMTP server, logs in with the sender's email and password, sends the email, and closes the connection.
def send_email_notification(sender_email, sender_password, receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

# Route to display notifications
@app.route('/')
    #This is the main function of the program.
    #It connects to the database, checks for low stock and expiring items, closes the database connection, and then sends email notifications if there are any low stock or expiring items.
def display_notifications():
    # Connect to the database
    conn = connect_to_database('inventory.db')

    # Check for low stock and expiring items
    low_stock_items, expiring_items = check_items(conn)

    # Close database connection
    conn.close()

    # Send notifications
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_password'
    receiver_email = 'recipient_email@gmail.com'

    if low_stock_items:
        subject = 'Low Stock Alert'
        body = 'The following items are running low in stock:\n\n'
        for item in low_stock_items:
            body += f"Item ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}\n"
        send_email_notification(sender_email, sender_password, receiver_email, subject, body)

    if expiring_items:
        subject = 'Expiring Items Alert'
        body = 'The following items are expiring within 7 days:\n\n'
        for item in expiring_items:
            body += f"Item ID: {item[0]}, Name: {item[1]}, Expiry Date: {item[3]}\n"
        send_email_notification(sender_email, sender_password, receiver_email, subject, body)

    return render_template('notifications.html')

if __name__ == "__main__":
    # Call the create_database function when the application is run
    create_database('inventory.db')
    app.run(debug=True)
