from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
students = [
    {"id": 1, "name": "John Doe", "year": "1st Year", "section": "Zechariah"},
    {"id": 2, "name": "Jane Smith", "year": "2nd Year", "section": "Gabriel"}
]

# === HOME PAGE (HTML + CSS + JS) ===
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Student Management | Flask API</title>
      <style>
        body {
          font-family: "Poppins", sans-serif;
          background-color: #ffe6ef;
          color: #333;
          margin: 0;
          padding: 0;
        }

        header {
          background-color: #ff5c8d;
          color: white;
          text-align: center;
          padding: 20px 0;
          font-size: 24px;
          font-weight: bold;
          letter-spacing: 1px;
        }

        main {
          max-width: 800px;
          margin: 40px auto;
          background: white;
          border-radius: 12px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          padding: 20px 30px;
        }

        h2 {
          text-align: center;
          color: #ff5c8d;
        }

        form {
          display: flex;
          flex-direction: column;
          gap: 12px;
          margin-bottom: 25px;
        }

        input {
          padding: 10px;
          border: 2px solid #ffb6c1;
          border-radius: 8px;
          font-size: 16px;
        }

        button {
          background-color: #ff5c8d;
          color: white;
          border: none;
          padding: 12px;
          border-radius: 8px;
          font-size: 16px;
          cursor: pointer;
          transition: 0.3s;
        }

        button:hover {
          background-color: #e14a79;
        }

        table {
          width: 100%;
          border-collapse: collapse;
        }

        th, td {
          text-align: center;
          border-bottom: 1px solid #ffb6c1;
          padding: 10px;
        }

        th {
          background-color: #ff5c8d;
          color: white;
        }

        .no-data {
          text-align: center;
          color: #777;
          font-style: italic;
        }
      </style>
    </head>
    <body>
      <header>🎓 Student Management</header>

      <main>
        <h2>Add New Student</h2>
        <form id="studentForm">
          <input type="text" id="name" placeholder="Student Name" required>
          <input type="text" id="year" placeholder="Year Level (e.g. 1st Year)" required>
          <input type="text" id="section" placeholder="Section" required>
          <button type="submit">Add Student</button>
        </form>

        <h2>All Students</h2>
        <table id="studentsTable">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Year</th>
              <th>Section</th>
            </tr>
          </thead>
          <tbody id="studentList">
            <tr><td colspan="4" class="no-data">Loading students...</td></tr>
          </tbody>
        </table>
      </main>

      <script>
        const API_URL = window.location.origin;

        async function loadStudents() {
          const res = await fetch(`${API_URL}/students`);
          const data = await res.json();
          const tbody = document.getElementById("studentList");
          tbody.innerHTML = "";

          if (data.students.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="no-data">No students found.</td></tr>`;
            return;
          }

          data.students.forEach(student => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${student.id}</td>
              <td>${student.name}</td>
              <td>${student.year}</td>
              <td>${student.section}</td>
            `;
            tbody.appendChild(row);
          });
        }

        document.getElementById("studentForm").addEventListener("submit", async (e) => {
          e.preventDefault();
          const name = document.getElementById("name").value;
          const year = document.getElementById("year").value;
          const section = document.getElementById("section").value;

          const res = await fetch(`${API_URL}/students`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ name, year, section })
          });

          const data = await res.json();
          if (data.success) {
            alert("✅ Student added successfully!");
            document.getElementById("studentForm").reset();
            loadStudents();
          } else {
            alert("⚠️ Failed to add student. Please check input fields.");
          }
        });

        loadStudents();
      </script>
    </body>
    </html>
    """

# === API ROUTES ===
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

    if not data or not all(key in data for key in ("name", "year", "section")):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    new_id = students[-1]["id"] + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "year": data["year"],
        "section": data["section"]
    }

    students.append(new_student)
    return jsonify({"success": True, "message": "Student added successfully!", "student": new_student}), 201

if __name__ == '__main__':
    app.run(debug=True)
