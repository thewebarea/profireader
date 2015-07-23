from profapp import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.40.71.189', port=8080)  #app.run(debug=True)
