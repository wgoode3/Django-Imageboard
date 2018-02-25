# Generated by Django 2.0.2 on 2018-02-25 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('comment', models.TextField(max_length=1000)),
                ('file_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='forums')),
                ('thumbnail', models.ImageField(blank=True, default=None, null=True, upload_to='forums')),
                ('is_thread', models.BooleanField()),
                ('is_sage', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('replies', models.ManyToManyField(blank=True, related_name='_post_replies_+', to='forum_app.Post')),
            ],
        ),
    ]