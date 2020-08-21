# -*- coding: utf-8 -*-
from datetime import datetime
import os
# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask, render_template, request, redirect, session
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

# Flask では標準で Flask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'sunabakoza'


@app.route('/')
def index():
    return render_template('type.html')


# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@app.route('/register', methods=["GET", "POST"])
def register():
    #  登録ページを表示させる
    if request.method == "GET":
        if 'user_id' in session:
            return redirect('/typ')
        else:
            return render_template("register.html")

    # ここからPOSTの処理
    else:
        # 登録ページで登録ボタンを押した時に走る処理
        name = request.form.get("name")
        password = request.form.get("password")

        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # 課題4の答えはここ
        c.execute("insert into user values(null,?,?,'no_img.png')",
                  (name, password))
        conn.commit()
        conn.close()
        return redirect('/login')


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'user_id' in session:
            return redirect("/typ")
        else:
            return render_template("login.html")
    else:
        # ブラウザから送られてきたデータを受け取る
        name = request.form.get("name")
        password = request.form.get("password")

        # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
        # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute(
            "select id from user where name = ? and password = ?", (name, password))
        user_id = c.fetchone()
        conn.close()
        # DBから取得してきたuser_id、ここの時点ではタプル型
        print(type(user_id))
        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if user_id is None:
            # ログイン失敗すると、ログイン画面に戻す
            return render_template("login.html")
        else:
            session['user_id'] = user_id[0]
            return redirect("/typ")

# GET  /type => type画面を表示
# POST /type => type処理をする


@app.route('/typ')
def typ():
    return render_template('type.html')


@app.route('/menum', methods=['GET', 'POST'])
def muki():
    if request.method == 'POST':
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
        # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
        c.execute("select name,prof_img from user where id ")
        user_info = c.fetchone()
        print(user_info)
        c.close()
        res = render_template('menum.html' ,user_info = user_info)

    return res


@app.route('/menun', methods=['GET', 'POST'])
def natyu():
    if request.method == 'POST':
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
        # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
        c.execute("select name,prof_img from user where id ")
        user_info = c.fetchone()
        print(user_info)
        c.close()
        res = render_template('menun.html',user_info = user_info)

    return res


@app.route('/menua', methods=['GET', 'POST'])
def atode():
    if request.method == 'POST':
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
        # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
        c.execute("select name,prof_img from user where id ")
        user_info = c.fetchone()
        print(user_info)
        c.close()
        res = render_template('menua.html' ,user_info = user_info)
    return res


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/login")


@app.route('/eatm', methods=['GET', 'POST'])
def eatm():
    if request.method == 'POST':
        conn = sqlite3.connect('eatmenum.db')
        c = conn.cursor()
        c.execute(
            "select menu_name,menu_url,menu_exp from eatmenum WHERE menu_id ORDER BY RANDOM() LIMIT 3")
        menu_info = c.fetchone()
        print(menu_info)
        c.close()
        res = render_template('eatmenum.html', db_eatinfo=menu_info)

    return res


@app.route('/musclem', methods=['GET', 'POST'])
def musclem():
    if request.method == 'POST':

        conn = sqlite3.connect('menum.db')
        c = conn.cursor()
        # fetchoneはタプル型
        # user_infoの中身を確認
        c.execute(
            "select menu_name,menu_url,menu_exp from menum WHERE menu_id ORDER BY RANDOM() LIMIT 3")
        menu_info = c.fetchone()
        print(menu_info)
        c.close()

        res = render_template('musclemenum.html', db_menuinfo=menu_info)
    return res


@app.route('/eatn', methods=['GET', 'POST'])
def eatn():
    if request.method == 'POST':

        conn = sqlite3.connect('eatmenun.db')
        c = conn.cursor()
        c.execute(
            "select menu_name,menu_url,menu_exp from eatmenun WHERE menu_id ORDER BY RANDOM() LIMIT 3")
        menu_info = c.fetchone()
        print(menu_info)
        c.close()
        res = render_template('eatmenun.html', db_eatinfo=menu_info)

    return res


@app.route('/musclen', methods=['GET', 'POST'])
def musclen():
    if request.method == 'POST':
        conn = sqlite3.connect('menun.db')
        c = conn.cursor()
        c.execute(
            "select menu_name,menu_url,menu_exp from menun WHERE menu_id ORDER BY RANDOM() LIMIT 3")
        menu_info = c.fetchone()
        print(menu_info)
        c.close()
        res = render_template('musclemenun.html', db_menuinfon=menu_info)

    return res


@app.route('/eata', methods=['GET', 'POST'])
def eata():
    if request.method == 'POST':
        res = render_template('eatmenua.html')

    return res


@app.route('/musclea', methods=['GET', 'POST'])
def musclea():
    if request.method == 'POST':
        res = render_template('musclemenua.html')

    return res

# @app.route('/add', methods=["POST"])
# def add():
#     user_id = session['user_id']

#     # 課題2の答えはここ 現在時刻を取得
#     time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

#     # POSTアクセスならDBに登録する
#     # フォームから入力されたアイテム名の取得(Python2ならrequest.form.getを使う)
#     comment = request.form.get("comment")
#     conn = sqlite3.connect('service.db')
#     c = conn.cursor()
#     # 現在の最大ID取得(fetchoneの戻り値はタプル)

#     # 課題1の答えはここ null,?,?,0の0はdel_flagのデフォルト値
#     # 課題2の答えはここ timeを新たにinsert
#     c.execute("insert into bbs values(null,?,?,0,?)", (user_id, comment,time))
#     conn.commit()
#     conn.close()
#     return redirect('/bbs')

# @app.route('/edit/<int:id>')
# def edit(id):
#     if 'user_id' in session :
#         conn = sqlite3.connect('service.db')
#         c = conn.cursor()
#         c.execute("select comment from bbs where id = ?", (id,) )
#         comment = c.fetchone()
#         conn.close()

#         if comment is not None:
#             # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
#             comment = comment[0] # "りんご" ○   ("りんご",) ☓
#             # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
#         else:
#             return "アイテムがありません" # 指定したIDの name がなければときの対処

#         item = { "id":id, "comment":comment }

#         return render_template("edit.html", comment=item)
#     else:
#         return redirect("/login")


# # /add ではPOSTを使ったので /edit ではあえてGETを使う
# @app.route("/edit")
# def update_item():
#     if 'user_id' in session :
#         # ブラウザから送られてきたデータを取得
#         item_id = request.args.get("item_id") # id
#         print(item_id)
#         item_id = int(item_id) # ブラウザから送られてきたのは文字列なので整数に変換する
#         comment = request.args.get("comment") # 編集されたテキストを取得する

#         # 既にあるデータベースのデータを送られてきたデータに更新
#         conn = sqlite3.connect('service.db')
#         c = conn.cursor()
#         c.execute("update bbs set comment = ? where id = ?",(comment,item_id))
#         conn.commit()
#         conn.close()

#         # アイテム一覧へリダイレクトさせる
#         return redirect("/bbs")
#     else:
#         return redirect("/login")

# @app.route('/del' , methods=["POST"])
# def del_task():
#     id = request.form.get("comment_id")
#     id = int(id)
#     conn = sqlite3.connect('service.db')
#     c = conn.cursor()
#     # 指定されたitem_idを元にDBデータを削除せずにdel_flagを1にして一覧からは表示しないようにする
#     # 課題1の答えはここ del_flagを1にupdateする
#     c.execute("update bbs set del_flag = 1 where id=?", (id,))
#     conn.commit()
#     conn.close()
#     # 処理終了後に一覧画面に戻す
#     return redirect("/bbs")

# 課題4の答えはここ
# @app.route('/upload', methods=["POST"])
# def do_upload():
#     # bbs.tplのinputタグ name="upload" をgetしてくる
#     upload = request.files['upload']
#     # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
#     if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         return 'png,jpg,jpeg形式のファイルを選択してください'

#     # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
#     save_path = get_save_path()
#     # パスが取得できているか確認
#     print(save_path)
#     # ファイルネームをfilename変数に代入
#     filename = upload.filename
#     # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
#     upload.save(os.path.join(save_path,filename))
#     # ファイル名が取れることを確認、あとで使うよ
#     print(filename)

#     # アップロードしたユーザのIDを取得
#     user_id = session['user_id']
#     conn = sqlite3.connect('service.db')
#     c = conn.cursor()
#     # update文
#     # 上記の filename 変数ここで使うよ
#     c.execute("update user set prof_img = ? where id=?", (filename,user_id))
#     conn.commit()
#     conn.close()

#     return redirect ('/bbs')

# #課題4の答えはここも
# def get_save_path():
#     path_dir = "./static/img"
#     return path_dir


@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound(code):
    return "404だよ！！見つからないよ！！！"


# __name__ というのは、自動的に定義される変数で、現在のファイル(モジュール)名が入ります。 ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になります。
if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=True)
