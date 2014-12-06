from flask_assets import Bundle, Environment

css_all = Bundle("css/normalize.css",
		"css/foundation.css",
		"css/app.css",
		output="css/all.css")

js_all = Bundle("js/jquery.js",
		"js/updater.js",
		"js/scripts.js",
		"js/modernizr.js",
		"js/foundation.min.js",
		"js/layout.js",
		output="js/lib.js")

assets = Environment()
assets.register('css', css_all)
assets.register('js', js_all)
