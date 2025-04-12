# imports
from django import forms
from django.template import loader
from django.views import generic
from django.db.models import Min, Max

from django.utils.timezone import timezone
from django.shortcuts import get_object_or_404, render, redirect

from .models import TimeSpent, Skill
from .forms import TimeSpentForm, SkillForm

from collections import defaultdict
from datetime import datetime, timedelta, date



# code
class IndexView(generic.ListView):
    model = Skill
    template_name = "rpg/index.html" 
    context_object_name = "skill_list"
    
    # def get_queryset(self):
    #     """ 
    #     """
    #     return Skill.objects.order_by("-pub_date")
    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add streak data for each skill
        skill_data = []
        for skill in context["skill_list"]:
            skill_data.append({
                "skill": skill,
                "current_streak": skill.current_streak(),
                "longest_streak": skill.longest_streak(),
            })
        print(skill_data, "skill?")
        context["skill_data"] = skill_data
        #
        return context
#

# Logic for graph
### previous attempt
def get_daily_training_data(skill):
    sessions = TimeSpent.objects.filter(skill=skill)
    #
    daily_totals = defaultdict(timedelta)
    #
    for session in sessions:
        if session.start_time and session.end_time and session.date:
            start_dt = datetime.combine(session.date, session.start_time)
            end_dt = datetime.combine(session.date, session.end_time)
            duration = end_dt - start_dt
            daily_totals[session.date] += duration
    # sort and format data
    data = sorted(daily_totals.items())
    return [{"date": d.strftime("%Y-%m-%d"), "minutes":round(t.total_seconds() / 60)} for d, t in data]

### Attempt that allows graph to have 'gap' days/ holes in the data.
def get_padded_daily_training_data(skill, start_date, end_date):
    sessions = TimeSpent.objects.filter(skill=skill, date__range=(start_date, end_date))
    # Group by day and sum durations
    daily_totals = defaultdict(timedelta)
    for session in sessions:
        if session.start_time and session.end_time:
            duration = datetime.combine(session.date, session.end_time) - datetime.combine(session.date, session.start_time)
            daily_totals[session.date] += duration

    # fill in all days in range
    padded_data = []
    current = start_date
    while current <= end_date:
        duration = daily_totals.get(current)
        if duration:
            minutes = round(duration.total_seconds() / 60)
        else: 
            minutes = None 
        padded_data.append({"date":current.strftime("%Y-%m-%d"), "minutes": minutes})
        current += timedelta(days=1)
    #
    return padded_data
# 
def train_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    skill_sessions_list = TimeSpent.objects.filter(skill=skill).order_by("-date")
    #
    today = date.today()
    earliest_session = TimeSpent.objects.filter(skill=skill).aggregate(Min("date"))["date__min"]
    latest_session = TimeSpent.objects.filter(skill=skill).aggregate(Max("date"))["date__max"]
    ranges = {
        "7d": (today - timedelta(days=7), today + timedelta(days=1)),
        "1m": (today - timedelta(days=30), today + timedelta(days=1)),
        "3m": (today - timedelta(days=90), today + timedelta(days=1)),
        "6m": (today - timedelta(days=180), today + timedelta(days=1)),
        "9m": (today - timedelta(days=270), today + timedelta(days=1)),
        "1y": (today - timedelta(days=365), today + timedelta(days=1)),
        "all": (today - timedelta(days=1), latest_session),
    }
    if earliest_session is not None:
        ranges.update({"all": (earliest_session - timedelta(days=1), latest_session),})
    
    #
    selected_range = request.GET.get("range", "1m")
    start_date, end_date = ranges.get(selected_range, ranges["1m"])
    #
    chart_data = get_padded_daily_training_data(skill, start_date, end_date)
    ##
    date_ranges = [
    ("all", "All Time"),
    ("1y", "1 Year"),
    ("9m", "9 Months"),
    ("6m", "6 Months"),
    ("3m", "3 Months"),
    ("1m", "1 Month"),
    ("7d", "7 Days"),
]
    ###
    # 
    if request.method == "POST":
        form = TimeSpentForm(request.POST)
        #
        if form.is_valid():
            training = form.save(commit=False)
            training.skill = skill
            training.save()
            return redirect("rpg:train", skill_id=skill.id)
        else:
            print(form.errors)

    else:
        # form = TimeSpentForm()
        # form.fields['skill'].initial = skill      
        form = TimeSpentForm(initial={'skill': skill})
    #
    return render(request, "rpg/train.html", {
        "form": form, 
        'skill': skill, 
        "skill_sessions_list": skill_sessions_list, 
        "chart_data": chart_data, 
        "date_ranges": date_ranges,
        "xp_percent": int((skill.current_xp() / skill.xp_for_next_level()) * 100),
        })

#
def edit_training_session(request, pk):
    session = get_object_or_404(TimeSpent, pk=pk)
    #
    if request.method == "POST":
        form = TimeSpentForm(request.POST, instance=session)
        #
        if form.is_valid():          
            form.save()
            return redirect("rpg:train", skill_id=session.skill.id)
    else:
        form = TimeSpentForm(instance=session)
    #
    return render(request, "rpg/edit-training-session.html", {
        "form": form, 
        "session" : session, 
        "skill": session.skill,
    })

#
def remove_training_session(request, pk):
    session = get_object_or_404(TimeSpent, pk=pk)

    # only POST can delete
    if request.method == "POST":
        session.delete()
        return redirect('rpg:train', session.skill.id)
    # handle GET
    return render(request, "rpg/confirm-session-removal.html", {"session": session})

#
def create_skill(request):
    #
    if request.method == "POST":
        form = SkillForm(request.POST)
        #
        if form.is_valid():
            skill = form.save(commit=False)
            skill.save()
            return redirect("rpg:index")
    else:
        form = SkillForm()
    #
    return render(request, "rpg/create-skill.html", {
        "form": form,

    })
#
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    #
    if request.method == "POST":
        skill.delete()
        return redirect("rpg:index")
    # GET
    return redirect("rpg:index")
        