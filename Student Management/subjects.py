
SUBJECTS = {

    ("BSCS", "1st"): [
        "Introduction to Computer",
        "Fundamentals of Programming",
        "Mathematics in Modern World",
        "Understanding the Self",
        "Purposive Communication",
        "Physical Education 1"
    ],

    ("BSCS", "2nd"): [
        "Object-Oriented Programming",
        "Data Structures and Algorithms",
        "Discrete Mathematics",
        "Database Management Systems",
        "Physical Education 2",
        "Rizal Course"
    ],

    ("BSCS", "3rd"): [
        "Operating Systems",
        "Computer Networks",
        "Software Engineering",
        "Web Development",
        "Information Management",
        "Physical Education 3"
    ],

    ("BSCS", "4th"): [
        "Artificial Intelligence",
        "Machine Learning",
        "Compiler Design",
        "System Administration",
        "Capstone Project 1",
        "Professional Ethics"
    ],

    ("BSCS", "5th"): [
        "Advanced Computer Science",
        "Advanced Software Engineering",
        "Capstone Project 2",
        "Research in Computing",
        "Internship / Practicum"
    ],



    ("BSIT", "1st"): [
        "Introduction to Information Technology",
        "Fundamentals of Programming",
        "Mathematics in Modern World",
        "Understanding the Self",
        "Purposive Communication",
        "Physical Education 1"
    ],

    ("BSIT", "2nd"): [
        "Object-Oriented Programming",
        "Database Management",
        "Web Systems and Technologies",
        "Data Structures",
        "Networking 1",
        "Physical Education 2"
    ],

    ("BSIT", "3rd"): [
        "Networking 2",
        "Systems Integration",
        "Information Assurance",
        "Web Development",
        "IT Project Management",
        "Physical Education 3"
    ],

    ("BSIT", "4th"): [
        "System Administration",
        "IT Security",
        "Enterprise Architecture",
        "Capstone Project 1",
        "IT Elective",
        "Professional Ethics"
    ],

    ("BSIT", "5th"): [
        "Advanced Networking",
        "Advanced IT Security",
        "Capstone Project 2",
        "Research in Information Technology",
        "Internship / Practicum"
    ],



    ("BSCpE", "1st"): [
        "Introduction to Computer Engineering",
        "Programming Fundamentals",
        "Engineering Mathematics",
        "Understanding the Self",
        "Purposive Communication",
        "Physical Education 1"
    ],

    ("BSCpE", "2nd"): [
        "Object-Oriented Programming",
        "Digital Logic Design",
        "Data Structures",
        "Engineering Physics",
        "Computer Organization",
        "Physical Education 2"
    ],

    ("BSCpE", "3rd"): [
        "Microprocessors",
        "Computer Architecture",
        "Operating Systems",
        "Embedded Systems",
        "Computer Networks",
        "Physical Education 3"
    ],

    ("BSCpE", "4th"): [
        "Advanced Computer Architecture",
        "Robotics",
        "Embedded Systems Design",
        "Computer Engineering Design",
        "Capstone Project 1",
        "Professional Ethics"
    ],

    ("BSCpE", "5th"): [
        "Advanced Embedded Systems",
        "Advanced Computer Engineering",
        "Capstone Project 2",
        "Research in Computer Engineering",
        "Internship / Practicum"
    ]
}


def get_subjects(course, year_level):
    return SUBJECTS.get(
        (course, year_level),
        []
    )
