from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course
from .forms import CourseModelForm, LessonModelForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


import logging
logger = logging.getLogger(__name__)


class CourseDetailView(DetailView):
    model = Course
    fields = '__all__'
    template_name = 'courses/detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        logger.debug('Courses detail view has been debugged!')
        logger.info('Logger of courses detail view informs you!')
        logger.warning('Logger of courses detail view warns you!')
        logger.error('Courses detail view went wrong!')
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        return context


class CourseCreateView(CreateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/add.html'
    context_object_name = 'form'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        context['title'] = "Course creation"
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        messages.success(self.request, 'Course %s has been successfully added.' % (data['name']))
        return super(CourseCreateView, self).form_valid(form)

class CourseUpdateView(UpdateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/edit.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super(CourseUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Course update"
        return context

    def form_valid(self, form):
        data = form.instance
        messages.success(self.request, 'The changes have been saved.')
        self.success_url = reverse_lazy('courses:edit', args=(data.id,))
        return super(CourseUpdateView, self).form_valid(form)

class CourseDeleteView(DeleteView):
    model = Course
    fields = '__all__'
    template_name = 'courses/remove.html'
    context_object_name = 'form'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(CourseDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Course deletion"
        return context

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        messages.success(self.request, 'Course %s has been deleted.' % (course.name))
        return super(CourseDeleteView, self).delete(request, *args, **kwargs)

def add_lesson(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = LessonModelForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, 'Lesson {} has been successfully added.'.format(lesson.subject))
            return redirect('courses:detail', lesson.course_id)
    else:
        form = LessonModelForm(initial={'course': course})
    return render(request, 'courses/add_lesson.html', {'form': form})

