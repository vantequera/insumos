# Django Signals
from django.core.exceptions import ValidationError, ObjectDoesNotExist, EmptyResultSet
from django.db.models.signals import post_save, pre_save, pre_init, pre_delete, post_init, post_delete, post_migrate
from django.dispatch import receiver
from django.db.models import Sum, Q, F, Min
from django.utils import timezone

# my_app.models
