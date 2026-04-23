from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE products_voiture CHANGE image image_exterieur VARCHAR(100);
                ALTER TABLE products_voiture ADD COLUMN image_interieur VARCHAR(100) DEFAULT '';
            """,
            reverse_sql="""
                ALTER TABLE products_voiture CHANGE image_exterieur image VARCHAR(100);
                ALTER TABLE products_voiture DROP COLUMN image_interieur;
            """,
        ),
    ]