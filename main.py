import json
from flask import render_template
from flask import request
from flask import Flask
from flask import send_file
from urllib.parse import urlencode
import pymysql
import requests
import os
from pymysql.cursors import DictCursor

import io
import base64
from PIL import Image

app = Flask(__name__)

print(__name__);

import user_methods

wx_app_secret = '7566f11d5a3db4f5ec58559f1e2e01d5';
wx_app_id = 'wxe0ff0c309e00cdb8';



@app.route('/user/get_logo')
def logo_get():
	user_id = request.args.get('user_id');
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute(f'select logo from student_users where user_id = \"{user_id}\";');
	res = cursor.fetchall().get('logo');
	cursor.close();
	conn.close();
	file_path = os.path.join(os.getcwd(),'user_info',f'{user_id}','avatar',f'{res}');
	return send_file(
		file_path,
		mimetype='image/png'
	);

@app.route('/user/change_logo')
def logo_change():
	post_img = request.files.get('file');   
	user_id = request.form.get('user_id');
	file_path = os.path.join(os.getcwd(),'user_info',f'{user_id}','avatar');
	file_list = os.listdir(file_path);
	file_number = len(file_list)+1;
	file_name = f'avatar{file_number}';
	file_path = os.path.join(file_path,file_name);
	post_img.save(file_path);

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute(f'update student_users set logo = \"{file_name}\" where user_id = \"{user_id}\";');
	cursor.execute('commit;');
	cursor.close();
	conn.close();
	return "OK";

@app.route('/user/get_data')
def name_get():
	user_id = request.args.get('user_id');
	data_type = request.args.get('data_type');
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute(f'select {data_type} from student_users where user_id = \"{user_id}\";');
	res = cursor.fetchall().get(data_type);
	cursor.close();
	conn.close();
	if(res == None):
		return "这个用户很懒，什么也没有留下";
	return res;

@app.route('/user/change_data')
def name_change():
	data_type = request.args.get('data_type');
	user_id = request.args.get('user_id');
	new_data = request.args.get('new_data');
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	print(f'update student_users set {data_type} = \"{new_data}\" where user_id = \"{user_id}\";');
	cursor.execute(f'update student_users set {data_type} = \"{new_data}\" where user_id = \"{user_id}\";');
	cursor.execute('commit;');
	cursor.close();
	conn.close();
	return "OK";

@app.route('/user/change_ful_data',methods = ['POST'])
def user_data_change():
	json_data = request.get_json();
	user_id = json_data.get('user_id');
	user_name = json_data.get('user_name');
	mobile = json_data.get('mobile');
	mail = json_data.get('mail');
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	print(f'update student_users set name = \"{user_name}\",mobile = \"{mobile}\",email = \"{mail}\" where user_id = \"{user_id}\";');
	cursor.execute(f'update student_users set name = \"{user_name}\",mobile = \"{mobile}\",email = \"{mail}\" where user_id = \"{user_id}\";');
	cursor.execute('commit;');
	cursor.close();
	conn.close();
	return "OK";

@app.route('/login')
def login():
	event = json.loads(request.args.get('code'));
	print(event);
	event = event.get('code');
	print(event);
	my_params = {'appid':wx_app_id,'secret':wx_app_secret,'js_code':event,'grant_type':'authorization_code'};
	res_data = requests.get(url = 'https://api.weixin.qq.com/sns/jscode2session',params = my_params);
	res_data = res_data.content.decode(encoding='utf-8', errors='strict')
	res_data = json.loads(res_data);
	res_data = res_data.get('openid');
	print(res_data);

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute(f'select * from student_users where user_id = \"{res_data}\"');
	check_list = cursor.fetchall();
	if len(check_list) == 0:
		cursor.execute(f'insert into student_users(name,user_id,mobile,email,student_id,ctime,passwd) values(\"一般通过淘宝用户\",\"{res_data}\",\"10010001000\",\"\",220100101,\'2022-11-11\',\"asdiasjdajsd\");');
		cursor.execute('commit;');

	cursor.close();
	conn.close();
	return res_data;


def image2byte(image):
    '''
    图片转byte
    image: 必须是PIL格式
    image_bytes: 二进制
    '''
    # 创建一个字节流管道
    img_bytes = io.BytesIO()
    #把PNG格式转换成的四通道转成RGB的三通道，然后再保存成jpg格式
    image = image.convert("RGB")
    image.save(img_bytes, format="JPEG")
    image_bytes = img_bytes.getvalue()
    return image_bytes

def byte2image(byte_data):
    image = Image.open(io.BytesIO(byte_data))
    return image

@app.route('/home')
def home():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute("select * from student_users");
	data_list = cursor.fetchall();
	cursor.close();
	conn.close();
	print(data_list);
	for item in data_list:
		print(item);
	return data_list;

@app.route('/img_test')
def check_img():
	image_path = os.path.join(os.getcwd(),'images','test1.png');
	image = Image.open(image_path)

	imgByteArr = io.BytesIO()
	image.save(imgByteArr,format='PNG')
	imgByteArr = imgByteArr.getvalue()
	return send_file(
		image_path,
		mimetype='image/png',
	);

@app.route('/post/getall')
def get_full_page():
	event = request.args;
	post_id = event.get("post_id");
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	print(f'select img_url,price,title,user_id,post_time,text from post_list where id = {post_id};');
	cursor.execute(f'select img_url,price,title,user_id,post_time,text from post_list where id = {post_id};');
	data_list = cursor.fetchall();
	if(len(data_list) == 0):
		data_list.append({'title':'页面不见了哦'});
		return data_list;
	data_list = data_list[0];
	print(data_list);
	file_path = data_list['text'];
	with open(f'{file_path}','r') as f:
		file_text = f.read();
		data_list['text'] = file_text;

	print(data_list);

	img_url = data_list['img_url']

	if os.path.exists(img_url):

		data_list['img_url'] = os.listdir(img_url);

		for id in range(len(data_list['img_url'])):
			img_url = data_list['img_url'][id];
			data_list['img_url'][id] = 'http://111.230.56.222:8000/post/get_img?' + urlencode({'img_name':img_url,'post_id':post_id});

	else:
		data_list['img_url'] = '';

	data_list['user_avatar'] = 'http:///111.230.56.222:8000/img_test';

	data_list['post_time'] = data_list['post_time'] .strftime("%Y年%m月%d日 %H:%M");

	
	user_id = data_list['user_id'];
	cursor.execute(f'select name,mobile from student_users where user_id = \"{user_id}\"');
	res = cursor.fetchall();
	if len(res) == 0 :
		res = "一般通过淘宝用户";
		data_list['user_name'] = res;
		data_list['user_mobile'] = '10010001000';
	else :
		res = res[0];
		data_list['user_name'] = res.get('name');
		data_list['user_mobile'] = res.get('mobile');
	
	cursor.close();
	conn.close();

	return data_list;

@app.route('/post/get')
def request_for_post_cover():
	event = request.args;
	print(event);
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	page = int(event.get('page'));
	pageNum = int(event.get('pageNum'));
	cursor.execute('select id,img_cover,price,title,user_id,post_time from post_list order by post_time desc limit ' + str(pageNum) + ' offset ' + str((page-1)*pageNum) + ';');
	data_list = cursor.fetchall();
	for id in range(len(data_list)):
		user_id = data_list[id]['user_id'];
		cursor.execute(f'select name,mobile from student_users where user_id = \"{user_id}\"');
		res = cursor.fetchall();
		if len(res) == 0 :
			res = "一般通过淘宝用户";
			data_list[id]['user_name'] = res;
			data_list[id]['user_mobile'] = '10010001000';
		else :
			res = res[0];
			data_list[id]['user_name'] = res.get('name');
			data_list[id]['user_mobile'] = res.get('mobile');
			

	print(data_list);

	cursor.close();
	conn.close();
	print(data_list);
	return data_list;

@app.route('/post/get_withclass')
def request_for_post_cover_get_with_class():
	event = request.args;
	print(event);
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	page = int(event.get('page'));
	pageNum = int(event.get('pageNum'));
	myclass = event.get('myclass');
	cursor.execute(f'select id,img_cover,price,title,user_id,post_time from post_list where class_1 = \"{myclass}\" order by post_time desc limit ' + str(pageNum) + ' offset ' + str((page-1)*pageNum) + ';');
	data_list = cursor.fetchall();
	for id in range(len(data_list)):
		user_id = data_list[id]['user_id'];
		cursor.execute(f'select name,mobile from student_users where user_id = \"{user_id}\"');
		res = cursor.fetchall();
		if len(res) == 0 :
			res = "一般通过淘宝用户";
			data_list[id]['user_name'] = res;
			data_list[id]['user_mobile'] = '10010001000';
		else :
			res = res[0];
			data_list[id]['user_name'] = res.get('name');
			data_list[id]['user_mobile'] = res.get('mobile');
			

	print(data_list);

	cursor.close();
	conn.close();
	print(data_list);
	return data_list;

@app.route('/post/get_withmyid')
def request_for_post_cover_get_withmyid():
	event = request.args;
	print(event);
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	page = int(event.get('page'));
	pageNum = int(event.get('pageNum'));
	user_id = event.get('user_id');
	cursor.execute(f'select id,img_cover,price,title,user_id,post_time from post_list where user_id = \"{user_id}\" order by post_time desc limit ' + str(pageNum) + ' offset ' + str((page-1)*pageNum) + ';');
	data_list = cursor.fetchall();
	for id in range(len(data_list)):
		user_id = data_list[id]['user_id'];
		cursor.execute(f'select name,mobile from student_users where user_id = \"{user_id}\"');
		res = cursor.fetchall();
		if len(res) == 0 :
			res = "一般通过淘宝用户";
			data_list[id]['user_name'] = res;
			data_list[id]['user_mobile'] = '10010001000';
		else :
			res = res[0];
			data_list[id]['user_name'] = res.get('name');
			data_list[id]['user_mobile'] = res.get('mobile');
			

	print(data_list);

	cursor.close();
	conn.close();
	print(data_list);
	return data_list;

@app.route('/post/get_img')
def request_for_img_list():
	event = request.args;
	image_path = os.path.join(os.getcwd(),'post_info',str(event.get("post_id")),'images',str(event.get("img_name")));
	return send_file(
		image_path,
		mimetype='image/png',
	);

@app.route('/user/up_load/post_file',methods=['POST'])
def user_post_file():
	
	json_data = request.get_json();
	print(request.get_json());
	post_id = request.get_json().get('postid');
	file_path = os.path.join(os.getcwd(), 'post_info',str(post_id),'content');
	print(file_path)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);

	print(f'select * from post_list where id = {post_id};');

	cursor.execute(f'select * from post_list where id = {post_id};');

	data_list = cursor.fetchall();

	if 1 :
		title = json_data.get('title');
		title = "default" if title == None else title;
		img_url = os.path.join(os.getcwd(),'post_info',str(post_id),'images');
		price = json_data.get('price');
		user_id = json_data.get('user_id');
		post_time = json_data.get('date');
		class1 = json_data.get('class1');
		class2 = json_data.get('class2');
		text = os.path.join(os.getcwd(),'post_info',str(post_id),'content','content.txt');
		print(f'update post_list set title = \"{title}\",img_url = \"{img_url}\",price = {price},user_id = \"{user_id}\",post_time = \"{post_time}\",text = \"{text}\",class_1 = \"{class1}\",class_2 = \"{class2}\" where id = {post_id};');
		cursor.execute(f'update post_list set title = \"{title}\",img_url = \"{img_url}\",price = {price},user_id = \"{user_id}\",post_time = \"{post_time}\",text = \"{text}\",class_1 = \"{class1}\",class_2 = \"{class2}\" where id = {post_id};');
	
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	
	with open(os.path.join(file_path,'content.txt'), 'a') as f:
		f.write(str(request.get_json().get('text')));

		cursor.execute('commit');
		cursor.close();
		conn.close();
	
	return ['1,2,3,4,5,6,7,8,9'];

@app.route('/user/up_load/post_img',methods=['POST'])
def user_post_img():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	post_img = request.files.get('file');
	post_id = str(request.form.get('postid'));
	file_path = os.path.join(os.getcwd(), 'post_info',post_id,'images');

	print(file_path);
	
	if not os.path.exists(file_path):
		os.makedirs(file_path)
		img_name = post_img.filename;
		img_cover_url = 'http://111.230.56.222:8000/post/get_img?' + urlencode({'img_name':img_name,'post_id':post_id});
		print(img_cover_url);
		cursor.execute(f'update post_list set img_cover=\"{img_cover_url}\" where id={post_id}');

	cursor.execute('commit;');
	cursor.close()
	conn.close()

	print(post_img.filename);

	file_path = os.path.join(file_path,post_img.filename);
	post_img.save(file_path);
	return ['1,2,3,4,5,6,7,8,9'];

@app.route('/user/up_load/number_request')
def user_post_number_ready_for_request():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	img_url = f'/home/ubuntu/mini-program/post_info/0/images/';
	img_cover = 'http://111.230.56.222:8000/img_test';
	print(f"insert into post_list(title,img_url,img_cover) values(\"default\",\"{img_url}\",\"{img_cover}\");");
	cursor.execute(f"insert into post_list(title,img_url,img_cover) values(\"default\",\"{img_url}\",\"{img_cover}\");");
	


	cursor.execute(f"select max(id) from post_list");
	max_id = cursor.fetchall()[0];
	max_id = max_id['max(id)'];
	print(max_id);
	img_url = f'/home/ubuntu/mini-program/post_info/{max_id}/images/';

	cursor.execute(f"update post_list set img_url=\"{img_url}\" where id = {max_id};");

	print(f"update post_list set img_url=\"{img_url}\" where id = {max_id};");

	cursor.execute('commit;')

	cursor.close();
	conn.close();
	return json.dumps(max_id);

@app.route('/user/subscribe')
def user_subscribe():
	return render_template('subscribe.html')

if __name__ == '__main__':
	app.run(host = '0.0.0.0',port=8000);
