# Generated by Django 5.2.3 on 2025-07-01 04:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('usermanagement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when last updated')),
                ('warehouse_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(help_text='Organization this record belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='usermanagement.organization')),
                ('user', models.ForeignKey(help_text='User who owns or created this record', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('organization', 'code')},
            },
        ),
        migrations.CreateModel(
            name='InventoryTransaction',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when last updated')),
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('IN', 'Stock In'), ('OUT', 'Stock Out'), ('XFER', 'Transfer'), ('ADJ', 'Adjustment')], max_length=4)),
                ('transaction_date', models.DateTimeField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('journal_id', models.CharField(max_length=20, null=True)),
                ('organization', models.ForeignKey(help_text='Organization this record belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='usermanagement.organization')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
                ('user', models.ForeignKey(help_text='User who owns or created this record', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('from_warehouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='from_transactions', to='inventory.warehouse')),
                ('to_warehouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='to_transactions', to='inventory.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryLocation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when last updated')),
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('location_type', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(help_text='Organization this record belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='usermanagement.organization')),
                ('user', models.ForeignKey(help_text='User who owns or created this record', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
            ],
            options={
                'unique_together': {('warehouse', 'code')},
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when last updated')),
                ('inventory_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity_on_hand', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('organization', models.ForeignKey(help_text='Organization this record belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='usermanagement.organization')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
                ('user', models.ForeignKey(help_text='User who owns or created this record', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.inventorylocation')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
