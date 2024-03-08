# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response, request, abort, jsonify, Blueprint
import threading, os, requests, time, json
from datetime import datetime

other_blueprint = Blueprint('other', __name__)

active_bots = {}  # Dictionary to store information about active bots

running_en = False
current_room_en = ""
peers_en = 0
ping_time_en = 0

running_fr = False
current_room_fr = ""
peers_fr = 0
ping_time_fr = 0

running_br = False
current_room_br = ""
peers_br = 0
ping_time_br = 0

script = ""

running = False

@other_blueprint.errorhandler(404)
def page_not_found(error):
  return render_template('wordbot/404.html'), 404

@other_blueprint.route('/status', methods=['POST'])
def receive_status():
    data = request.json
    room_code = data.get('roomCode')
    language = data.get('language')
    count = data.get('count')
    is_main = data.get('isMain')
    is_public = data.get('isPublic')
    print("publihclihc", is_public)

    # Update last ping time for the bot
    active_bots[room_code] = {'language': language, 'count': count,
                              'is_main': is_main, 'last_ping_time': time.time(), 'is_public': is_public}

    return jsonify({'message': 'Status received successfully.'})


@other_blueprint.route('/live')
def show_status():
    return render_template('wordbot/status.html', bots=active_bots)


@other_blueprint.route("/ping")
def ping():
  global running_en, current_room_en, peers_en, ping_time_en
  global running_fr, current_room_fr, peers_fr, ping_time_fr
  global running_br, current_room_br, peers_br, ping_time_br

  source = request.args.get('src')
  if source == "en":
    current_room_en = request.args.get('code')
    peers_en = request.args.get('peers')
    ping_time_en = time.time()
    running_en = True
    print("ping from EN")
  if source == "fr":
    current_room_fr = request.args.get('code')
    peers_fr = request.args.get('peers')
    ping_time_fr = time.time()
    running_fr = True
    print("ping from FR")
  if source == "br":
    current_room_br = request.args.get('code')
    peers_br = request.args.get('peers')
    ping_time_br = time.time()
    running_br = True
    print("ping from BR")

  return Response(status=200)

@other_blueprint.route("/records")
def records():
  return render_template("wordbot/notyet.html")


@other_blueprint.route("/changelog")
def changelog():
  return render_template("wordbot/changelog.html")


@other_blueprint.route("/configure")
def conf():
  return render_template("wordbot/notyet.html")


@other_blueprint.route("/dev")
def dev():
  return render_template("wordbot/notyet.html")


@other_blueprint.route("/about")
def about():
  return render_template("wordbot/about.html")


@other_blueprint.route("/up_en")
def running_en():
  if running_en:
    return jsonify([{"code": current_room_en, "peers": peers_en}])
  else:
    return abort(403)


@other_blueprint.route("/")
def index():
  #client_ip = request.headers['X-Forwarded-For']
  current_time = datetime.now()
  formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

  if running_en or running_br or running_fr:
    return render_template("wordbot/index.html", live_data=script, bots=active_bots)
  return render_template("wordbot/down.html")


def loop():

  global script, running_en, running_fr, running_br, running
  while True:
        
    current_time = time.time()
    for room_code, bot_info in list(active_bots.items()):
            last_ping_time = bot_info['last_ping_time']
            # Bot hasn't pinged for 60 seconds (adjust as needed)
            if current_time - last_ping_time > 60:
                del active_bots[room_code]  # Remove the dead bot
        
    time.sleep(5)
    if (time.time() - ping_time_en
        ) * 1000 > 60000:  #if it has been 30 seconds, infer bot is down
      running_en = False
   
    if (time.time() - ping_time_fr
        ) * 1000 > 60000:  #if it has been 30 seconds, infer bot is down
      running_fr = False
     
    if (time.time() - ping_time_br
        ) * 1000 > 60000:  #if it has been 30 seconds, infer bot is down
      running_br = False
      
    script = ""
    if running_en:
      script += u'WordBot ⚡ English is up and running at <a href="https://jklm.fun/'+current_room_en+'" target="_blank">https://jklm.fun/'+current_room_en+'</a> with ' +peers_en+ ' person(s) playing.<br><br>'

    if running_fr:
      script += u'WordBot ⚡ Français est opérationnel à l’adresse suivante <a href="https://jklm.fun/'+current_room_fr+'" target="_blank" >https://jklm.fun/'+current_room_fr+'</a> avec '+peers_fr+' personnes jouant<br><br>'

    if running_br:
      script += u'WordBot ⚡ Português está em funcionamento na <a href="https://jklm.fun/'+current_room_br+'" target="_blank" >https://jklm.fun/'+current_room_br+'</a> com '+peers_br+' pessoa jogando<br><br>'

    if not running_en and not running_br and not running_fr:
      running = False
    else:
      running = True


loop_thread = threading.Thread(target=loop)
loop_thread.start()



