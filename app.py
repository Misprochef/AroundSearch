from flask import Flask, render_template, request, logging, Response, redirect, flash, url_for

app = Flask(__name__)

@app.route("/")
def input():
    return render_template("input.html")

# @app.route("/output", methods = ["POST"])
# def output():
#         keyword = request.form["keyword"]
#         return redirect(url_for("redirect_test",
#                keyword = keyword))

# @app.route("/redirect_test", methods=["GET"])
# def redirect_test():
#     keyword = request.args.get("keyword", "")
#     return render_template("output.html", keyword = keyword)

@app.route("/output", methods = ["POST"])
def output():
    keyword = request.form["keyword"]
    return render_template("output.html", keyword = keyword)



if __name__ == "__main__" :
    app.run(host="0.0.0.0")
