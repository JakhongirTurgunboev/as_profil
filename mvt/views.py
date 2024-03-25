import math
from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from roof.models import RoofMaterial


def main_view(request):
    return render(request, 'main.html')


def part1_view(request):
    if request.method == 'POST':
        type = request.POST.get('materialType')
        return redirect(f'/part-second/{type}/')
    return render(request, 'part1.html')


def part2_view(request, type):
    if request.method == 'POST':
        material = request.POST.get('materialSelection')
        return redirect(f'/part-third/{int(material)}/')
    if type not in ('p', 'm', 's'):
        return HttpResponse("Noto'g'ri ma'lumot kiritilgan", status=400)
    roofs = RoofMaterial.objects.filter(type=type)

    return render(request, 'part2.html', context={'roofs': roofs})


def part3_view(request, material):
    if request.method == 'POST':
        A = Decimal(request.POST.get('fieldA'))
        B = Decimal(request.POST.get('fieldB'))
        C = Decimal(request.POST.get('fieldC'))
        D = Decimal(request.POST.get('fieldD'))
        E = Decimal(request.POST.get('fieldE'))
        F = Decimal(request.POST.get('fieldF'))
        G = Decimal(request.POST.get('fieldG'))
        H = Decimal(request.POST.get('fieldH'))

        material_id = material

        try:
            material = RoofMaterial.objects.get(pk=material_id)
        except RoofMaterial.DoesNotExist:
            return JsonResponse({'error': 'Material not found'}, status=400)

        if A <= G + H or B <= C + D + E + F:
            return JsonResponse({'error': 'Not valid sides'}, status=400)

        if material.type == 's':
            g_side = math.ceil(G / material.height_m)
            h_side = math.ceil(H / material.height_m)
            c_side = math.ceil(C / material.height_m)
            d_side = math.ceil(D / material.height_m)
            e_side = math.ceil(E / material.height_m)
            f_side = math.ceil(F / material.height_m)

            c_count = math.ceil(A / material.width_m) * c_side
            d_count = math.ceil((A - G) / material.width_m) * d_side
            e_count = math.ceil((A - G) / material.width_m) * e_side
            f_count = math.ceil(A / material.width_m) * f_side
            g_count = math.ceil(B / material.width_m) * g_side
            h_count = math.ceil((B - C - F) / material.width_m) * h_side

            all_count = sum([c_count, g_count, f_count, h_count, d_count, e_count])
            overall_price = all_count * material.price

            sides = [
                {
                    "quantity": all_count,
                    "height_meter": material.height_m,
                    "price": overall_price
                },
            ]


        else:
            c_f_side_count = math.ceil(A / material.width_m)
            d_e_side_count = math.ceil(A - G / material.width_m)
            h_side_count = math.ceil((B - C - F) / material.width_m)
            g_side_count = math.ceil(B / material.width_m)
            sides = [
                {
                    "quantity": c_f_side_count,
                    "height_meter": C,
                    "price": ((C * material.width_m) * material.price) * c_f_side_count
                },
                {
                    "quantity": c_f_side_count,
                    "height_meter": F,
                    "price": ((F * material.width_m) * material.price) * c_f_side_count
                },
                {
                    "quantity": d_e_side_count,
                    "height_meter": D,
                    "price": ((D * material.width_m) * material.price) * d_e_side_count
                },
                {
                    "quantity": d_e_side_count,
                    "height_meter": E,
                    "price": ((E * material.width_m) * material.price) * d_e_side_count
                },
                {
                    "quantity": h_side_count,
                    "height_meter": H,
                    "price": ((H * material.width_m) * material.price) * h_side_count
                },
                {
                    "quantity": g_side_count,
                    "height_meter": G,
                    "price": ((G * material.width_m) * material.price) * g_side_count
                }
            ]

            overall_price = sum(x['price'] for x in sides)

        material_type = ''
        match material.type:
            case 'p':
                material_type = 'Profnastil'
            case 's':
                material_type = 'Shifer'
            case 'm':
                material_type = 'Metall'

        overall_price = round(overall_price)

        response_data = {
            "material_title": material.title,
            "material_type": material_type,
            "material_width": material.width_m,
            "sides": sides,
            "overall_price": overall_price,
        }

        # Return the response
        return render(request, 'result.html', context=response_data)

    return render(request, 'part3.html')
