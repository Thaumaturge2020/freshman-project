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

app = Flask("__main__")

@app.route('/user/get_logo')
def logo_get():
	user_id = request.args.get('user_id');
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute(f'select logo from student_users where user_id = \"{user_id}\"');
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
	cursor.execute(f'update student_users set logo = \"{file_name}\" where user_id = \"{user_id}\"');
	cursor.execute('commit;');
	cursor.close();
	conn.close();
	return "OK";

@app.route('/user/get_name')
def name_get():
	user_id = request.args.get('user_id');
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute(f'select name from student_users where user_id = \"{user_id}\"');
	res = cursor.fetchall().get('name');
	cursor.close();
	conn.close();
	return res;

@app.route('/user/change_name')
def name_change():
	user_id = request.args.get('user_id');
	new_name = request.args.get('new_name');
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='THEOUTLAND190230', charset='utf8',database='mini_program');
	cursor = conn.cursor(cursor=DictCursor);
	cursor.execute(f'update name = \"{new_name}\" from student_users where user_id = \"{user_id}\"');
	cursor.execute('commit;');
	cursor.close();
	conn.close();
	return "OK";
