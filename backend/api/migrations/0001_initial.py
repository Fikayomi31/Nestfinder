# Generated by Django 3.2.25 on 2024-11-06 09:43

from django.db import migrations, models
import django.utils.timezone
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'PENDING'), ('Approved', 'APPROVED'), ('Rejected', 'REJECTED')], default='PENDING', max_length=20)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('booking_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Deplex', 'DEPLEX'), ('3 Bedroom flat', '3 BEDROOM FLAT'), ('2 Bedroom flat', '2 BEDROOM FLAT'), ('A Room Self contain', 'A ROOM SELF CONTAIN'), ('Room and Parlow Self Contain', 'ROOM AND PARLAW SELF CONTAIN')], default='3 Bedroom Flat', max_length=200)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='catergories_images/')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_object_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='', unique=True)),
                ('receiver_object_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='', unique=True)),
                ('message_text', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('New Booking', 'NEW BOOKING'), ('New Message', 'NEW MESSAGE'), ('New Review', 'NEW REVIEW')], max_length=100)),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_url', models.FileField(upload_to='property_file')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('property_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='', unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Agent_fess', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('caution_fee', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('agreement_fee', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('type_of_property', models.CharField(choices=[('rental', 'Rental'), ('sale', 'Sale')], default='Rental', max_length=200)),
                ('property_status', models.CharField(choices=[('Available', 'AVAILABE'), ('Rent', 'RENT'), ('Sold', 'SOLD')], default='Available', max_length=200)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('available_from', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': ['Properties'],
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(upload_to='property_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('1', '1 star'), ('2', '2 star'), ('3', '3 star'), ('4', '4 star'), ('5', '5 star')], default=None, max_length=200)),
                ('review_text', models.TextField()),
                ('reply', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SavedSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_criteria', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('Processing', 'PROCESSING'), ('Approved', 'APPROVED'), ('Rejected', 'REJECTED')], default='Processing', max_length=200)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('stripe_session_id', models.CharField(blank=True, max_length=2000, null=True)),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='', unique=True)),
            ],
        ),
    ]
