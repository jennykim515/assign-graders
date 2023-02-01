import csv

# column constants for course staff csv
COLUMN_INSTRUCTOR = 4
COLUMN_SECTION = 1
COLUMN_TA = 10
COLUMN_FILEPATH = 0
PATH_TO_COURSE_STAFF_CSV = "example-course-staff.csv"
PATH_TO_RESULTS_CSV = "result.csv"

"""
    Sample content to PATH_TO_COURSE_STAFF_CSV:
    filepath,Section,Time,Days,Instructor,Location,Description,Max,Enrolled,Num of LAs,LA #1,LA #2,LA #3,LA #4,
    Path/to/31882.csv,31882,10:00-10:50am,"Mon, Wed",Barrett Koster,GFS101,"31882: 10:00-10:50am; Mon, Wed; Barrett Koster; GFS101",60,60,3,Dylan Andrews,Sid Qian,William Fu,,
"""

def get_csv_tas(filename=PATH_TO_COURSE_STAFF_CSV):
    """
    Read the CSV file for TA names

    :param filename: Path to input file
    :return: Map of Sections to TAs, Section to Instructors
    """
    ta_list = {}
    section_to_instructors = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(csvfile) # skip header row

        for line in reader:
            instructor = line[COLUMN_INSTRUCTOR]
            section = line[COLUMN_SECTION]
            section_to_instructors[section] = section + " (" + instructor + ")"
            if section not in ta_list:
                ta_list[section] = []
            for ta in line[COLUMN_TA:]:
                if ta.strip():
                    name_list = ta.split(" ")
                    name = name_list[0] + " " + name_list[1][0]
                    ta_list[section].append(name)
    return ta_list, section_to_instructors

def read_csv(section):
    """
    Parse files associated to a section
    :param section: Section of class to read
    :return: a list of students in the class
    """
    names = []
    filepath = ""
    with open(PATH_TO_COURSE_STAFF_CSV, newline='') as masterfile:
        reader = csv.reader(masterfile, delimiter=',')
        for line in reader:
            if line[COLUMN_SECTION] == section:
                filepath = line[COLUMN_FILEPATH]

    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for line in reader:
            names.append(line[0] + " " + line[1])
    return names


def write_csv(section_ta_mapping, section_to_instructors):
    """

    :param section_ta_mapping: Mapping from section to list of TAs
    :param section_to_instructors: Mapping from section to instructors
    :return: Output Graders mapping to Student last names
    """
    with open(PATH_TO_RESULTS_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["SECTION", "GRADER", "LAST NAMES"])
        for section in section_ta_mapping:
            names_list = read_csv(section)
            ta_list = section_ta_mapping[section]
            num_ta = len(ta_list)
            num_students = len(names_list)
            ratio = num_students // num_ta

            start = 0
            end = ratio - 1
            for ta in ta_list:
                # if last ta, have them grade the rest
                if ta == ta_list[-1]:
                    end = num_students - 1
                writer.writerow([section_to_instructors[section], ta, ', '.join(names_list[start].split(" ")) + " - " + ', '.join(names_list[end].split(" "))])
                start = end + 1
                end += ratio

mapping, section_to_instructors = get_csv_tas()
write_csv(mapping, section_to_instructors)