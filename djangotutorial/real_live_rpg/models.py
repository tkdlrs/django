from datetime import datetime, timedelta, date

from django.db import models
from django.urls import reverse
from django.utils import timezone

import math 



# Create your models here.
class Skill(models.Model):
    skill_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField( "date published", default=timezone.now) 
    #
    def __str__(self):
        return self.skill_name 
    #
    def get_absolute_url(self):
        return reverse("index", kwargs={ "pk": self.pk })
    
    #
    def training_dates(self):
        return TimeSpent.objects.filter(skill=self).values_list("date", flat=True).distinct()
    
    #
    def current_streak(self):
        dates = sorted(set(self.training_dates()))
        if not dates:
            return 0
        
        today = date.today()
        streak = 0
        day = today 

        while day in dates:
            streak += 1
            day -= timedelta(days=1)
        
        return streak
    
    #
    def longest_streak(self):
        dates = sorted(set(self.training_dates()))
        if not dates: 
            return 0
        
        longest = 1
        current = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i - 1] + timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        #
        return longest
    
    #
    def total_minutes(self):
        # return sum((session.amount_time_minutes() for session in self.timespent_set.all()))
        sessions = self.timespent_set.all()
        total = timedelta()
        for session in sessions:
            if session.start_time and session.end_time:
                total += datetime.combine(session.date, session.end_time) - datetime.combine(session.date, session.start_time)
        return int(total.total_seconds() // 60)
    
    #
    def level(self):
        total_xp = self.total_minutes()
        level = int(math.sqrt(total_xp / 60))
        return min(level, 100)
    #
    def current_level(self):
        # 10,000 hours = 600,000 minutes to reach level 100
        total_minutes = self.total_minutes()
        return min(int((total_minutes / 600000) * 100), 100)
    #
    def xp_for_next_level(self):
        level = self.current_level()
        return int(((level + 1) / 100) * 600000)
    #
    def current_xp(self):
        return self.total_minutes()
    #
    # def total_training_duration(self):
    #     sessions = self.timespent_set.all()
    #     total_duration = timedelta()
    #     for session in sessions:
    #         if session.start_time and session.end_time:
    #             duration = datetime.combine(date.min, session.end_time) - datetime.combine(date.min, session.start_time)
    #             total_duration += duration
    #     return total_duration
    #
    def total_training_hours(self):
        duration = self.total_minutes()
        return round(duration / 60, 2)
    # 
    def training_at_minimum_wage_rate(self):
        return round(self.total_training_hours() * 7.25, 2)
#


class TimeSpent(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField("Training session start")
    end_time = models.TimeField("Training session end")
    pub_date = models.DateTimeField(auto_now_add=True)

    # @admin.display
    def amount_time(self):
         #
         if not self.start_time or not self.end_time or not self.date:
             return "~incomplete data" 
         #
         start_dt = datetime.combine(self.date, self.start_time)
         end_dt = datetime.combine(self.date, self.end_time)
         #
         duration = end_dt - start_dt
         total_seconds = int(duration.total_seconds())
         #
         hours = total_seconds // 3600
         minutes = (total_seconds % 3600) // 60
         seconds = total_seconds % 60
         #
         parts = []
         if hours: 
            parts.append(f"{hours}h")
         if minutes: 
            parts.append(f"{minutes}m")
         if seconds or not parts: 
             parts.append(f"{seconds}s")
         #
         return " ".join(parts)
        
    def __str__(self):
        return f"{self.skill.skill_name} ({self.start_time} - {self.end_time})"
    
    #
    def amount_time_minutes(self):
        if self.start_time and self.end_time:
            start_dt = datetime.combine(self.date, self.start_time)
            end_dt = datetime.combine(self.date, self.end_time)
            delta = end_dt - start_dt
            return int(delta.total_seconds() // 60)
        #
        return 0

