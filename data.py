from College import app, db
from College.models import Student

# Add student details using app context
with app.app_context():
    student = Student(
        admission_no="A1001",
        name="John Doe",
        father_name="Mr. John Senior",
        dob="2009-05-21",
        class_name="6th Grade",
        admission_date="2018-06-15",
        leaving_date="2024-02-15",
        reason_for_leaving="Completed primary education"
    )
    
    db.session.add(student)
    db.session.commit()
    print("Student record added successfully!")