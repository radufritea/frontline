from django.db import models
from tinymce.models import HTMLField
import datetime

from accounts.models import CustomUser

class CourseCategory(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return(self.name)


class LectureType(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return(self.name)


class Lecture(models.Model):
	name = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	position = models.PositiveSmallIntegerField(default=1)
	duration = models.DurationField(null=True)
	url = models.PositiveBigIntegerField(blank=True, null=True)
	content = HTMLField(blank=True, null=True)
	lecture_type = models.ForeignKey(LectureType, on_delete=models.CASCADE, null=True, blank=True)
	pdf_file = models.FileField(upload_to="documents/", blank=True)
	zip_file = models.FileField(upload_to="archives/", blank=True)

	def __str__(self):
		return(self.name)

class Chapter(models.Model):
	name = models.CharField(max_length=255)
	position = models.PositiveSmallIntegerField(default=1)
	lectures = models.ManyToManyField(Lecture, related_name="lectures")

	def __str__(self):
		return(self.name)


class Course(models.Model):
	name = models.CharField(max_length=255)
	thumbnail = models.ImageField(upload_to="images/", blank=True)
	description = models.TextField(null=True)
	presentation = HTMLField(null=True)
	category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True)
	chapters = models.ManyToManyField(Chapter, related_name="chapters")
	date_created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return(self.name)

class CoursePermissions(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()


NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)

class Card(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    def move(self, solved):
    	new_box = self.box + 1 if solved else BOXES[0]

    	if new_box in BOXES:
    		self.box = new_box
    		self.save()

    	return self


class Test(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField()
	thumbnail = models.ImageField(upload_to="images/", blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	questions_count = models.IntegerField(default=0)
	duration = models.DurationField(null=True)

	class Meta:
		ordering = ['date_created',]
		verbose_name_plural = "Teste"

	def __str__(self):
		return self.name


class Question(models.Model):
	label = models.CharField(max_length=500, default="")
	test = models.ForeignKey(Test, on_delete=models.CASCADE)
	order = models.IntegerField(default=0)
	feedback = models.TextField(blank=True, null=True)

	class Meta:
		ordering = ("order",)
		verbose_name_plural = "Întrebări"

	def __str__(self):
		return self.label
	

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
	label = models.CharField(max_length=500, default="")
	position = models.IntegerField("position")
	is_correct = models.BooleanField(default=False)

	class Meta:
		unique_together = [
			("question", "label"),
			("question", "position")
		]
		ordering = ("position",)
		verbose_name_plural = "Choices"

	def __str__(self):
		return self.label


class UserChoice(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


	def __str__(self):
		self.choice


class TestInstance(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	test = models.ForeignKey(Test, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)
	completed = models.BooleanField(default=False)
	date_finished = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username


