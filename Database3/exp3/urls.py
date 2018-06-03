from django.urls import path
from . import views

app_name = 'exp3'
urlpatterns = [
    # index
    path('', views.IndexView.as_view(), name='index'),

    # institutes
    path('institutes/', views.InstitutesListView.as_view(), name='institutesList'),
    path('institutes/search/', views.searchInstitutes, name='searchInstitutes'),
    path('institutes/create/', views.createInstitutes, name='createInstitutes'),
    path('institutes/<str:pk>/', views.InstitutesDetailView.as_view(), name='institutesDetail'),
    path('institutes/<str:pk>/update/', views.updateInstitutes, name='updateInstitutes'),
    path('institutes/<str:pk>/delete/', views.deleteInstitutes, name='deleteInstitutes'),

    # laboratories
    path('labs/', views.LabsListView.as_view(), name='labsList'),
    path('labs/search/', views.searchLabs, name='searchLabs'),
    path('labs/create/', views.createLabs, name='createLabs'),
    path('labs/<str:pk>/', views.LabsDetailView.as_view(), name='labsDetail'),
    path('labs/<str:pk>/update/', views.updateLabs, name='updateLabs'),
    path('labs/<str:pk>/delete/', views.deleteLabs, name='deleteLabs'),

    # groups
    path('groups/', views.GroupsListView.as_view(), name='groupsList'),
    path('groups/search/', views.searchGroups, name='searchGroups'),
    path('groups/create/', views.createGroups, name='createGroups'),
    path('groups/<str:pk>/', views.GroupsDetailView.as_view(), name='groupsDetail'),
    path('groups/<str:pk>/update/', views.updateGroups, name='updateGroups'),
    path('groups/<str:pk>/delete/', views.deleteGroups, name='deleteGroups'),

    # teachers
    path('teachers/', views.TeachersListView.as_view(), name='teachersList'),
    path('teachers/search/', views.searchTeachers, name='searchTeachers'),
    path('teachers/create/', views.createTeachers, name='createTeachers'),
    path('teachers/<str:pk>/', views.TeachersDetailView.as_view(), name='teachersDetail'),
    path('teachers/<str:pk>/update/', views.updateTeachers, name='updateTeachers'),
    path('teachers/<str:pk>/delete/', views.deleteTeachers, name='deleteTeachers'),

    # students
    path('students/', views.StudentsListView.as_view(), name='studentsList'),
    path('students/search/', views.searchStudents, name='searchStudents'),
    path('students/create/', views.createStudents, name='createStudents'),
    path('students/<str:pk>/', views.StudentsDetailView.as_view(), name='studentsDetail'),
    path('students/<str:pk>/update/', views.updateStudents, name='updateStudents'),
    path('students/<str:pk>/delete/', views.deleteStudents, name='deleteStudents'),

    # projects
    path('projects/', views.ProjectsListView.as_view(), name='projectsList'),
    path('projects/search/', views.searchProjects, name='searchProjects'),
    path('projects/create/', views.createProjects, name='createProjects'),
    path('projects/<str:pk>/', views.ProjectsDetailView.as_view(), name='projectsDetail'),
    path('projects/<str:pk>/update/', views.updateProjects, name='updateProjects'),
    path('projects/<str:pk>/delete/', views.deleteProjects, name='deleteProjects'),

    # achievements
    path('achievements/', views.AchievementsListView.as_view(), name='achievementsList'),
    path('achievements/search/', views.searchAchievements, name='searchAchievements'),
    path('achievements/create/', views.createAchievements, name='createAchievements'),
    path('achievements/<str:pk>/', views.AchievementsDetailView.as_view(), name='achievementsDetail'),
    path('achievements/<str:pk>/update/', views.updateAchievements, name='updateAchievements'),
    path('achievements/<str:pk>/delete/', views.deleteAchievements, name='deleteAchievements'),

    # papers
    path('papers/', views.PapersListView.as_view(), name='papersList'),
    path('papers/search/', views.searchPapers, name='searchPapers'),
    path('papers/create/', views.createPapers, name='createPapers'),
    path('papers/<str:pk>/', views.PapersDetailView.as_view(), name='papersDetail'),
    path('papers/<str:pk>/update/', views.updatePapers, name='updatePapers'),
    path('papers/<str:pk>/delete/', views.deletePapers, name='deletePapers'),

    # patents
    path('patents/', views.PatentsListView.as_view(), name='patentsList'),
    path('patents/search/', views.searchPatents, name='searchPatents'),
    path('patents/create/', views.createPatents, name='createPatents'),
    path('patents/<str:pk>/', views.PatentsDetailView.as_view(), name='patentsDetail'),
    path('patents/<str:pk>/update/', views.updatePatents, name='updatePatents'),
    path('patents/<str:pk>/delete/', views.deletePatents, name='deletePatents'),
]