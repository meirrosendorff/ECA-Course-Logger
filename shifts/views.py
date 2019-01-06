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