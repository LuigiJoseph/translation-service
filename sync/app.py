from restapi_server import app,api
# import restapi_server.route
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)