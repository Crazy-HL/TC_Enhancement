# app.py
import tornado.ioloop
import tornado.web
import json






class ArticleHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
    def get(self):
        # 加载文章数据
        with open('content.json', 'r', encoding='utf-8') as f:
            # print(json.load(f))
            data = json.load(f)
            self.write(json.dumps(data))

class CommentsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
    
    def get(self):
        # 加载评论数据
        with open('comments.json', 'r', encoding='utf-8') as f:
            # print(json.load(f))
            data = json.load(f)
            self.write(json.dumps(data))

def make_app():
    return tornado.web.Application([
        (r"/article", ArticleHandler),
        (r"/comments", CommentsHandler),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 监听8888端口
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()