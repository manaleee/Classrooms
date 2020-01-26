from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout 

from .models import Classroom, Student
from .forms import ClassroomForm, RegisterForm, LoginForm , StudentForm



# -----------------------------------------------------------------------


def register(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit= False)
			user.set_password(user.password)
			user.save()
			login(request, user)
			# classroom-list --> from URL 
			return redirect("classroom-list")

	context = {
		"form": form
	}		

	return render(request, "register.html", context)


# ----------------------------------------------------------------------- 


def login_view(request):
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(request.POST)

		#username & password --> from (form.py)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")

			auth_user = authenticate(username= username, password= password)

			if auth_user is not None:
				login(request, auth_user)
				return redirect("classroom-list")

	context = {
		"form": form 
	}			
	return render(request, "login.html", context)



# ----------------------------------------------------------------------- 


def logout_view(request):
	logout(request)
	return redirect("classroom-list")


#------------------------------------------------------------------------


def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


#------------------------------------------------------------------------


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)

	students = classroom.student_set.all().order_by("name", "exam_grade")

	context = {
		"classroom": classroom,
		"students": students, 
	}
	return render(request, 'classroom_detail.html', context)


#------------------------------------------------------------------------


def classroom_create(request):
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)

		if form.is_valid():
			classroom_obj = form.save(commit=False)
			# form.save(commit=False)
			classroom_obj.teacher = request.user
			classroom_obj.save()

			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')

		print (form.errors)

	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


#------------------------------------------------------------------------




def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)




#------------------------------------------------------------------------





def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')






#------------------------------------------------------------------------


#------------------------------------------------------------------------






def student_create(request, classroom_id):
	classroom_obj = Classroom.objects.get(id=classroom_id)

	if request.user.is_anonymous:
		return redirect("login")

	if request.user != classroom_obj.teacher:
		return redirect("classroom_detail", classroom_id)
		# return redirect("classroom_detail", args= [classroom_id])

	   # return redirect("classroom_detail", kwargs={"classroom_id":| classroom_id})


	form = StudentForm()

	if request.method == "POST":
		form = StudentForm(request.POST )

		if form.is_valid():
			student_obj = form.save(commit=False)
			# form.save(commit=False)
			student_obj.classroom = classroom_obj
			student_obj.save()

			messages.success(request, "Successfully Created!")
			return redirect("classroom-detail", classroom_id )
			# return redirect("classroom-detail", args= [classroom_id] )

		# print (form.errors)

	context = {
		"form": form,
		"classroom_id": classroom_id, 
	}
	return render(request, 'create_student.html', context)



#------------------------------------------------------------------------



def student_update(request, classroom_id, student_id):
	classroom_obj = Classroom.objects.get(id=classroom_id)
	student_obj = Student.objects.get(id=student_id)


	if request.user.is_anonymous:
		return redirect("login")

	if request.user != classroom_obj.teacher:
		return redirect("classroom_detail", classroom_id)
		# return redirect("classroom_detail", args= [classroom_id])

	   # return redirect("classroom_detail", kwargs={"classroom_id":| classroom_id})


	form = StudentForm(instance=student_obj)

	if request.method == "POST":
		form = StudentForm(request.POST , instance=student_obj)

		if form.is_valid():
			# student_obj = form.save(commit=False)
			# form.save(commit=False)
			# student_obj.classroom = classroom_obj
			# student_obj.save()
			form.save()

			messages.success(request, "Successfully update!")
			return redirect("classroom-detail", classroom_id )
			# return redirect("classroom-detail", args= [classroom_id] )

		# print (form.errors)

	context = {
		"form": form,
		"classroom_id": classroom_id, 
		"student": student_obj , 
	}

	return render(request, 'update_student.html', context)




#------------------------------------------------------------------------





# def student_delete(request, classroom_id):
# 	Classroom.objects.get(id=classroom_id).delete()
# 	messages.success(request, "Successfully Deleted!")
# 	return redirect('classroom-list')





def student_delete(request, classroom_id, student_id):

	classroom_obj = Classroom.objects.get(id=classroom_id)
	
	if request.user.is_anonymous:
		return redirect("login")

	if request.user != classroom_obj.teacher:
		return redirect("classroom_detail", classroom_id)


	Student.objects.get(id=student_id).delete()

	return redirect("classroom-detail", classroom_id)





#------------------------------------------------------------------------


