# -*- coding:utf-8 -*-
from app import app
from app import routes

app.run(host="0.0.0.0", threaded=True, debug=True)

