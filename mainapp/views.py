import re

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView

from komtek import settings
from mainapp.models import Directory, DirectoryElement


def paginator_result(request, view):
    paginator = Paginator(view.object_list, settings.TOTAL_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    dirs = []
    for dir in page_obj:
        dirs.append({
            "id": dir.id,
            "long_name": dir.long_name,
            "short_name": dir.short_name,
            "description": dir.description,
            "version": dir.version,
            "date_time": dir.date_time,
        })

    response = {
        "items": dirs,
        "num_pages": page_obj.paginator.num_pages,
        "total": page_obj.paginator.count,
    }

    return response


def paginator_result_elem(request, view):
    paginator = Paginator(view.object_list, settings.TOTAL_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    direls = []
    for direl in page_obj:
        direls.append({
            "id": direl.id,
            "directories_id": direl.directories_id,
            "element_code": direl.element_code,
            "element_value": direl.element_value,
        })

    response = {
        "items": direls,
        "num_pages": page_obj.paginator.num_pages,
        "total": page_obj.paginator.count,
    }
    return response


class DirectoryView(ListView):
    model = Directory
    queryset = Directory.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("long_name")

        response = paginator_result(request, self)

        return JsonResponse(response, safe=False)


class DateArchive(ListView):
    model = Directory
    queryset = Directory.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        result = re.findall(pattern='[0-9]{4}-[0-9]{2}-[0-9]{2}', string=kwargs.get('date'))
        if result:
            self.object_list = self.object_list.filter(date_time__icontains=kwargs.get('date'))
        else:
            return JsonResponse('Введите дату в формате YYYY-MM-DD', safe=False)

        response = paginator_result(request, self)

        return JsonResponse(response, safe=False)


class DirectoryElementViewCurrentDate(ListView):
    models = DirectoryElement
    queryset = DirectoryElement.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.filter(directories__short_name=kwargs.get('short_name'))

        response = paginator_result_elem(request, self)

        return JsonResponse(response, safe=False)


class DirectoryElementView(ListView):
    models = DirectoryElement
    queryset = DirectoryElement.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.filter(Q(directories__short_name=kwargs.get('short_name')) &
                                                   Q(directories__version=kwargs.get('version')))

        response = paginator_result_elem(request, self)

        return JsonResponse(response, safe=False)
