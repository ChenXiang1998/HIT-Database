from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from .models import *
from .forms import *
from datetime import date

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'exp3/index.html'


class InstitutesListView(generic.ListView):
    template_name = 'exp3/institute/list.html'
    context_object_name = 'institutes_list'

    def get_queryset(self):
        return Institute.objects.order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        cur = connection.cursor()
        cur.execute('SELECT id, name FROM hit_labs')
        selected = cur.fetchall()
        hit_labs = []
        for item in selected:
            hit_labs.append((item[0], item[1]))
        context = super(InstitutesListView, self).get_context_data()
        context['hit_labs'] = hit_labs
        return context



def searchInstitutes(request):
    if request.method == 'POST':
        form = request.POST
        institutes_list = Institute.objects.all()
        if form['id']:
            institutes_list = institutes_list.filter(id=form['id'])
        if form['name']:
            institutes_list = institutes_list.filter(name=form['name'])
        if form['homepage']:
            institutes_list = institutes_list.filter(homepage=form['homepage'])
        if institutes_list.count() == 0:
            message = 'Institute does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/institute/result.html', {'institutes_list': institutes_list})

    form = InstituteForm()
    return render(request, 'exp3/institute/search.html', {'form': form})


def createInstitutes(request):
    if request.method == 'POST':
        try:
            form = InstituteForm(request.POST)
            if form.is_valid():
                Institute.objects.create(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    homepage=request.POST['homepage'],
                )
                return HttpResponseRedirect(reverse('exp3:institutesDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = InstituteForm()
    return render(request, 'exp3/institute/create.html', {'form': form})


class InstitutesDetailView(generic.DetailView):
    model = Institute
    template_name = 'exp3/institute/detail.html'


def updateInstitutes(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Institute.objects.filter(pk=pk).update(name=form['name'])
            if form['homepage']:
                Institute.objects.filter(pk=pk).update(homepage=form['homepage'])
            return HttpResponseRedirect(reverse('exp3:institutesDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = InstituteForm()
    return render(request, 'exp3/institute/update.html', {'institute_id': pk, 'form': form})


def deleteInstitutes(request, pk):
    try:
        Institute.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:institutesList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class LabsListView(generic.ListView):
    template_name = 'exp3/laboratory/list.html'
    context_object_name = 'labs_list'

    def get_queryset(self):
        return Laboratory.objects.order_by('id')


def searchLabs(request):
    if request.method == 'POST':
        form = request.POST
        labs_list = Laboratory.objects.all()
        if form['id']:
            labs_list = labs_list.filter(id=form['id'])
        if form['name']:
            labs_list = labs_list.filter(name=form['name'])
        if form['homepage']:
            labs_list = labs_list.filter(homepage=form['homepage'])
        if form['address']:
            labs_list = labs_list.filter(address=form['address'])
        if form['institute']:
            labs_list = labs_list.filter(institute__id=form['institute'])
        if labs_list.count() == 0:
            message = 'Laboratory does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/laboratory/result.html', {'labs_list': labs_list})

    form = LaboratoryForm()
    return render(request, 'exp3/laboratory/search.html', {'form': form})


def createLabs(request):
    if request.method == 'POST':
        try:
            form = LaboratoryForm(request.POST)
            print(12345678)
            if form.is_valid():
                Laboratory.objects.create(
                    id=request.POST['id'],
                    name = request.POST['name'],
                    address=request.POST['address'],
                    institute=Institute.objects.get(id=request.POST['institute']),
                    homepage=request.POST['homepage'],
                )
                print(123456, request.POST)
                return HttpResponseRedirect(reverse('exp3:labsDetail', args=(request.POST['id'],)))
        except Exception as e:
            print(e.__str__())
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = LaboratoryForm()
    return render(request, 'exp3/laboratory/create.html', {'form': form})


class LabsDetailView(generic.DetailView):
    model = Laboratory
    template_name = 'exp3/laboratory/detail.html'


def updateLabs(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Laboratory.objects.filter(pk=pk).update(name=form['name'])
            if form['address']:
                Laboratory.objects.filter(pk=pk).update(address=form['address'])
            if form['institute']:
                laboratory = Laboratory.objects.get(pk=pk)
                laboratory.institute = Institute.objects.get(id=form['institute'])
                laboratory.save()
            if form['homepage']:
                Laboratory.objects.filter(pk=pk).update(homepage=form['homepage'])
            return HttpResponseRedirect(reverse('exp3:labsDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = LaboratoryForm()
    return render(request, 'exp3/laboratory/update.html', {'lab_id': pk, 'form': form})


def deleteLabs(request, pk):
    try:
        Laboratory.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:labsList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class GroupsListView(generic.ListView):
    template_name = 'exp3/group/list.html'
    context_object_name = 'groups_list'

    def get_queryset(self):
        return Group.objects.order_by('id')


def searchGroups(request):
    if request.method == 'POST':
        form = request.POST
        groups_list = Group.objects.all()
        if form['id']:
            groups_list = groups_list.filter(id=form['id'])
        if form['name']:
            groups_list = groups_list.filter(name=form['name'])
        if form['leader']:
            groups_list = groups_list.filter(leader=form['leader'])
        if form['laboratory']:
            groups_list = groups_list.filter(laboratory=form['laboratory'])
        if groups_list.count() == 0:
            message = 'Group does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/group/result.html', {'groups_list': groups_list})

    form = GroupForm()
    return render(request, 'exp3/group/search.html', {'form': form})


def createGroups(request):
    if request.method == 'POST':
        try:
            form = GroupForm(request.POST)
            if form.is_valid():
                Group.objects.create(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    leader=request.POST['leader'],
                    laboratory=Laboratory.objects.get(id=request.POST['laboratory']),
                )
                return HttpResponseRedirect(reverse('exp3:groupsDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = GroupForm()
    return render(request, 'exp3/group/create.html', {'form': form})


class GroupsDetailView(generic.DetailView):
    model = Group
    template_name = 'exp3/group/detail.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        cur = connection.cursor()
        cur.execute(
            'SELECT exp3_student.id, exp3_student.name FROM exp3_student WHERE exp3_student.tutor_id in '
            '(SELECT exp3_teacher.id FROM exp3_teacher where exp3_teacher.group_id = %s)', (kwargs['object'].id,))
        context = super(GroupsDetailView, self).get_context_data(**kwargs)
        selected = cur.fetchall()
        students = []
        for item in selected:
            students.append((item[0], item[1]))
        context['students'] = students
        context['group'] = kwargs['object']
        return context


def updateGroups(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Group.objects.filter(pk=pk).update(name=form['name'])
            if form['leader']:
                Group.objects.filter(pk=pk).update(leader=form['leader'])
            if form['laboratory']:
                group = Group.objects.get(pk=pk)
                group.laboratory = Laboratory.objects.get(id=form['laboratory'])
                group.save()
            return HttpResponseRedirect(reverse('exp3:groupsDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = GroupForm()
    return render(request, 'exp3/group/update.html', {'group_id': pk, 'form': form})


def deleteGroups(request, pk):
    try:
        Group.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:groupsList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class TeachersListView(generic.ListView):
    template_name = 'exp3/teacher/list.html'
    context_object_name = 'teachers_list'

    def get_queryset(self):
        return Teacher.objects.order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        cur = connection.cursor()
        cur.execute('SELECT exp3_student.tutor_id, COUNT(*) FROM exp3_student GROUP BY exp3_student.tutor_id')
        selected = cur.fetchall()
        counts = []
        for item in selected:
            counts.append((item[0], item[1]))
        context = super(TeachersListView, self).get_context_data()
        context['counts'] = counts
        return context


def searchTeachers(request):
    if request.method == 'POST':
        form = request.POST
        teachers_list = Teacher.objects.all()
        if form['id']:
            teachers_list = teachers_list.filter(id=form['id'])
        if form['name']:
            teachers_list = teachers_list.filter(name=form['name'])
        if form['sex']:
            teachers_list = teachers_list.filter(sex=form['sex'])
        if form['age']:
            teachers_list = teachers_list.filter(age=form['age'])
        if form['phone']:
            teachers_list = teachers_list.filter(phone=form['phone'])
        if form['email']:
            teachers_list = teachers_list.filter(email=form['email'])
        if form['group']:
            teachers_list = teachers_list.filter(group__id=form['group'])
        if teachers_list.count() == 0:
            message = 'Teacher does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/teacher/result.html', {'teachers_list': teachers_list})

    form = TeacherForm()
    cur = connection.cursor()
    cur.execute('SELECT exp3_teacher.name, exp3_group.name FROM exp3_teacher, exp3_group WHERE exp3_teacher.id = exp3_group.leader')
    selected = cur.fetchall()
    leaders = []
    for item in selected:
        leaders.append((item[0], item[1]))
    return render(request, 'exp3/teacher/search.html', {'form': form, 'leaders': leaders})


def createTeachers(request):
    if request.method == 'POST':
        try:
            form = TeacherForm(request.POST)
            if form.is_valid():
                Teacher.objects.create(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    sex=request.POST['sex'],
                    age=request.POST['age'],
                    phone=request.POST['phone'],
                    email=request.POST['email'],
                    group=Group.objects.get(id=request.POST['group']),
                )
                return HttpResponseRedirect(reverse('exp3:teachersDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = TeacherForm()
    return render(request, 'exp3/teacher/create.html', {'form': form})


class TeachersDetailView(generic.DetailView):
    model = Teacher
    template_name = 'exp3/teacher/detail.html'


def updateTeachers(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Teacher.objects.filter(pk=pk).update(name=form['name'])
            if form['sex']:
                Teacher.objects.filter(pk=pk).update(sex=form['sex'])
            if form['age']:
                Teacher.objects.filter(pk=pk).update(age=form['age'])
            if form['phone']:
                Teacher.objects.filter(pk=pk).update(phone=form['phone'])
            if form['email']:
                Teacher.objects.filter(pk=pk).update(email=form['email'])
            if form['group']:
                teacher = Teacher.objects.get(pk=pk)
                teacher.group = Group.objects.get(id=form['group'])
                teacher.save()
            return HttpResponseRedirect(reverse('exp3:teachersDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = TeacherForm()
    return render(request, 'exp3/teacher/update.html', {'teacher_id': pk, 'form': form})


def deleteTeachers(request, pk):
    try:
        Teacher.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:teachersList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class StudentsListView(generic.ListView):
    template_name = 'exp3/student/list.html'
    context_object_name = 'students_list'

    def get_queryset(self):
        return Student.objects.order_by('id')


def searchStudents(request):
    if request.method == 'POST':
        form = request.POST
        students_list = Student.objects.all()
        if form['id']:
            students_list = students_list.filter(id=form['id'])
        if form['name']:
            students_list = students_list.filter(name=form['name'])
        if form['sex']:
            students_list = students_list.filter(sex=form['sex'])
        if form['age']:
            students_list = students_list.filter(age=form['age'])
        if form['tutor']:
            students_list = students_list.filter(tutor__id=form['tutor'])
        if form['phone']:
            students_list = students_list.filter(phone=form['phone'])
        if form['email']:
            students_list = students_list.filter(email=form['email'])
        if students_list.count() == 0:
            message = 'Student does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/student/result.html', {'students_list': students_list})

    form = StudentForm()
    return render(request, 'exp3/student/search.html', {'form': form})


def createStudents(request):
    if request.method == 'POST':
        try:
            form = StudentForm(request.POST)
            if form.is_valid():
                Student.objects.create(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    sex=request.POST['sex'],
                    age=request.POST['age'],
                    tutor=Teacher.objects.get(id=request.POST['tutor']),
                    phone=request.POST['phone'],
                    email=request.POST['email']
                )
                return HttpResponseRedirect(reverse('exp3:studentsDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = StudentForm()
    return render(request, 'exp3/student/create.html', {'form': form})


class StudentsDetailView(generic.DetailView):
    model = Student
    template_name = 'exp3/student/detail.html'


def updateStudents(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Student.objects.filter(pk=pk).update(name=form['name'])
            if form['sex']:
                Student.objects.filter(pk=pk).update(sex=form['sex'])
            if form['age']:
                Student.objects.filter(pk=pk).update(age=form['age'])
            if form['tutor']:
                student = Student.objects.get(pk=pk)
                student.tutor = Teacher.objects.get(id=form['tutor'])
                student.save()
            if form['phone']:
                Student.objects.filter(pk=pk).update(phone=form['phone'])
            if form['email']:
                Student.objects.filter(pk=pk).update(email=form['email'])
            return HttpResponseRedirect(reverse('exp3:studentsDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = StudentForm()
    return render(request, 'exp3/student/update.html', {'student_id': pk, 'form': form})


def deleteStudents(request, pk):
    try:
        Student.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:studentsList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class ProjectsListView(generic.ListView):
    template_name = 'exp3/project/list.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        return Project.objects.order_by('id')


def searchProjects(request):
    if request.method == 'POST':
        form = request.POST
        projects_list = Project.objects.all()
        if form['id']:
            projects_list = projects_list.filter(id=form['id'])
        if form['name']:
            projects_list = projects_list.filter(name=form['name'])
        if form['group']:
            projects_list = projects_list.filter(group__id=form['group'])
        if projects_list.count() == 0:
            message = 'Project does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/project/result.html', {'projects_list': projects_list})

    form = ProjectForm()
    return render(request, 'exp3/project/search.html', {'form': form})


def createProjects(request):
    if request.method == 'POST':
        try:
            form = ProjectForm(request.POST)
            if form.is_valid():
                Project.objects.create(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    group=Group.objects.get(id=request.POST['group']),
                )
                return HttpResponseRedirect(reverse('exp3:projectsDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = ProjectForm()
    return render(request, 'exp3/project/create.html', {'form': form})


class ProjectsDetailView(generic.DetailView):
    model = Project
    template_name = 'exp3/project/detail.html'


def updateProjects(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Project.objects.filter(pk=pk).update(name=form['name'])
            if form['group']:
                Project.objects.filter(pk=pk).update(group=Group.objects.get(id=form['group']))
            return HttpResponseRedirect(reverse('exp3:projectsDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = ProjectForm()
    return render(request, 'exp3/project/update.html', {'project_id': pk, 'form': form})


def deleteProjects(request, pk):
    try:
        Project.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:projectsList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class AchievementsListView(generic.ListView):
    template_name = 'exp3/achievement/list.html'
    context_object_name = 'achievements_list'

    def get_queryset(self):
        return Achievement.objects.order_by('id')


def searchAchievements(request):
    if request.method == 'POST':
        form = request.POST
        achievements_list = Achievement.objects.all()
        if form['id']:
            achievements_list = achievements_list.filter(id=form['id'])
        if form['result']:
            achievements_list = achievements_list.filter(result=form['result'])
        if form['start_date']:
            achievements_list = achievements_list.filter(start_date=form['start_date'])
        if form['end_date']:
            achievements_list = achievements_list.filter(end_date=form['end_date'])
        if form['project']:
            achievements_list = achievements_list.filter(project__id=form['project'])
        if achievements_list.count() == 0:
            message = 'Achievement does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/achievement/result.html', {'achievements_list': achievements_list})

    form = AchievementForm()
    return render(request, 'exp3/achievement/search.html', {'form': form})


def createAchievements(request):
    if request.method == 'POST':
        try:
            form = AchievementForm(request.POST)
            if form.is_valid():
                Achievement.objects.create(
                    id=request.POST['id'],
                    result=request.POST['result'],
                    start_date=request.POST['start_date'],
                    end_date=request.POST['end_date'],
                    project=Project.objects.get(id=request.POST['project']),
                )
                return HttpResponseRedirect(reverse('exp3:achievementsDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = AchievementForm()
    return render(request, 'exp3/achievement/create.html', {'form': form})


class AchievementsDetailView(generic.DetailView):
    model = Achievement
    template_name = 'exp3/achievement/detail.html'


def updateAchievements(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['result']:
                Achievement.objects.filter(pk=pk).update(name=form['result'])
            if form['start_date']:
                Achievement.objects.filter(pk=pk).update(start_date=form['start_date'])
            if form['end_date']:
                Achievement.objects.filter(pk=pk).update(end_date=form['end_date'])
            if form['project']:
                achievement = Achievement.objects.get(pk=pk)
                achievement.project = Project.objects.get(id=form['project'])
                achievement.save()
            return HttpResponseRedirect(reverse('exp3:achievementsDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = AchievementForm()
    return render(request, 'exp3/achievement/update.html', {'achievement_id': pk, 'form': form})


def deleteAchievements(request, pk):
    try:
        Achievement.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:achievementsList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class PapersListView(generic.ListView):
    template_name = 'exp3/paper/list.html'
    context_object_name = 'papers_list'

    def get_queryset(self):
        return Paper.objects.order_by('id')


def searchPapers(request):
    if request.method == 'POST':
        form = request.POST
        print(form['publish_date'])
        papers_list = Paper.objects.all()
        if form['id']:
            papers_list = papers_list.filter(id=form['id'])
        if form['name']:
            papers_list = papers_list.filter(name=form['name'])
        if form['teachers']:
            papers_list = papers_list.filter(teachers__id=form['teachers'])
        if form['students']:
            papers_list = papers_list.filter(students__id=form['students'])
        if form['publish_date']:
            papers_list = papers_list.filter(publish_date=form['publish_date'])
        if form['journal']:
            papers_list = papers_list.filter(journal=form['journal'])
        if papers_list.count() == 0:
            message = 'Paper does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/paper/result.html', {'papers_list': papers_list})

    form = PaperForm()
    return render(request, 'exp3/paper/search.html', {'form': form})


def createPapers(request):
    if request.method == 'POST':
        try:
            form = PaperForm(request.POST)
            if form.is_valid():
                paper = Paper(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    publish_date=request.POST['publish_date'],
                    journal=request.POST['journal'],
                )
                paper.save()
                for teacher_id in request.POST['teachers'].split():
                    paper.teachers.add(Teacher.objects.get(id=teacher_id))
                for student_id in request.POST['students'].split():
                    paper.students.add(Student.objects.get(id=student_id))
                paper.save()
                return HttpResponseRedirect(reverse('exp3:papersDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = PaperForm()
    return render(request, 'exp3/paper/create.html', {'form': form})


class PapersDetailView(generic.DetailView):
    model = Paper
    template_name = 'exp3/paper/detail.html'


def updatePapers(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Paper.objects.filter(pk=pk).update(name=form['name'])
            if form['teachers']:
                paper = Paper.objects.get(pk=pk)
                paper.teachers.clear()
                for teacher_id in form['teachers'].split():
                    paper.teachers.add(Teacher.objects.get(id=teacher_id))
                paper.save()
            if form['students']:
                paper = Paper.objects.get(pk=pk)
                paper.students.clear()
                for student_id in form['students'].split():
                    paper.students.add(Student.objects.get(id=student_id))
                paper.save()
            if form['publish_date']:
                Paper.objects.filter(pk=pk).update(publish_date=form['publish_date'])
            if form['journal']:
                Paper.objects.filter(pk=pk).update(journal=form['journal'])
            return HttpResponseRedirect(reverse('exp3:papersDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = PaperForm()
    return render(request, 'exp3/paper/update.html', {'paper_id': pk, 'form': form})


def deletePapers(request, pk):
    try:
        Paper.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:papersList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})


class PatentsListView(generic.ListView):
    template_name = 'exp3/patent/list.html'
    context_object_name = 'patents_list'

    def get_queryset(self):
        return Patent.objects.order_by('id')


def searchPatents(request):
    if request.method == 'POST':
        form = request.POST
        patents_list = Patent.objects.all()
        if form['id']:
            patents_list = patents_list.filter(id=form['id'])
        if form['name']:
            patents_list = patents_list.filter(name=form['name'])
        if form['teachers']:
            patents_list = patents_list.filter(teachers__id=form['teachers'])
        if form['students']:
            patents_list = patents_list.filter(students__id=form['students'])
        if form['pass_date']:
            patents_list = patents_list.filter(pass_date=form['pass_date'])
        if form['valid_time']:
            patents_list = patents_list.filter(valid_time=form['valid_time'])
        if patents_list.count() == 0:
            message = 'Patent does not exist.'
            return render(request, 'exp3/error.html', {'message': message})
        else:
            return render(request, 'exp3/patent/result.html', {'patents_list': patents_list})

    form = PatentForm()
    return render(request, 'exp3/patent/search.html', {'form': form})


def createPatents(request):
    if request.method == 'POST':
        try:
            form = PatentForm(request.POST)
            if form.is_valid():
                patent = Patent(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    pass_date=request.POST['pass_date'],
                    valid_time=request.POST['valid_time'],
                )
                patent.save()
                for teacher_id in request.POST['teachers'].split():
                    patent.teachers.add(Teacher.objects.get(id=teacher_id))
                for student_id in request.POST['students'].split():
                    patent.students.add(Student.objects.get(id=student_id))
                patent.save()
                return HttpResponseRedirect(reverse('exp3:patentsDetail', args=(request.POST['id'],)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = PatentForm()
    return render(request, 'exp3/patent/create.html', {'form': form})


class PatentsDetailView(generic.DetailView):
    model = Patent
    template_name = 'exp3/patent/detail.html'


def updatePatents(request, pk):
    if request.method == 'POST':
        form = request.POST
        try:
            if form['name']:
                Patent.objects.filter(pk=pk).update(name=form['name'])
            if form['teachers']:
                patent = Patent.objects.get(pk=pk)
                patent.teachers.clear()
                for teacher_id in form['teachers'].split():
                    patent.teachers.add(Teacher.objects.get(id=teacher_id))
                patent.save()
            if form['students']:
                patent = Patent.objects.get(pk=pk)
                patent.students.clear()
                for student_id in form['students'].split():
                    patent.students.add(Student.objects.get(id=student_id))
                patent.save()
            if form['pass_date']:
                Patent.objects.filter(pk=pk).update(pass_date=form['pass_date'])
            if form['valid_time']:
                Patent.objects.filter(pk=pk).update(valid_time=form['valid_time'])
            return HttpResponseRedirect(reverse('exp3:patentsDetail', args=(pk,)))
        except Exception as e:
            message = e.__str__()
            return render(request, 'exp3/error.html', {'message': message})

    form = PatentForm()
    return render(request, 'exp3/patent/update.html', {'patent_id': pk, 'form': form})


def deletePatents(request, pk):
    try:
        Patent.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('exp3:patentsList', args=()))
    except Exception as e:
        message = e.__str__()
        return render(request, 'exp3/error.html', {'message': message})
