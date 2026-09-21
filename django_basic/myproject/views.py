from django.shortcuts import render

def student(request):
    return render(request, 'students.html', {
        'name': 'Susruthi',
        'age': 20,
        'course': 'Python',
        'college': 'ABC College'
    })