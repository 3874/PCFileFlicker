from flask import Flask, request, jsonify, send_from_directory, json
from tinydb import TinyDB
from flask_cors import CORS
import logging
import os, sys

qr_app = Flask(__name__)
CORS(qr_app)

QR_PORT = 9000
QR_VERSION = '0.1.2'

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates') 
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'drive')
DB_FOLDER = os.path.join(BASE_DIR, 'db')
SETTING_FOLDER = os.path.join(BASE_DIR, 'setting')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
if not os.path.exists(SETTING_FOLDER):
    os.makedirs(SETTING_FOLDER)

QR_config = None

db_path = os.path.join(DB_FOLDER,'fileDB.json')
db_path2 = os.path.join(DB_FOLDER,'companyDB.json')

db = TinyDB(db_path)
db2 = TinyDB(db_path2)

fileTable = db.table('fileTable')
compTable = db2.table('compTable')

def save_settings(settings):
    
    with open(config_path, "w") as json_file:
        json.dump(settings, json_file, indent=4)
        
    print("설정이 JSON 형태로 저장되었습니다.")

config_path = os.path.join(SETTING_FOLDER, "config.json")
if not os.path.exists(config_path):
    settings = {
        "version":QR_VERSION,
        "port": QR_PORT,
        "OPENAI_KEY": ''
    }
    save_settings(settings)
    
with open(config_path, 'r') as file:
    QR_config = json.load(file)
    
@qr_app.route('/')
def home():
    return send_from_directory(TEMPLATE_FOLDER, 'index.html')

@qr_app.route('/gotofile')
def gotofile():
    return send_from_directory(TEMPLATE_FOLDER, 'file.html')

@qr_app.route('/gotocompany')
def gotocompany():
    return send_from_directory(TEMPLATE_FOLDER, 'company.html')

@qr_app.route('/files', methods=['GET'])
def get_files():
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '').lower()
    
    files = fileTable.all()

    if search_value:
        results = []
        for file in files:
            if (search_value in file['file_name'].lower() or
                search_value in file.get('summary', '').lower() or
                search_value in file.get('tags', '').lower()):
                results.append(file)
        files = results
    
    records_with_id = [{'doc_id': file.doc_id, **file} for file in files]
    records_with_id.reverse()

    paginated_files = records_with_id[start:start + length]

    response = {
        "draw": int(request.args.get('draw', 1)),
        "recordsTotal": len(fileTable.all()),
        "recordsFiltered": len(records_with_id),
        "data": paginated_files
    }

    return jsonify(response)

@qr_app.route('/syncFiles', methods=['GET'])
def sync_files():
    # 파일 전체 조회
    files = fileTable.all()

    # 전체 파일 데이터를 포함한 response 생성
    records_with_id = [{'doc_id': file.doc_id, **file} for file in files]

    response = {
        "draw": int(request.args.get('draw', 1)), 
        "recordsTotal": len(fileTable.all()),      
        "recordsFiltered": len(records_with_id),  
        "data": records_with_id                   
    }

    return jsonify(response)

@qr_app.route('/file/<corpID>', methods=['GET'])
def get_files_by_corp_id(corpID):

    files = fileTable.all()

    matching_files = []
    for file in files:
        if file.get('company_code') == corpID: 
            matching_files.append({'doc_id': file.doc_id, 'file_name': file['file_name']})

    if not matching_files:
        return jsonify({"error": "No matched files"}), 404

    return jsonify({"files": matching_files}), 200

@qr_app.route('/companies', methods=['GET'])
def get_companies():
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '').lower()
    
    companies = compTable.all()

    if search_value:
        results = []
        for comp in companies:
            if (search_value in comp['company'].lower() or
                search_value in comp.get('summary', '').lower() or
                search_value in comp.get('tags', '').lower()):
                results.append(comp)
        companies = results
    
    records_with_id = [{'doc_id': comp.doc_id, **comp} for comp in companies]
    records_with_id.reverse()
    paginated_files = records_with_id[start:start + length]

    response = {
        "draw": int(request.args.get('draw', 1)),
        "recordsTotal": len(compTable.all()),
        "recordsFiltered": len(records_with_id),
        "data": paginated_files
    }

    return jsonify(response)

@qr_app.route('/syncCompanies', methods=['GET'])
def sync_companies():
    # 파일 전체 조회
    companies = compTable.all()

    # 전체 파일 데이터를 포함한 response 생성
    records_with_id = [{'doc_id': comp.doc_id, **comp} for comp in companies]

    response = {
        "draw": int(request.args.get('draw', 1)),  # 클라이언트에서 보내온 draw 값
        "recordsTotal": len(fileTable.all()),      # 전체 파일 개수
        "recordsFiltered": len(records_with_id),  # 전체 파일 개수 (필터링 없음)
        "data": records_with_id                   # 전체 파일 데이터
    }

    return jsonify(response)

@qr_app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@qr_app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
      
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    if os.path.exists(file_path):
        return jsonify({"error": "File already exists"}), 400

    try:
        file.save(file_path)
        fileTable.insert({'file_name': file.filename, 'tags':[], 'summary':'', 'location': file_path})
        return jsonify({"success": "File uploaded", "filename": file.filename}), 201
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        return jsonify({"error": "File could not be saved"}), 500

@qr_app.route('/delete', methods=['DELETE'])
def delete_file():
    doc_id = request.args.get('doc_id', type=int)
    if doc_id is None:
        return jsonify({"error": "No doc_id provided"}), 400

    file_entry = fileTable.get(doc_id=doc_id)

    if not file_entry:
        return jsonify({"error": "File not found"}), 404

    try:
        file_path = file_entry['location']
        fileTable.remove(doc_ids=[doc_id])
        os.remove(file_path)
        return jsonify({"success": "File deleted", "doc_id": doc_id}), 200
    except Exception as e:
        logging.error(f"Error deleting file: {e}")
        return jsonify({"error": "File could not be deleted"}), 500

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_file(filename):
    IMAGE_EXTENTIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENTIONS


if __name__ == '__main__':
    qr_app.run(host='0.0.0.0', port=QR_config['port'], debug=True)
    