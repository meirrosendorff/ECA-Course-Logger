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
                bookedIDs = [o.shift.shiftID for o in booked]
                availableShifts = Shift.objects.all().filter(shiftType=shiftType).exclude(shiftID__in=bookedIDs)
                context['shifts'] = availableShifts.order_by('startDate', 'startTime')



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
                bookedIDs = [o.shift.shiftID for o in booked]
                availableShifts = Shift.objects.all().exclude(shiftID__in=bookedIDs)
                context['shifts'] = availableShifts.order_by('startDate', 'startTime')

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

def myShiftsView(request):

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect(loginPage)
        else:
            context = create_context_csrf(request)

            context = addImportantContext(request, context)

            # try:

            types = ShiftType.objects.all()
            studentShifts = studentShift.objects.filter(student=request.user)
            studentShiftID = [o.shift.shiftID for o in studentShifts]

            studentShifts = Shift.objects.filter(shiftID__in=studentShiftID)

            allShifts = []
            for type in types:

                allShifts.append(studentShifts.filter(shiftType__name=type).order_by('startDate', 'startTime'))

            context['allShifts'] = allShifts
            context['user'] = request.user
            #
            # except:
            #     return render(request, "error.html", context)

            return render(request, "shifts/myShifts.html", context)

def removeShift(request):
    if request.method == 'POST':

        shiftID = request.POST['shiftID']

        currShift = Shift.objects.get(shiftID=shiftID)

        currShift.placesFilled -= 1
        currShift.placesAvailable += 1
        currShift.save()

        currStudentShift = studentShift.objects.filter(student=request.user, shift__shiftID=shiftID)

        currStudentShift.delete()


        return redirect("/shifts/myShifts/")