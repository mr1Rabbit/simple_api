from flask import Flask, jsonify, request

app = Flask(__name__)
health_status = True
key = "AbCdEf123456"


def results(name, age, hobby):
    return {"success": 1, "name": name, "age": age, "hobby": hobby}


@app.route('/api/simple/hello', methods=['GET'])
def helloworld():
    if (request.method == 'GET'):
        response = jsonify('Hello world!')
        response.status_code = 200
        return response


@app.route('/api/simple/student', methods=['GET'])
def student():
    name = request.args.get('name', "")
    age = request.args.get('age', "")
    hobby = request.args.get('hobby', "")
    if name == "" or hobby == "" or age == "":
        return jsonify({"success": 0, "result": {"error": "Error: Not all requered field provided. Please specify your name,age,and hobby."}})
    return jsonify(results(name, age, hobby))

# Explaining different status codes.


@app.route('/healthz')
def health():
    if health_status:
        resp = jsonify(health="healthy")
        resp.status_code = 200
    else:
        resp = jsonify(health="unhealthy")
        resp.status_code = 500

    return resp


@app.route('/admin')
def admin():
    profile = request.args.get('profile', "")
    if profile == "student":
        resp = jsonify("You are forbidden to access this route.")
        resp.status_code = 403
    else:
        resp = jsonify("You have control now.")
        resp.status_code = 200

    return resp


@app.route('/authorize')
def authorize():
    headers = Flask.request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    if token == key:
        resp = jsonify("You are Authorized to access this api.")
        resp.status_code = 200
        return resp
    resp = jsonify(
        "You are Unauthorized to access this api.please provide a valid token.")
    resp.status_code = 401
    return resp


if __name__ == '__main__':
    app.run(debug=True)
