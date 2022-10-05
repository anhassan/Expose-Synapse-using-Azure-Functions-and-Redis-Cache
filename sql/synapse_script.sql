CREATE SCHEMA Patients;


CREATE TABLE [Patients].[Details](
PatientId INT,
PatientAge INT,
PatientName VARCHAR(20),
AdmitDepartment VARCHAR(20)
)


INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(1,25,'Bob','Ortho')
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(2,35,'Kelly','Cardio');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(3,40,'Steve','Surgery');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(4,56,'Beth','Neuro');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(5,55,'Mike','Ortho');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(6,52,'Liz','Ortho');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(7,18,'Kevin','Surgery');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(8,56,'Shaun','Ortho');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(9,43,'Kim','Cardio');
INSERT INTO Patients.Details
(PatientId,PatientAge,PatientName,AdmitDepartment)
VALUES 
(10,34,'George','Cardio');
