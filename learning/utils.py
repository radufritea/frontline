import zipfile
import os

from datetime import timedelta, date

from .models import Course, Chapter, Lecture, Test, Question


def get_course(pk):
	course = Course.objects.get(pk=pk)
	return(course)


def get_chapters(course):
	chapters = course.chapters.all().order_by('position')
	return(chapters)


def get_lectures(chapters):
	lectures = []
	for chapter in chapters:
		for lecture in chapter.lectures.all():
			lectures.append(lecture)

	return(lectures)

def get_course_duration(lectures):
	course_duration = timedelta(seconds=0)
	for lecture in lectures:
		course_duration += lecture.duration
	return(course_duration)

def get_courses_details():
	courses_details = {}
	courses = Course.objects.all()
	for course in courses:
		chapters = get_chapters(course)
		lectures = get_lectures(chapters)
		duration = get_course_duration(lectures)
		no_of_lectures = len(lectures)
		course_details = {course.id: {'name': course.name, 'image': course.thumbnail, 'duration': duration, 'no_of_lectures': no_of_lectures}}
		courses_details.update(course_details)
	return(courses_details)


def get_index_from_zip (lecture):
	lecture = Lecture.objects.get(id=lecture)
	file_name = lecture.zip_file
	folder_name = os.path.splitext(str(file_name))[0]
	dest_folder = 'media/' + folder_name
	try:
		with zipfile.ZipFile(file_name, mode="r") as archive:
			archive.extractall(dest_folder)
			index = '/media/' + folder_name + '/index.html'
		return (index)
	except zipfile.BadZipFile as error:
		return ("Acest exercitiu nu poate fi deschis. Va rugam sa ne sesizati aceasta eroare la adresa contact@frontlinesolutions.ro")


def get_test(pk):
	test = Test.objects.get(pk=pk)
	questions = Question.objects.filter(test=test)

	return(test, questions)


def check_access(user, course):
	pass
	# permissions = CoursePermissions.objects.filter(user=user).filter(course=course)
	# today = date.today()
	# if permission == None:
	# 	return False
	# else:
	# 	for permission in permissions:
			
	# 	return False
