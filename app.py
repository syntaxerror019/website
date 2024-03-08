from flask import Flask, render_template, request
from wordbot import other_blueprint
from mbta_server import mbta_blueprint
from headlines import news_blueprint
from ai import ai_blueprint

from datetime import datetime

app = Flask(__name__)

def is_returning_user(ip_address):
    # Check if the IP address exists in the file
    with open('user_log.txt', 'r') as file:
        return ip_address in file.read()

def log_user(ip_address, user_agent, date, returning_user):
    # Log user information to the file
    with open('user_log.txt', 'a') as file:
        file.write(f"IP Address: {ip_address}\n")
        file.write(f"User Agent: {user_agent}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Returning User: {returning_user}\n")
        file.write("="*30 + "\n")
        
def new_user(ip_address, user_agent, date):
    # Log user information to the file
    with open('new_user_log.txt', 'a') as file:
        file.write(f"IP Address: {ip_address}\n")
        file.write(f"User Agent: {user_agent}\n")
        file.write(f"Date: {date}\n")
        file.write("="*30 + "\n")

        
JS_CODE = """
<script>
    // JavaScript code for IP logging
    fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {
            var ip = data.ip;
            console.log('Your IP address is:', ip);
            // Send the IP address and user agent to the Flask endpoint
            sendClientData(ip, navigator.userAgent);
        })
        .catch(error => {
            console.error('Error fetching IP address:', error);
        });

    // Function to send the client's IP address and user agent to the Flask endpoint
    function sendClientData(ip, userAgent) {
        fetch('/save-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip: ip, userAgent: userAgent }),
        })
        .then(response => {
            if (response.ok) {
                console.log('Client data sent successfully');
            } else {
                console.error('Failed to send client data');
            }
        })
        .catch(error => {
            console.error('Error sending client data:', error);
        });
    }
</script>
"""

@app.after_request
def add_ip_logging_js(response):
    # Check if the response content type is HTML
    if response.content_type.startswith('text/html'):
        # Inject the JavaScript code into the HTML response
        response.data = response.get_data(as_text=True).replace('</body>', f'{JS_CODE}</body>')
        return response
    return response

        
        
@app.before_request
def before_request_func():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
          

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.get_json()
    ip_address = data['ip']
    user_agent = data['userAgent']
    # Do something with the client's IP address and user agent (e.g., log them)
    if "python" in str(user_agent) or "robot" in str(user_agent):
        return #its the ping bot and shit
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    returning_user = is_returning_user(ip_address)
    
    if not returning_user:
        new_user(ip_address, user_agent, date)

    log_user(ip_address, user_agent, date, returning_user)  
    return 'Success' 
   
# Main route
@app.route('/')
def index():
    return render_template('index.html')

# Register the updated blueprint with multiple routes
app.register_blueprint(other_blueprint, url_prefix='/wordbot')
app.register_blueprint(mbta_blueprint, url_prefix='/mbta')
app.register_blueprint(news_blueprint, url_prefix='/news')
app.register_blueprint(ai_blueprint, url_prefix='/ai')

app.run(host='0.0.0.0', port=1775)