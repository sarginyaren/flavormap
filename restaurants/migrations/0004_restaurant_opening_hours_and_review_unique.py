# Generated for FlavorMap — adds opening_hours JSONField and review uniqueness

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0003_alter_reviewreply_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='opening_hours',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(
                condition=models.Q(('user__isnull', False)),
                fields=('user', 'restaurant'),
                name='unique_user_restaurant_review',
            ),
        ),
    ]
