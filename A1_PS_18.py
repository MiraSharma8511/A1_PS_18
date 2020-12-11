in_file = 'inputPS18.txt'
out_file = 'outputPS18.txt'
prompt_file = 'promptsPS18.txt'


class Student:
    def __init__(self, student_id, cgpa):
        self.sID = student_id
        self.cgpa = cgpa

    def student_info(self):
        return (self.sID + " / " + self.cgpa) + "\n"


class StudentHashTable:
    def __init__(self, size=300):
        self.keys = []
        self.size = size
        self.map = [None] * size

    def nor_hash_id(self, key):
        h = 0
        for c in key:
            h = h + ord(c)
        return h % self.size

    def hash_id(self, key):
        h = self.nor_hash_id(key)
        return h

    def insertStudentRec(self, student_id, cgpa):
        key_exists = False
        student = Student(student_id, cgpa)
        key = student.sID
        hash_key = self.hash_id(key)
        bucket = self.map[hash_key]
        if not bucket:
            self.map[hash_key] = []
            bucket = self.map[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                key_exists = True
                break
        if key_exists:
            bucket[i] = (key, student)
        else:
            bucket.append((key, student))
            self.keys.append(key)

    def get_student_details(self, student_id):
        key = student_id
        hash_key = self.hash_id(key)
        bucket = self.map[hash_key]
        if bucket:
            for i, kv in enumerate(bucket):
                k, v = kv
                if key == k:
                    return v
        return None

    def destroyHash(self):
        self.map.clear()
        self.keys = []


class UniversityReport:
    def __init__(self):
        self.studentMap = StudentHashTable()

    def read_input_file(self):
        input_file = open(in_file, "r")
        count = 0
        for line in input_file:
            student_data_list = line.split("/")
            count += 1
            self.studentMap.insertStudentRec(student_data_list[0].strip(), student_data_list[1].strip())
        input_file.close()

        output_file = open(out_file, "w")
        output_file.write("Successfully inserted %d records into the system.\n" % count)
        output_file.close()

    def read_prompts_file(self):
        prompts_file = open(prompt_file, "r")
        for line in prompts_file:
            if line.startswith("hallOfFame:"):
                self.hallOfFame()
            elif line.startswith("courseOffer:"):
                range_list = line.replace("courseOffer: ", "").split(" ")
                range_list.pop(1)
                self.newCourseList(range_list[0], range_list[1])
            elif line.startswith("depAvg"):
                self.depAvg()
        prompts_file.close()

    def hallOfFame(self):
        cse_graduated_list = []
        ece_graduated_list = []
        mec_graduated_list = []
        arc_graduated_list = []

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            course_code = key[4:7]
            if course_code == "CSE":
                cse_cgpa = float(student.cgpa)
                cse_graduated_list.append(cse_cgpa)
            elif course_code == "ECE":
                ece_cgpa = float(student.cgpa)
                ece_graduated_list.append(ece_cgpa)
            elif course_code == "MEC":
                mec_cgpa = float(student.cgpa)
                mec_graduated_list.append(mec_cgpa)
            elif course_code == "ARC":
                arc_cgpa = float(student.cgpa)
                arc_graduated_list.append(arc_cgpa)

        max_cse_cgpa = float(max(cse_graduated_list))
        max_ece_cgpa = float(max(ece_graduated_list))
        max_mec_cgpa = float(max(mec_graduated_list))
        max_arc_cgpa = float(max(arc_graduated_list))

        eligible_student_list = []

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            graduation_year = key[0:4]
            cgpa = float(student.cgpa)
            if cgpa == max_cse_cgpa and graduation_year == "2010":
                eligible_student_list.append(student)
            elif cgpa == max_ece_cgpa and graduation_year == "2010":
                eligible_student_list.append(student)
            elif cgpa == max_mec_cgpa and graduation_year == "2010":
                eligible_student_list.append(student)
            elif cgpa == max_arc_cgpa and graduation_year == "2010":
                eligible_student_list.append(student)

        output_file = open(out_file, "a")
        output_file.write("---------- hall of fame ----------\n")
        output_file.write("Total eligible students: " + str(len(eligible_student_list)) + "\n")
        output_file.write("Qualified Students:\n")

        for student in eligible_student_list:
            output_file.write(student.student_info())
        output_file.close()

    def newCourseList(self, cgpa_from, cgpa_to):
        min_cgpa = float(cgpa_from)
        max_cgpa = float(cgpa_to)
        student_list = []
        output_file = open(out_file, "a")
        output_file.write("-------------------------------------\n")
        output_file.write("---------- new course candidates ----------\n")
        output_file.write("Input: " + cgpa_from + " to " + cgpa_to)

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            cgpa = float(student.cgpa)
            if (cgpa >= min_cgpa) and (cgpa <= max_cgpa):
                student_list.append(student)

        output_file.write("Total eligible students: " + str(len(student_list)) + "\n")
        output_file.write("Qualified Students:\n")

        for student in student_list:
            output_file.write(student.student_info())

        output_file.close()

    # This function prints the list of all departments followed
    # by the maximum CGPA and average CGPA of all students in that department.
    # The output should be captured in outputPS18.txt following format.

    def depAvg(self):
        cse_list = []
        ece_list = []
        mec_list = []
        arc_list = []

        for key in self.studentMap.keys:
            student = self.studentMap.get_student_details(key)
            course_code = key[4:7]
            if course_code == "CSE":
                cse_cgpa = float(student.cgpa)
                cse_list.append(cse_cgpa)
            elif course_code == "ECE":
                ece_cgpa = float(student.cgpa)
                ece_list.append(ece_cgpa)
            elif course_code == "MEC":
                mec_cgpa = float(student.cgpa)
                mec_list.append(mec_cgpa)
            elif course_code == "ARC":
                arc_cgpa = float(student.cgpa)
                arc_list.append(arc_cgpa)

        cse_set = set(cse_list)
        ece_set = set(ece_list)
        mec_set = set(mec_list)
        arc_set = set(arc_list)

        cse_max_cgpa = max(cse_set)
        ece_max_cgpa = max(ece_set)
        mec_max_cgpa = max(mec_set)
        arc_max_cgpa = max(arc_set)

        cse_average = sum(cse_list) / len(cse_list)
        ece_average = sum(ece_list) / len(ece_list)
        mec_average = sum(mec_list) / len(mec_list)
        arc_average = sum(arc_list) / len(arc_list)

        write_string_1 = "CSE: " + "max: " + str(cse_max_cgpa) + " avg: " + str(cse_average) + "\n"
        write_string_2 = "ECE: " + "max: " + str(ece_max_cgpa) + " avg: " + str(ece_average) + "\n"
        write_string_3 = "MEC: " + "max: " + str(mec_max_cgpa) + " avg: " + str(mec_average) + "\n"
        write_string_4 = "ARC: " + "max: " + str(arc_max_cgpa) + " avg: " + str(arc_average) + "\n"

        output_file = open(out_file, "a")
        output_file.write("-------------------------------------\n")
        output_file.write("---------- department CGPA ----------\n")
        output_file.write(write_string_1)
        output_file.write(write_string_2)
        output_file.write(write_string_3)
        output_file.write(write_string_4)
        output_file.write("-------------------------------------\n")

        output_file.close()

    def destroyHash(self):
        self.studentMap.destroyHash()


universityReport = UniversityReport()
universityReport.read_input_file()
universityReport.read_prompts_file()
universityReport.destroyHash()
