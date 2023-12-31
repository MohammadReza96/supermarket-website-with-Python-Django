# Generated by Django 4.1.4 on 2023-04-07 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "products",
            "0004_alter_brand_brand_image_alter_product_product_image_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "register_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_favorites",
                        to="products.product",
                        verbose_name="کالا",
                    ),
                ),
                (
                    "user_favorite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_favorites",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر علاقه مند",
                    ),
                ),
            ],
            options={
                "verbose_name": "علاقه",
                "verbose_name_plural": "علاقه مندی ها",
            },
        ),
    ]
