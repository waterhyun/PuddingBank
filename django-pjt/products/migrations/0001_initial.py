from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.CharField(max_length=100, unique=True)),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'base_products',
            },
        ),
        migrations.CreateModel(
            name='DepositOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField()),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('intr_rate', models.FloatField(default=-1)),
                ('intr_rate2', models.FloatField(default=-1)),
                ('save_trm', models.IntegerField()),
            ],
            options={
                'db_table': 'deposit_options',
            },
        ),
        migrations.CreateModel(
            name='DepositProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('join_way', models.TextField()),
                ('spcl_cnd', models.TextField()),
            ],
            options={
                'db_table': 'deposit_products',
            },
        ),
        migrations.CreateModel(
            name='LeaseLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.CharField(help_text='금융회사 코드', max_length=20)),
                ('kor_co_nm', models.CharField(help_text='금융회사명', max_length=100)),
                ('fin_prdt_cd', models.CharField(help_text='금융상품 코드', max_length=100)),
                ('fin_prdt_nm', models.CharField(help_text='금융상품명', max_length=200)),
                ('join_way', models.CharField(help_text='가입방법', max_length=300)),
                ('loan_inci_expn', models.TextField(help_text='대출부대비용')),
                ('erly_rpay_fee', models.TextField(help_text='중도상환수수료')),
                ('dly_rate', models.TextField(help_text='연체이자율')),
                ('loan_lmt', models.TextField(help_text='대출한도')),
                ('dcls_strt_day', models.CharField(help_text='공시 시작일', max_length=8)),
                ('dcls_end_day', models.CharField(blank=True, help_text='공시 종료일', max_length=8, null=True)),
                ('fin_co_subm_day', models.CharField(help_text='금융회사 제출일', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'products_leaseloan',
            },
        ),
        migrations.CreateModel(
            name='LeaseLoanOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.CharField(help_text='금융상품 코드', max_length=100)),
                ('rpay_type', models.CharField(choices=[('D', '분할상환방식'), ('S', '만기일시상환방식')], help_text='상환방식', max_length=1)),
                ('lend_rate_type', models.CharField(choices=[('F', '고정금리'), ('C', '변동금리')], help_text='금리유형', max_length=1)),
                ('lend_rate_min', models.DecimalField(decimal_places=2, help_text='최저금리', max_digits=5)),
                ('lend_rate_max', models.DecimalField(decimal_places=2, help_text='최고금리', max_digits=5)),
                ('lend_rate_avg', models.DecimalField(blank=True, decimal_places=2, help_text='평균금리', max_digits=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'products_leaseloan_option',
            },
        ),
        migrations.CreateModel(
            name='MortgageLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.CharField(help_text='금융회사 코드', max_length=20)),
                ('kor_co_nm', models.CharField(help_text='금융회사명', max_length=100)),
                ('fin_prdt_cd', models.CharField(help_text='금융상품 코드', max_length=100)),
                ('fin_prdt_nm', models.CharField(help_text='금융상품명', max_length=200)),
                ('join_way', models.CharField(help_text='가입방법', max_length=300)),
                ('loan_inci_expn', models.TextField(help_text='대출부대비용')),
                ('erly_rpay_fee', models.TextField(help_text='중도상환수수료')),
                ('dly_rate', models.TextField(help_text='연체이자율')),
                ('loan_lmt', models.TextField(help_text='대출한도')),
                ('dcls_strt_day', models.CharField(help_text='공시 시작일', max_length=8)),
                ('dcls_end_day', models.CharField(blank=True, help_text='공시 종료일', max_length=8, null=True)),
                ('fin_co_subm_day', models.CharField(help_text='금융회사 제출일', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SavingProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('join_way', models.TextField()),
                ('spcl_cnd', models.TextField()),
            ],
            options={
                'db_table': 'saving_products',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('deposit_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.depositproducts')),
                ('saving_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.savingproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'wishlist',
            },
        ),
        migrations.CreateModel(
            name='SavingOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField()),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('intr_rate', models.FloatField(default=-1)),
                ('intr_rate2', models.FloatField(default=-1)),
                ('save_trm', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.savingproducts')),
            ],
            options={
                'db_table': 'saving_options',
            },
        ),
        migrations.CreateModel(
            name='MortgageLoanOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.CharField(help_text='금융상품 코드', max_length=100)),
                ('mrtg_type', models.CharField(choices=[('A', '아파트'), ('E', '아파트외')], help_text='담보유형', max_length=1)),
                ('rpay_type', models.CharField(choices=[('D', '분할상환방식'), ('S', '만기일시상환방식')], help_text='상환방식', max_length=1)),
                ('lend_rate_type', models.CharField(choices=[('F', '고정금리'), ('C', '변동금리')], help_text='금리유형', max_length=1)),
                ('lend_rate_min', models.DecimalField(decimal_places=2, help_text='최저금리', max_digits=5)),
                ('lend_rate_max', models.DecimalField(decimal_places=2, help_text='최고금리', max_digits=5)),
                ('lend_rate_avg', models.DecimalField(blank=True, decimal_places=2, help_text='평균금리', max_digits=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='products.mortgageloan')),
            ],
        ),
        migrations.AddIndex(
            model_name='mortgageloan',
            index=models.Index(fields=['fin_co_no', 'fin_prdt_cd'], name='products_mo_fin_co__8acda5_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='mortgageloan',
            unique_together={('fin_co_no', 'fin_prdt_cd')},
        ),
        migrations.AddField(
            model_name='leaseloanoption',
            name='loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='products.leaseloan'),
        ),
        migrations.AddIndex(
            model_name='leaseloan',
            index=models.Index(fields=['fin_co_no', 'fin_prdt_cd'], name='products_le_fin_co__78c2e7_idx'),
        ),
        migrations.AddField(
            model_name='depositoptions',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.depositproducts'),
        ),
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together={('user', 'deposit_product', 'saving_product')},
        ),
        migrations.AddIndex(
            model_name='mortgageloanoption',
            index=models.Index(fields=['loan', 'fin_prdt_cd', 'mrtg_type', 'rpay_type', 'lend_rate_type'], name='products_mo_loan_id_0a6e0a_idx'),
        ),
        migrations.AddIndex(
            model_name='leaseloanoption',
            index=models.Index(fields=['loan', 'fin_prdt_cd', 'rpay_type', 'lend_rate_type'], name='products_le_loan_id_8444be_idx'),
        ),
    ]
