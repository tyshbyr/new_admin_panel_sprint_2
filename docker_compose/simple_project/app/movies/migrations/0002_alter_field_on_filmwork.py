from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='certificate',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='certificate'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='file_path',
            field=models.FileField(blank=True, default='', upload_to='movies/', verbose_name='file'),
        ),
    ]
