from django.db import models


# Create your models here.
class Institute(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    homepage = models.URLField()

    def __str__(self):
        return self.id + ' ' + self.name


class Laboratory(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    homepage = models.URLField()

    def __str__(self):
        return self.id + ' ' + self.name


class Group(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    leader = models.CharField(max_length=10)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)

    def __str__(self):
        return self.id + ' ' + self.name


class Teacher(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    MAN = 'M'
    WOMAN = 'W'
    UNKNOWN_SEX = 'U'
    SEX = (
        (MAN, 'Man'),
        (WOMAN, 'Woman'),
        (UNKNOWN_SEX, 'Unknown')
    )
    sex = models.CharField(max_length=1, choices=SEX, default=UNKNOWN_SEX)
    age = models.PositiveSmallIntegerField()
    phone = models.PositiveIntegerField()
    email = models.EmailField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.id + ' ' + self.name


class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    MAN = 'M'
    WOMAN = 'W'
    UNKNOWN_SEX = 'U'
    SEX = (
        (MAN, 'Man'),
        (WOMAN, 'Woman'),
        (UNKNOWN_SEX, 'Unknown')
    )
    sex = models.CharField(max_length=1, choices=SEX, default=UNKNOWN_SEX)
    age = models.PositiveSmallIntegerField()
    tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.id + ' ' + self.name


class Project(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.id + ' ' + self.name


class Achievement(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    SUCCESS = 'S'
    FAIL = 'F'
    UNFINISHED = 'U'
    RESULT = (
        (SUCCESS, 'Success'),
        (FAIL, 'Fail'),
        (UNFINISHED, 'Unfinished')
    )
    result = models.CharField(max_length=1, choices=RESULT, default=UNFINISHED)
    start_date = models.DateField()
    end_date = models.DateField()
    project = models.OneToOneField(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.id + ' ' + self.result


class Paper(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)
    publish_date = models.DateField()
    journal = models.CharField(max_length=50)

    def __str__(self):
        return self.id + ' ' + self.name


class Patent(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)
    pass_date = models.DateField()
    valid_time = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.id + ' ' + self.name
