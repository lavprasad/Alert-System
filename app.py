from flask import Flask, render_template
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to connect to the database
def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    return conn

# Function to check for low stock items and expiring items
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
    app.run(debug=True)
