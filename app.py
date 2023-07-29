from website import start

app = start()

if(__name__ == "__main__"):
	app.config["SERVER_NAME"] = "internal.local:5000"
	app.config["SESSION_COOKIE_DOMAIN"] = ".internal.local"
	app.run(host="0.0.0.0", debug=True)