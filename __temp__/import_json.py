import datetime, random
import json
from flaskblog import db
from flaskblog.models import Post

json_str = open('posts.json').read()
json_data = json.loads(json_str)

for json_post in json_data['posts']:
    # print(json_post['title'])
    r_mth = random.randint(1,10)
    r_day = random.randint(1,30)
    dte=datetime.date(2018,r_mth,r_day)
    post_new = Post(title=json_post['title'],
                    content=json_post['content'],
                    user_id=json_post['user_id'],
                    date_posted=dte)
    db.session.add(post_new)
    db.session.commit()
