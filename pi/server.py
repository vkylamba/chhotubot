import time
from flask import Flask, render_template, Response
import threading
from camera import Camera
from car import Car
car = Car()
commands = []

# Flask app
app = Flask(__name__)


def gen(camera):
    global commands
    while True:
        frame, data = camera.get_frame()
        status, command = car.get_commands(data)
        if status:
            commands.extend(command)
        else:
            commands = command
        if frame is None:
            frame = b''
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    camera = Camera()
    data = gen(camera)
    return Response(data, mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route("/target")
# def hello():
#     x = request.args['x']
#     y = request.args['y']
#     return "Hello World!"


def run_flask():
    app.run(host='0.0.0.0', debug=True, threaded=True)


def control_car():
    while True:
        if isinstance(commands, list) and len(commands) > 0:
            command = commands.pop(0)
            print("sending command", command)
            car.send_command(command)
            time.sleep(1)


if __name__ == '__main__':
    # t1 = threading.Thread(target=run_flask)
    t2 = threading.Thread(target=control_car)
    t2.start()
    app.run(host='0.0.0.0', debug=True, threaded=True)
    t2.join()
    # starting thread 1
    # t1.start()
    # starting thread 2

    # wait until thread 1 is completely executed
    # t1.join()
    # wait until thread 2 is completely executed
