from crypt import methods
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename
from trial import get_plan

app = Flask(__name__)

client  = MongoClient('mongodb+srv://smallaj1:7Ne7ysmx2Kqc49qZ@cluster0.zrz9f.mongodb.net/')

db = client['SurgARy']

auth = db['auth']


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = {
        "email": email,
        "password": password
    }

    if auth.find_one({"email": email}):
        return jsonify({"message": "Username already exists"}), 400

    auth.insert_one(user)
    return jsonify({"message": "User signed up successfully!"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    person = auth.find_one({'email': email})
    
    if not person:
        return jsonify({"message": "User not found"}), 404

    if person.get('password') != password:
        return jsonify({"message": "Incorrect password"}), 401
    
    return jsonify({"message": "User logged in"}), 200


UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

patient_collection = db['patient_info']  # Replace with your collection name

checklist = db['checklist'] # Replace with your collection name

# Utility function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to add patient information along with file uploads
@app.route('/patientinfo', methods=['POST','GET'])

def AddPatientInfo():
    if request.method == 'POST':
        if 'pdf_file' not in request.files or 'medical_image' not in request.files:
            return jsonify({"message": "PDF or medical image missing!"}), 400
        

        pdf_file = request.files['pdf_file']
        medical_image = request.files['medical_image']
        if pdf_file and allowed_file(pdf_file.filename) and pdf_file.filename.endswith('.pdf'):
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            pdf_file.save(pdf_path)
        else:
            return jsonify({"message": "Invalid PDF file!"}), 400
        
        if medical_image and allowed_file(medical_image.filename):
            image_filename = secure_filename(medical_image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            medical_image.save(image_path)
        else:
            return jsonify({"message": "Invalid medical image file!"}), 400

        # Insert into MongoDB
        patient_data = {
            'email': request.form.get('email'),
            'pdf_file_path': pdf_path,
            'medical_image_path': image_path
        }
        
        patient_collection.insert_one(patient_data)

        return jsonify({"message": "Patient info and files uploaded successfully!"}), 201

    elif request.method == 'GET':
        email = request.args.get('email')

        if not email:
            return jsonify({"message": "Email parameter is missing!"}), 400

        patient = patient_collection.find_one({"email": email})

        if not patient:
            return jsonify({"message": "Patient not found!"}), 404

        # Assuming get_plan() is your custom function that generates the plan
        plan = get_plan(patient['medical_image_path'], patient['pdf_file_path'])

        body = {
            "email": email,
            "checklists": plan
        }

        checklist.insert_one(body)

        plan_str = ""
        for idx,ch in enumerate(plan):
                plan_str += str((idx+1)) + "." + ch["title"] + ": " + ch["description"] + "\n"

        return jsonify({"checklists": plan, "plan_str": plan_str}), 200

    # Add a return in case of unsupported method types
    return jsonify({"message": "Invalid method"}), 405




        




if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)




