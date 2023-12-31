# Generated by Django 4.1.4 on 2023-04-05 12:18

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modules.file_upload_module


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, verbose_name='نام برند')),
                ('brand_slug', models.SlugField(null=True)),
                ('brand_image', models.ImageField(upload_to=modules.file_upload_module.FileUploader.upload_to, verbose_name='تصویر برند')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=50, verbose_name='نام ویژگی')),
                ('feature_slug', models.SlugField(blank=True, max_length=100, null=True, verbose_name='شناسه ویژگی')),
            ],
            options={
                'verbose_name': 'ویژگی',
                'verbose_name_plural': 'ویژگی ها',
            },
        ),
        migrations.CreateModel(
            name='FeatureValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_title', models.CharField(max_length=100, verbose_name='مقدار ویژگی')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_value', to='products.feature', verbose_name='ویژگی')),
            ],
            options={
                'verbose_name': 'مقدار ویژگی',
                'verbose_name_plural': 'مقدار ویژگی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=300, verbose_name='نام محصول')),
                ('product_summery_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='خلاصه توضیحات کالا')),
                ('product_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='توضیحات کالا')),
                ('product_image', models.ImageField(upload_to=modules.file_upload_module.FileUploader.upload_to, verbose_name='تصویر محصول')),
                ('product_price', models.PositiveBigIntegerField(default=0, verbose_name='قیمت محصول')),
                ('product_isactive', models.BooleanField(blank=True, default=False, verbose_name='وضعیت کالا')),
                ('product_slug', models.SlugField(null=True, verbose_name='شناسه کالا')),
                ('product_registerdate', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('product_publish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('product_expire_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ انقضا')),
                ('product_update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('product_brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='products.brand')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50, verbose_name='عنوان گروه کالا')),
                ('group_slug', models.SlugField(null=True, verbose_name='شناسه گروه کالا')),
                ('group_image', models.ImageField(upload_to=modules.file_upload_module.FileUploader.upload_to, verbose_name='تصویر گروه کالا')),
                ('group_isactive', models.BooleanField(blank=True, default=False, verbose_name='وضعیت گروه')),
                ('product_registerdate', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('product_publish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('product_update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('group_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='products.productgroup', verbose_name='والد گروه کالا')),
            ],
            options={
                'verbose_name': 'گروه محصول',
                'verbose_name_plural': 'گروه های محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductGallary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_gallary_image', models.ImageField(upload_to=modules.file_upload_module.FileUploader.upload_to, verbose_name='تصویر محصول')),
                ('product_gallary_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_gallary', to='products.product', verbose_name='')),
            ],
            options={
                'verbose_name': 'تصویر محصول',
                'verbose_name_plural': 'تصویر های محصول',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='مقدار ویژگی محصول')),
                ('filter_value', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_values', to='products.featurevalue', verbose_name='مقدار فیلتر')),
                ('product_feature_feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.feature', verbose_name='ویژگی')),
                ('product_feature_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_features', to='products.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'ویژگی محصول',
                'verbose_name_plural': 'ویژگی های محصولات',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_feature',
            field=models.ManyToManyField(through='products.ProductFeature', to='products.feature'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_group',
            field=models.ManyToManyField(related_name='products_of_group', to='products.productgroup', verbose_name='گروه کالا'),
        ),
        migrations.AddField(
            model_name='feature',
            name='product_group',
            field=models.ManyToManyField(related_name='features_of_group', to='products.productgroup', verbose_name='گروه کالا'),
        ),
    ]
