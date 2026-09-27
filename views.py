from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee

MAX_PIC_SIZE_MB = 5


def validate_employee_fields(name, designation, salary, address):
    errors = []
    if not name:
        errors.append("Name is required.")
    if not designation:
        errors.append("Designation is required.")
    if not salary:
        errors.append("Salary is required.")
    else:
        cleaned = salary.lstrip("-").replace(".", "", 1)
        if not cleaned.isdigit():
            errors.append("Salary must be a positive number.")
        elif float(salary) <= 0:
            errors.append("Salary must be greater than zero.")
    if not address:
        errors.append("Address is required.")
    return errors


def validate_picture(pic):
    if not pic:
        return None
    if not pic.content_type.startswith("image/"):
        return "Uploaded file must be an image (jpg, png, etc.)."
    if pic.size > MAX_PIC_SIZE_MB * 1024 * 1024:
        return f"Image must be smaller than {MAX_PIC_SIZE_MB}MB."
    return None


def index(request):
    count = Employee.objects.count()
    return render(request, "mainapp/index.html", {"count": count})


def addEmp(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        designation = request.POST.get("designation", "").strip()
        salary = request.POST.get("salary", "").strip()
        address = request.POST.get("address", "").strip()
        pic = request.FILES.get("pic")

        errors = validate_employee_fields(name, designation, salary, address)
        pic_error = validate_picture(pic)
        if pic_error:
            errors.append(pic_error)

        if errors:
            return render(request, "mainapp/addemp.html", {
                "errors": errors,
                "old": request.POST,
            })

        Employee.objects.create(
            name=name, designation=designation, salary=salary,
            picture=pic, address=address
        )
        return redirect("show")

    return render(request, "mainapp/addemp.html")


def showEmp(request):
    employees = Employee.objects.all().order_by("name")
    return render(request, "mainapp/show-employee.html", {"employees": employees})


def updateEmp(request, eid):
    emp = get_object_or_404(Employee, empid=eid)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        designation = request.POST.get("designation", "").strip()
        salary = request.POST.get("salary", "").strip()
        address = request.POST.get("address", "").strip()
        pic = request.FILES.get("pic")

        errors = validate_employee_fields(name, designation, salary, address)
        pic_error = validate_picture(pic)
        if pic_error:
            errors.append(pic_error)

        if errors:
            return render(request, "mainapp/edit-employee.html", {
                "employee": emp,
                "errors": errors,
            })

        emp.name = name
        emp.designation = designation
        emp.salary = salary
        emp.address = address
        if pic:
            emp.picture = pic
        emp.save()
        return redirect("show")

    return render(request, "mainapp/edit-employee.html", {"employee": emp})


def delEmp(request, eid):
    emp = get_object_or_404(Employee, empid=eid)
    if request.method == "POST":
        emp.delete()
        return redirect("show")
    return render(request, "mainapp/delete-employee.html", {"employee": emp})