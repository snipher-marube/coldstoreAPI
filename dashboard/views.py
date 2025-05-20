from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from coldrooms.models import ColdRoom, ColdRoomVerification
from users.models import User

class ColdRoomOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == User.UserType.COLD_ROOM_OWNER

class ColdRoomDashboardView(LoginRequiredMixin, ColdRoomOwnerRequiredMixin, ListView):
    model = ColdRoom
    template_name = 'coldrooms/dashboard.html'
    context_object_name = 'coldrooms'

    def get_queryset(self):
        return ColdRoom.objects.filter(owner=self.request.user)

class ColdRoomCreateView(LoginRequiredMixin, ColdRoomOwnerRequiredMixin, CreateView):
    model = ColdRoom
    template_name = 'coldrooms/coldroom_form.html'
    fields = ['name', 'location', 'capacity', 'temp_min', 'temp_max', 'temp_unit', 'availability_schedule']
    success_url = reverse_lazy('coldroom-dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Cold room created successfully!')
        return response

class ColdRoomUpdateView(LoginRequiredMixin, ColdRoomOwnerRequiredMixin, UpdateView):
    model = ColdRoom
    template_name = 'coldrooms/coldroom_form.html'
    fields = ['name', 'location', 'capacity', 'temp_min', 'temp_max', 'temp_unit', 'availability_schedule']
    success_url = reverse_lazy('coldroom-dashboard')

    def get_queryset(self):
        return ColdRoom.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cold room updated successfully!')
        return response

class ColdRoomDetailView(LoginRequiredMixin, ColdRoomOwnerRequiredMixin, DetailView):
    model = ColdRoom
    template_name = 'coldrooms/coldroom_detail.html'

    def get_queryset(self):
        return ColdRoom.objects.filter(owner=self.request.user)

class VerificationRequestView(LoginRequiredMixin, ColdRoomOwnerRequiredMixin, CreateView):
    model = ColdRoomVerification
    template_name = 'coldrooms/verification_form.html'
    fields = ['documentation']
    success_url = reverse_lazy('coldroom-dashboard')

    def get_coldroom(self):
        return get_object_or_404(ColdRoom, pk=self.kwargs['pk'], owner=self.request.user)

    def form_valid(self, form):
        coldroom = self.get_coldroom()
        if hasattr(coldroom, 'verification'):
            messages.error(self.request, 'Verification already requested for this cold room')
            return self.form_invalid(form)
            
        form.instance.cold_room = coldroom
        response = super().form_valid(form)
        messages.success(self.request, 'Verification request submitted successfully!')
        return response