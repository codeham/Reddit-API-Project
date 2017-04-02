import praw
import json
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
# sensitive reddit data...
with open('reddit_login.json') as data_file:
    data = json.load(data_file)
print (data)

reddit = praw.Reddit(client_id = data["client_id"],
                    client_secret = data["client_secret"],
                    password = data["password"],
                    user_agent = data["user_agent"],
                    username = data["username"])

# verify authenticated correct user
print('current reddit user: ' + str(reddit.user.me()))

@app.route("/")
def home(sub1=None, sub2=None, sub3=None):
    return render_template("index.html", sub1="funny", sub2="me_irl", sub3="cscareerquestions")

@app.route("/funny/")
def programming_main():
    home(request.path)
    return submissions_to_json(request.path)

@app.route("/me_irl/")
def learnprogramming_main():
    return submissions_to_json(request.path)

@app.route("/cscareerquestions/")
def cscareerquestions_main():
    return submissions_to_json(request.path)

#img scraper, testing....
# def img_scraper(url, count):
#     # request.urlretriever(url, "img_url", + str(count) + ".jpg")

def submissions_to_json(subname):
    trimmed_subname = subname.strip('/')
    subreddit = reddit.subreddit(trimmed_subname)
    all_submissions = {}
    for index, submission in enumerate(subreddit.hot(limit=5)):
        all_submissions[str(index)] = [{'title': submission.title}, {'url': submission.url}, {"post_num": index}]
    return jsonify({trimmed_subname: all_submissions})

if __name__ == "__main__":
    # debug mode removed in production
    app.run(debug=True)
