
import sqlite3
import pandas as pd

db_connect = sqlite3.connect('test.db')
cursor = db_connect.cursor()

# -- Create the clinic table
create_clinic = """
CREATE TABLE Clinic (
    clinicNo INT PRIMARY KEY,
    clinicName VARCHAR(255),
    clinicAddress VARCHAR(255) UNIQUE,
    managerNo VARCHAR(255) NOT NULL,
    clinicPhone VARCHAR(255),
    FOREIGN KEY (managerNo) REFERENCES Staff
);"""

create_staff = """
CREATE TABLE Staff (
    staffNo INT PRIMARY KEY,
    clinicNo INT,
    staffName VARCHAR(255),
    staffAddress VARCHAR(255),
    staffPhone VARCHAR(255),
    staffDOB DATE,
    staffPosition VARCHAR(255),
    staffSalary INT,
    FOREIGN KEY (clinicNo) REFERENCES Clinic
);
"""

create_owner = """
CREATE TABLE Owner (
    ownerNo INT NOT NULL PRIMARY KEY,
    ownerName VARCHAR(255),
    ownerAddress VARCHAR(255),
    ownerPhone VARCHAR(255) NOT NULL
);
"""

create_pet = """
CREATE TABLE Pet (
    petNo INT PRIMARY KEY,
    ownerNo INT,
    clinicNo INT,
    petName VARCHAR(255),
    petDOB DATE,
    petSpecies VARCHAR(255),
    petBreed VARCHAR(255),
    petColor VARCHAR(255),
    FOREIGN KEY (ownerNo) REFERENCES Owner,
    FOREIGN KEY (clinicNo) REFERENCES Clinic
);
"""

create_exam = """
CREATE TABLE Examination (
    examNo INT NOT NULL PRIMARY KEY,
    petNo INT NOT NULL,
    staffNo INT NOT NULL,
    chiefComplaint VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    dateSeen DATE NOT NULL,
    actionsTaken VARCHAR(255),
    FOREIGN KEY (petNo) REFERENCES Pet,
    FOREIGN KEY (staffNo) REFERENCES Staff
);
"""
cursor.execute(create_clinic)
cursor.execute(create_staff)
cursor.execute(create_owner)
cursor.execute(create_pet)
cursor.execute(create_exam)


# Create sample tuples:

# -- Insert 5 tuples into the Clinic relation
clinic_info = """
INSERT INTO Clinic VALUES
(1, 'Pawsome Pets Clinic 1', '123 Main St, Anytown USA', 1 , '123-456-7890'),
(2, 'Pawsome Pets Clinic 2', '456 Park Ave, Anytown USA', 2 , '234-567-8901'),
(3, 'Pawsome Pets Clinic 3', '789 Hill St, Anytown USA', 4 , '345-678-9012'),
(4, 'Pawsome Pets Clinic 4', '321 River Rd, Anytown USA', 5, '456-789-0123'),
(5, 'Pawsome Pets Clinic 5', '654 Mountain Ave, Anytown USA', 3, '567-890-1234');
"""

# -- Insert 5 tuples into the Staff relation
staff_info = """
INSERT INTO Staff VALUES
(1, 2, 'John Green', '123 Main St, Anytown USA', '123-456-7890', '1990-01-01', 'Veterinarian', 80000),
(2, 2, 'Jane Doe', '456 Park Ave, Anytown USA', '234-567-8901', '1995-04-15', 'Receptionist', 40000),
(3, 4, 'Barb Johnson', '789 Hill St, Anytown USA', '345-678-9012', '1980-07-05', 'Veterinarian', 80000),
(4, 5, 'Star Williams', '321 River Rd, Anytown USA', '456-789-0123', '1985-10-20', 'Technician', 50000),
(5, 2, 'Stella Brown', '654 Mountain Ave, Anytown USA', '567-890-1234', '1988-12-31', 'Receptionist', 40000);
"""

# -- Insert 5 tuples into the Owner relation
owner_info = """
INSERT INTO Owner VALUES
(1, 'Alice Smith', '123 Main St, Anytown USA', '123-456-7890'),
(2, 'Bob Jones', '456 Park Ave, Anytown USA', '234-567-8901'),
(3, 'Carol Johnson', '789 Hill St, Anytown USA', '345-678-9012'),
(4, 'David Williams', '321 River Rd, Anytown USA', '456-789-0123'),
(5, 'Emily Brown', '654 Mountain Ave, Anytown USA', '567-890-1234');
"""

# -- Insert 5 tuples into the Pet relation
pet_info = """
INSERT INTO Pet VALUES
(1, 1, 2, 'Fluffy', '2010-01-01', 'Dog', 'Labrador Retriever', 'Yellow'),
(2, 2, 4, 'Buddy', '2012-03-15', 'Dog', 'Golden Retriever', 'Golden'),
(3, 3, 5, 'Sasha', '2011-05-07', 'Cat', 'Siamese', 'Gray'),
(4, 2, 3, 'Max', '2009-09-21', 'Dog', 'German Shepherd', 'Black'),
(5, 2, 1, 'Kitty', '2008-12-31', 'Cat', 'Domestic Shorthair', 'Tuxedo');
"""

examination_info = """
    INSERT OR IGNORE INTO Examination
    VALUES
        ('1423', 2, 2, 'Check Up', 'Monthly appointment', '2008-12-31', 'N/A'),
        ('1534', 1, 2, 'Teeth checkup', 'Looked at teeth', '2009-09-21', 'Given meds'),
        ('1523',2, 4, 'Dentist', 'Took teeth out', '2010-08-11', 'treats'),
        ('1827',5, 3, 'Femur tumor', 'remove tumor', '2000-10-08', 'Treats'),
        ('1827', 2, 3, 'Surgery', 'Had broken ribs', '2004-04-23', 'N/A');
    """

cursor.execute(clinic_info)
cursor.execute(staff_info)
cursor.execute(owner_info)
cursor.execute(pet_info)
cursor.execute(examination_info)
# --
q1 = """
SELECT *
FROM Clinic;
"""


q2 = """
SELECT *
FROM Staff;
"""


q3 = """
SELECT *
FROM Owner;
"""


q4 = """
SELECT *
FROM Pet;
"""


q5 = """
SELECT *
FROM Examination;
"""

queries = [q1, q2, q3, q4, q5]

print("Database")

for query in queries:
    cursor.execute(query)
    column_names = [row[0] for row in cursor.description]
    table_data = cursor.fetchall()
    df = pd.DataFrame(table_data, columns = column_names)
    print("...")
    print(df)
    print("...")
    

    
 # --
# -- Query 1: Get the clinic number, name, and address for all clinics
q1 = """
SELECT clinicNo, clinicName, clinicAddress
FROM Clinic;
"""

# -- Query 2: Get the staff number, name, and position for all staff members who are veterinarians
q2 = """
SELECT staffNo, staffName, staffPosition
FROM Staff
WHERE staffPosition = 'Veterinarian';
"""

# -- Query 3: Get the owner number, name, and telephone number for all owners who have pets registered at Clinic 1
q3 = """
SELECT o.ownerNo, o.ownerName, o.ownerPhone
FROM Owner o
JOIN Pet p ON o.ownerNo = p.ownerNo
JOIN Clinic c ON p.clinicNo = c.clinicNo
WHERE c.clinicNo = 1;
"""

# -- Query 4: Get the pet number, name, species, and breed for all pets registered at Clinic 2
q4 = """
SELECT p.petNo, p.petName, petSpecies, petBreed
FROM Pet p
JOIN Clinic c ON p.clinicNo = c.clinicNo
WHERE c.clinicNo = 2;
"""

# -- Query 5: Get the examination number, chief complaint, and actions taken for all examinations performed by Staff 2
q5 = """
SELECT e.examNo, e.chiefComplaint, e.actionsTaken
FROM Examination e
JOIN Staff s ON e.staffNo = s.staffNo
WHERE s.staffNo = 2;
"""
print("Queries")
queries = [q1, q2, q3, q4, q5]
for query in queries:
    cursor.execute(query)
    column_names = [row[0] for row in cursor.description]
    table_data = cursor.fetchall()
    df = pd.DataFrame(table_data, columns = column_names)
    print("...")
    print(df)
    print("...")
    
# commit changes
db_connect.close()
