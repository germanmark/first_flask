from flask import Flask, jsonify, request, Response
import json
import db_helpers

app = Flask(__name__)
app.debug = True

@app.route('/')
def homepage():
    print(request)
    # print(request.headers)
    print(request.args)
    print(request.args.get('var1'))
    print(request.args.get('var2'))
    return "Hello world"

@app.get('/api/users')
def users_get():
    # Some database operations that write to user_list
    params = request.args
    print("Arguments for the GET:" + str(params))
    user_id = params.get('userId')
    print(user_id)
    if user_id:
        query_result = db_helpers.run_query("SELECT id, username from user WHERE id=?",[user_id])
    else:
        query_result = db_helpers.run_query("SELECT id, username from user ORDER BY id ASC")
    people = []
    for person in query_result:
        people.append(person[1])
    # user_list = [
    #             {"id" : 1,
    #              "name" : "John",
    #              "age" : 20},
    #             {"id" : 2,
    #              "name" : "Jane",
    #              "age" : 21}
    #             ]
    # return Response(json.dumps(user_list, default=str), mimetype="application/json", status=200)
    # The above and below are equivalent
    resp = {"usernames" : people}
    return jsonify(resp), 200

@app.post('/api/users')
def users_post():
    user_data = request.json
    print(user_data)
    if not user_data.get('username'):
        return jsonify("Missing required field: username"), 422
    if not user_data.get('userAge'):
        return jsonify("Missing required field: userAge"), 422
    
    db_helpers.run_query("INSERT INTO user (username, age) VALUES(?,?)", 
                        [user_data.get('username'), user_data.get('userAge')])
    # Some database operations that create the user
    # More DB operations that generate a login token
    login_dictionary = {"loginToken" : "abc123"}
    # return Response(json.dumps(login_dictionary, default=str), mimetype="application/json", status=201)
    # Above and below are equivalent
    if login_dictionary['loginToken'] == "abc123":
        return jsonify(login_dictionary), 201
    else:
        return jsonify("There was an error"), 403
