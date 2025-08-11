"""Initial migration for surveys app."""
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('is_published', models.BooleanField(default=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={'ordering': ['-start_date']},
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('image_url', models.URLField(blank=True)),
                ('table_description', models.CharField(blank=True, max_length=200)),
                ('question_type', models.CharField(choices=[('open', 'Open'), ('mc', 'Meerkeuze'), ('scale', 'Schaal')], max_length=10)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='surveys.survey')),
            ],
            options={'ordering': ['number']},
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('responded_at', models.DateTimeField(blank=True, null=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='surveys.survey')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='surveys.question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=2000)),
                ('scale', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='surveys.invitation')),
                ('option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='surveys.option')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question')),
            ],
        ),
    ]
