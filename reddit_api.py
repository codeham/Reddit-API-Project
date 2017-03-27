import praw
from flask import Flask, jsonify, request
app = Flask(__name__)
reddit = praw.Reddit(client_id="",
                    client_secret="",
                    password="",
                    user_agent="",
                    username="")

# verify authenticated correct user
print('current reddit user: ' + str(reddit.user.me()))

@app.route("/")
def home():
    return "Greetings from the homepage !"

@app.route("/programming/")
def programming_main():
    return submissions_to_json(request.path)

@app.route("/learnprogramming/")
def learnprogramming_main():
    return submissions_to_json(request.path)

@app.route("/cscareerquestions/")
def cscareerquestions_main():
    return submissions_to_json(request.path)

def submissions_to_json(subname):
    trimmed_subname = subname.strip('/')
    subreddit = reddit.subreddit(trimmed_subname)
    all_submissions = {}
    for index, submission in enumerate(subreddit.top(limit=5)):
        all_submissions[str(index)] = [{'title': submission.title}, {'url': submission.url}, {"post_num": index}]
    return jsonify({trimmed_subname: all_submissions})

if __name__ == "__main__":
    # debug mode removed in production
    app.run(debug=True)
