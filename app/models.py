# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import datetime
from django.contrib.auth.models import User

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class StockCompany(models.Model):
    company_id = models.AutoField(db_column='company_ID', primary_key=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='company_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    companyfullname = models.CharField(db_column='companyFullName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    company_code = models.CharField(db_column='company_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    company_categories = models.CharField(db_column='company_Categories', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_company'


class StockInfo(models.Model):
    companyprice = models.FloatField(db_column='companyPrice', blank=True, null=True)  # Field name made lowercase.
    companyvolume = models.IntegerField(db_column='companyVolume', blank=True, null=True)  # Field name made lowercase.
    companyeps = models.FloatField(db_column='companyEPS', blank=True, null=True)  # Field name made lowercase.
    companydps = models.FloatField(db_column='companyDPS', blank=True, null=True)  # Field name made lowercase.
    companynta = models.FloatField(db_column='companyNTA', blank=True, null=True)  # Field name made lowercase.
    companype = models.DecimalField(db_column='companyPE', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    companydy = models.FloatField(db_column='companyDY', blank=True, null=True)  # Field name made lowercase.
    companyroe = models.FloatField(db_column='companyROE', blank=True, null=True)  # Field name made lowercase.
    companyptbv = models.FloatField(db_column='companyPTBV', blank=True, null=True)  # Field name made lowercase.
    companymcap = models.FloatField(db_column='companyMCAP', blank=True, null=True)  # Field name made lowercase.
    company = models.ForeignKey(StockCompany, on_delete=models.CASCADE, related_name='companys', db_column='company_ID', blank=True, null=True)  # Field name made lowercase.
    datetimecollect = models.DateTimeField(db_column='datetimeCollect', blank=True, null=True)  # Field name made lowercase.
    info_id = models.AutoField(primary_key=True)

    #def __str__(self):
    #   return self.info_id

    class Meta:
        managed = False
        db_table = 'stock_info'



class Portfolio(models.Model):
    
    portfolio_id = models.AutoField(primary_key=True)
    symbols = models.CharField(max_length=100, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio_info = models.ForeignKey(StockInfo, on_delete=models.CASCADE)

    #def __str__(self):
    #   return self.owner


class PredictedStock(models.Model):
    company_code = models.CharField(db_column='company_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    company = models.ForeignKey('StockCompany', models.DO_NOTHING, db_column='company_ID', blank=True, null=True)  # Field name made lowercase.
    stockpriceid = models.AutoField(db_column='stockpriceID', primary_key=True)  # Field name made lowercase.
    priceday1 = models.FloatField(db_column='priceDay1', blank=True, null=True)  # Field name made lowercase.
    priceday2 = models.FloatField(db_column='priceDay2', blank=True, null=True)  # Field name made lowercase.
    priceday3 = models.FloatField(db_column='priceDay3', blank=True, null=True)  # Field name made lowercase
    coefficient = models.FloatField(blank=True, null=True)
    stock_trend = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predicted_stock'