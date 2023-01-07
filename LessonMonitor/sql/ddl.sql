DROP TABLE IF EXISTS Teacher;
CREATE TABLE Teacher(
	account varchar(32) primary key,
    keyword varchar(32) not null
);

DROP TABLE IF EXISTS Student;
CREATE TABLE Student(
	account varchar(32) primary key,
    keyword varchar(32) not null,
    name varchar(32) not null
);

DROP TABLE IF EXISTS Teacher_Lesson;
CREATE TABLE Teacher_Lesson(
	lesson_id varchar(32) primary key,
    teacher_id varchar(32) not null,
    lesson_date datetime not null,
    lesson_info varchar(128),
    lesson_period int
);

DROP TABLE IF EXISTS Student_Lesson;
CREATE TABLE Student_Lesson(
	lesson_id varchar(32) not null,
    student_id varchar(32) not null,
    sleep_count int default 0,
    sleep_time float default 0,
    talk_count int default 0,
    talk_time float default 0,
    pry_count int default 0,
    pry_time float default 0,
    absence_count int default 0,
    absence_time float default 0,
    total_time float default 0,
    primary key(lesson_id, student_id)
);