import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import config

def create_html_report(report_content: str, product_idea: str) -> str:
    """
    Converts the report content into a styled HTML file.
    
    Args:
        report_content: The string content of the report.
        product_idea: The product idea for the report title.

    Returns:
        The file path of the generated HTML report.
    """
    # Basic CSS for better readability
    html_style = """
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            max-width: 800px; 
            margin: 20px auto; 
            padding: 20px; 
            border: 1px solid #ddd; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 10px; }
        h2 { color: #333; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 25px; }
        pre, code { background-color: #f4f4f4; padding: 5px; border-radius: 4px; font-family: 'Courier New', Courier, monospace; }
        strong { color: #000; }
        li { margin-bottom: 10px; }
    </style>
    """
    
    # Simple conversion from Markdown-like text to HTML
    html_content = report_content.replace("\n\n", "<p>")
    html_content = html_content.replace("\n", "<br>")
    html_content = html_content.replace("## ", "<h2>").replace("</h2><br>", "</h2>")
    html_content = html_content.replace("# ", "<h1>").replace("</h1><br>", "</h1>")
    
    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Product Research Report: {product_idea}</title>
        {html_style}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    file_path = "product_research_report.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_body)
        
    print(f"Report successfully generated at: {file_path}")
    return file_path

def send_report_by_email(file_path: str, product_idea: str):
    """
    Sends the generated report file as an email attachment.
    
    Args:
        file_path: The path to the report file to attach.
        product_idea: The product idea for the email subject.
    """
    if not all([config.SENDER_EMAIL, config.SENDER_PASSWORD, config.RECIPIENT_EMAIL]):
        print("Email configuration is incomplete. Skipping email dispatch.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = config.SENDER_EMAIL
        msg['To'] = config.RECIPIENT_EMAIL
        msg['Subject'] = f"AI Product Research Report: {product_idea}"

        body = f"Please find the attached research report for the product idea: '{product_idea}'."
        msg.attach(MIMEText(body, 'plain'))

        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {file_path}")
        msg.attach(part)

        # Using Gmail's SMTP server as an example
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(config.SENDER_EMAIL, config.RECIPIENT_EMAIL, text)
        server.quit()
        
        print(f"Report successfully sent to {config.RECIPIENT_EMAIL}")

    except Exception as e:
        print(f"Error sending email: {e}")