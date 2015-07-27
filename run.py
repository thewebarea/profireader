from profapp import create_app

if __name__ == '__main__':
    app = create_app()

    #app.run(host='127.40.71.198', port=8080)  #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)  #app.run(debug=True)
    #app.run()
