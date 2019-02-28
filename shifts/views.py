from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from accounts.views import create_context_csrf, addImportantContext, loginPage
from .models import Shift, ShiftType, studentShift


def bookingView(request, bookingType):

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect(loginPage)
        else:
            context = create_context_csrf(request)

            context = addImportantContext(request, context)

            context['bookingType'] = bookingType

            try:

                shiftType = ShiftType.objects.get(name=bookingType)
                booked = studentShift.objects.filter(student=request.user)
                bookedIDs = [booking.shift.shiftID for booking in booked]
                allShifts = Shift.objects.all().filter(shiftType=shiftType).order_by('startDate', 'startTime')

                shifts = [(i, i.shiftID in bookedIDs) for i in allShifts]
                context['shifts'] = shifts



            except:
                return render(request, "error.html", context)

            return render(request, "shifts/booking.html", context)


    elif request.method == 'POST':

        currStudentShift = studentShift()

        currShift = Shift.objects.get(shiftID=request.POST['shiftID'])

        currShift.placesFilled += 1
        currShift.placesAvailable -= 1
        currShift.save()

        currStudentShift.shift = currShift

        currStudentShift.student = request.user

        currStudentShift.save()


        return redirect("/shifts/booking/" + bookingType)


def bookingGlobalView(request):

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect(loginPage)
        else:
            context = create_context_csrf(request)

            context = addImportantContext(request, context)

            try:

                booked = studentShift.objects.filter(student=request.user)
                bookedIDs = [booking.shift.shiftID for booking in booked]
                allShifts = Shift.objects.all().order_by('startDate', 'startTime')

                shifts = [(i, i.shiftID in bookedIDs) for i in allShifts]
                context['shifts'] = shifts


            except:
                return render(request, "error.html", context)

            return render(request, "shifts/bookingGlobal.html", context)

    elif request.method == 'POST':

        currStudentShift = studentShift()

        currShift = Shift.objects.get(shiftID=request.POST['shiftID'])

        currShift.placesFilled += 1
        currShift.placesAvailable -= 1
        currShift.save()

        currStudentShift.shift = currShift

        currStudentShift.student = request.user

        currStudentShift.save()

        return redirect("/shifts/booking/")


def myShiftsView(request, user=None):

    if not request.user.is_authenticated:
        return redirect(loginPage)
    else:

        if user is None:
            user = request.user

        context = create_context_csrf(request)

        context = addImportantContext(request, context)

        context['username'] = user.first_name + " " + user.last_name

        try:

            types = ShiftType.objects.all()
            studentShifts = studentShift.objects.filter(student=user)
            studentShiftID = [o.shift.shiftID for o in studentShifts]

            studentShifts = Shift.objects.filter(shiftID__in=studentShiftID)

            allShifts = []
            for type in types:

                allShifts.append(studentShifts.filter(shiftType__name=type).order_by('startDate', 'startTime'))

            context['allShifts'] = allShifts
            context['user'] = request.user

        except:
            return render(request, "error.html", context)

        return render(request, "shifts/myShifts.html", context)

def removeShift(request, user=None):
    if request.method == 'POST':

        shiftID = request.POST['shiftID']

        currPage = request.POST['next']

        currShift = Shift.objects.get(shiftID=shiftID)

        currShift.placesFilled -= 1
        currShift.placesAvailable += 1
        currShift.save()

        if user is None:
            user = request.user

        currStudentShift = studentShift.objects.filter(student=user, shift__shiftID=shiftID)

        currStudentShift.delete()

        return redirect(currPage)


def shiftSummaryView(request):

    if not request.user.is_authenticated:
        return redirect(loginPage)

    context = create_context_csrf(request)
    context = addImportantContext(request, context)

    if not request.user.is_staff:
        return render(request, "notStaff.html", context)

    summary = []

    shiftTypes = ShiftType.objects.all()

    for type in shiftTypes:

        shifts = Shift.objects.filter(shiftType=type)

        typeSummary = [(shift, studentShift.objects.filter(shift=shift)) for shift in shifts]

        summary.append((type.name, typeSummary))

    context['summary'] = summary

    return render(request, "shifts/shiftSummary.html", context)


def studentsShiftsView(request):
    # redirect if not already logged in
    if not request.user.is_authenticated:
        return redirect(loginPage)

    context = create_context_csrf(request)
    context = addImportantContext(request, context)

    if not request.user.is_staff:
        return render(request, "notStaff.html", context)

    if request.method == "GET":

        students = User.objects.filter(is_staff=False)

        studentList = [(student.username, student.first_name + " " + student.last_name) for student in students]

        context['studentList'] = studentList

        return render(request, "shifts/studentsShifts.html", context)

    if request.method == "POST":

        try:

            username = request.POST['username']

            user = User.objects.get(username=username)

            return myShiftsView(request, user)

        except:

            return render(request, "error.html", context)