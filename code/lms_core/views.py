from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from lms_core.models import Course, Comment, CourseContent, ContentCompletion, CourseMember, Profile, Category
from django.core import serializers
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django import forms
from django.contrib import messages

def index(request):
    return HttpResponse("<h1>Hello World</h1>")
    
def testing(request):
    dataCourse = Course.objects.all()
    dataCourse = serializers.serialize("python", dataCourse)
    return JsonResponse(dataCourse, safe=False)

def addData(request): 
    course = Course(
        name = "Belajar Django",
        description = "Belajar Django dengan Mudah",
        price = 1000000,
        teacher = User.objects.get(username="reza")
    )
    course.save()
    return JsonResponse({"message": "Data berhasil ditambahkan"})

def editData(request):
    course = Course.objects.filter(name="Belajar Django").first()
    course.name = "Belajar Django Setelah update"
    course.save()
    return JsonResponse({"message": "Data berhasil diubah"})

def deleteData(request):
    course = Course.objects.filter(name__icontains="Belajar Django").first()
    course.delete()
    return JsonResponse({"message": "Data berhasil dihapus"})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({"message": "User registered successfully"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def list_comments(request, content_id):
    comments = Comment.objects.filter(content_id=content_id, is_approved=True)
    data = serializers.serialize("json", comments)
    return JsonResponse(data, safe=False)

def user_activity_dashboard(request, user_id):
    user = User.objects.get(id=user_id)
    stats = user.get_course_stats()
    return JsonResponse(stats)

def course_analytics(request, course_id):
    course = Course.objects.get(id=course_id)
    stats = course.get_course_stats()
    return JsonResponse(stats)

def list_course_contents(request, course_id):
    contents = CourseContent.objects.filter(course_id=course_id, release_date__lte=timezone.now())
    data = serializers.serialize("json", contents)
    return JsonResponse(data, safe=False)

@csrf_exempt
def enroll_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        user_id = data.get('user_id')

        course = Course.objects.get(id=course_id)
        user = User.objects.get(id=user_id)

        if CourseMember.objects.filter(course_id=course, user_id=user).exists():
            return JsonResponse({"error": "Student is already enrolled in this course"}, status=400)

        if CourseMember.objects.filter(course_id=course).count() >= course.max_students:
            return JsonResponse({"error": "Course is full"}, status=400)

        CourseMember.objects.create(course_id=course, user_id=user)
        return JsonResponse({"message": "Student enrolled successfully"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def add_completion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content_id = data.get('content_id')
        user_id = data.get('user_id')

        content = CourseContent.objects.get(id=content_id)
        user = User.objects.get(id=user_id)

        if ContentCompletion.objects.filter(content=content, user=user).exists():
            return JsonResponse({"error": "Content already marked as completed"}, status=400)

        ContentCompletion.objects.create(content=content, user=user)
        return JsonResponse({"message": "Content marked as completed"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def show_completion(request, course_id, user_id):
    completions = ContentCompletion.objects.filter(content__course_id=course_id, user_id=user_id)
    data = serializers.serialize("json", completions)
    count = completions.count()
    response = {
        "count": count,
        "completions": data
    }
    return JsonResponse(response, safe=False)

@csrf_exempt
def delete_completion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content_id = data.get('content_id')
        user_id = data.get('user_id')

        content = CourseContent.objects.get(id=content_id)
        user = User.objects.get(id=user_id)

        completion = ContentCompletion.objects.filter(content=content, user=user)
        if completion.exists():
            completion.delete()
            return JsonResponse({"message": "Completion deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Completion not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def show_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    courses_created = Course.objects.filter(teacher=user)
    courses_enrolled = CourseMember.objects.filter(user_id=user)
    profile_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.profile.phone if hasattr(user, 'profile') else None,
        "description": user.profile.description if hasattr(user, 'profile') else None,
        "profile_picture": user.profile.profile_picture.url if hasattr(user, 'profile') and user.profile.profile_picture else None,
        "courses_created": serializers.serialize("json", courses_created),
        "courses_enrolled": serializers.serialize("json", courses_enrolled),
    }
    return JsonResponse(profile_data)

@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.profile.phone = data.get('phone', user.profile.phone)
        user.profile.description = data.get('description', user.profile.description)
        if 'profile_picture' in request.FILES:
            user.profile.profile_picture = request.FILES['profile_picture']
        user.save()
        user.profile.save()
        profile_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.profile.phone,
            "description": user.profile.description,
            "profile_picture": user.profile.profile_picture.url if user.profile.profile_picture else None,
            "courses_created": serializers.serialize("json", Course.objects.filter(teacher=user)),
            "courses_enrolled": serializers.serialize("json", CourseMember.objects.filter(user_id=user)),
        }
        return JsonResponse(profile_data)
    return JsonResponse({"error": "Invalid request method"}, status=405)

class BatchEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course")
    students = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_staff=False), label="Students")

def batch_enroll(request):
    if request.method == 'POST':
        form = BatchEnrollForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            students = form.cleaned_data['students']
            if CourseMember.objects.filter(course_id=course).count() + len(students) > course.max_students:
                messages.error(request, "Not enough slots available for all students")
                return redirect('batch_enroll')
            for student in students:
                if not CourseMember.objects.filter(course_id=course, user_id=student).exists():
                    CourseMember.objects.create(course_id=course, user_id=student)
            messages.success(request, "Students enrolled successfully")
            return redirect('admin:index')
    else:
        form = BatchEnrollForm()
    return render(request, 'admin/batch_enroll.html', {'form': form})

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')

        category = Category.objects.create(name=name, description=description)
        return JsonResponse({"message": "Category created successfully", "category_id": category.id}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def show_categories(request):
    categories = Category.objects.all()
    data = serializers.serialize("json", categories)
    return JsonResponse(data, safe=False)

@csrf_exempt
def delete_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data.get('category_id')

        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return JsonResponse({"message": "Category deleted successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)