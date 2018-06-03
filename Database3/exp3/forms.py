from django import forms


class InstituteForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'instituteId',
            'placeholder': '请输入编号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'instituteName',
            'placeholder': '请输入名称',
        }))
    homepage = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'instituteHomepage',
            'placeholder': '请输入主页',
        }))


class LaboratoryForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'laboratoryId',
            'placeholder': '请输入编号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'laboratoryName',
            'placeholder': '请输入名称',
        }))
    address = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'laboratoryAddress',
            'placeholder': '请输入地址',
        }))
    institute = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'laboratoryInstitute',
            'placeholder': '请输入所属机构编号',
        }))
    homepage = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'laboratoryHomepage',
            'placeholder': '请输入主页',
        }))


class GroupForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'groupId',
            'placeholder': '请输入编号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'groupName',
            'placeholder': '请输入名称',
        }))
    leader = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'groupLeader',
            'placeholder': '请输入组长编号',
        }))
    laboratory = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'groupLaboratory',
            'placeholder': '请输入所属实验室编号',
        }))


class TeacherForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherId',
            'placeholder': '请输入工号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherName',
            'placeholder': '请输入姓名',
        }))
    sex = forms.ChoiceField(
        required=False,
        choices=[('M', 'Man'), ('W', 'Woman'), ('U', 'Unknown')],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'teacherSex',
        }))
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherAge',
            'placeholder': '请输入年龄',
        }))
    phone = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherPhone',
            'placeholder': '请输入电话',
        }))
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherEmail',
            'placeholder': '请输入邮箱',
        }))
    group = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherGroup',
            'placeholder': '请输入所属研究组编号',
        }))


class StudentForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'studentId',
            'placeholder': '请输入学号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'studentName',
            'placeholder': '请输入姓名',
        }))
    sex = forms.ChoiceField(
        required=False,
        choices=[('M', 'Man'), ('W', 'Woman'), ('U', 'Unknown')],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'studentSex',
        }))
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'studentAge',
            'placeholder': '请输入年龄',
        }))
    tutor = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'studentTutor',
            'placeholder': '请输入导师工号',
        }))
    phone = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherPhone',
            'placeholder': '请输入电话',
        }))
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'teacherEmail',
            'placeholder': '请输入邮箱',
        }))


class ProjectForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'projectId',
            'placeholder': '请输入编号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'projectName',
            'placeholder': '请输入名称',
        }))
    group = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'projectGroup',
            'placeholder': '请输入承担研究组编号',
        }))


class AchievementForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'achievementId',
            'placeholder': '请输入编号',
        }))
    result = forms.ChoiceField(
        required=False,
        choices=[('S', 'Success'), ('F', 'Fail'), ('U', 'Unfinished')],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'achievementResult',
        }))
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'achievementStartDate',
                'placeholder': '请输入日期',
            }))
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'achievementEndDate',
                'placeholder': '请输入日期',
            }))
    project = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'achievementProject',
            'placeholder': '请输入项目编号',
        }))


class PaperForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'paperId',
            'placeholder': '请输入编号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'paperName',
            'placeholder': '请输入名称',
        }))
    teachers = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'paperTeachers',
            'placeholder': '请输入老师工号',
        }))
    students = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'paperStudents',
            'placeholder': '请输入学生学号',
        }))
    publish_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'paperPublishDate',
                'placeholder': '请输入日期',
            }))
    journal = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'paperJournal',
            'placeholder': '请输入期刊',
        }))


class PatentForm(forms.Form):
    id = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'patentId',
            'placeholder': '请输入编号',
        }))
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'patentName',
            'placeholder': '请输入名称',
        }))
    teachers = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'patentTeachers',
            'placeholder': '请输入老师工号',
        }))
    students = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'patentStudents',
            'placeholder': '请输入学生学号',
        }))
    pass_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'patentPassDate',
                'placeholder': '请输入日期',
            }))
    valid_time = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'patentValidTime',
            'placeholder': '请输入有效期',
        }))