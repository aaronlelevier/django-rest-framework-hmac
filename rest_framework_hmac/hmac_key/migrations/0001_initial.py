from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from ..models import HMACKey


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HMACKey',
            fields=[
                ('key', models.CharField(default=HMACKey.generate_key, max_length=40, primary_key=True, serialize=False)),
                ('secret', models.CharField(default=HMACKey.generate_key, max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
