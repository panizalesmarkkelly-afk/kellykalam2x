from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary in-memory storage for students
students = [
    {"id": 1, "name": "John Doe", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Jane Smith", "grade": 9, "section": "Gabriel"}
]

@app.route('/')
def home():
    return """
    <h1>🎓 Welcome to the Student API</h1>
    <p>Use the following endpoints:</p>
    <ul>
      <li><b>GET</b> /students - View all students</li>
      <li><b>POST</b> /students - Add a new student</li>
      <li><b>GET</b> /student/&lt;id&gt; - View a specific student</li>
    </ul>
    """

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "success": True,
        "total_students": len(students),
        "students": students
    })

@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify({"success": True, "student": student})
    return jsonify({"success": False, "message": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    # Validation
    if not all(key in data for key in ("name", "grade", "section")):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Create new student entry
    new_id = students[-1]["id"] + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }

    students.append(new_student)
    return jsonify({"success": True, "message": "Student added successfully!", "student": new_student}), 201

if __name__ == '__main__':
    app.run(debug=True)
