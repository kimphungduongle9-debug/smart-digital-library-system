from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Quản trị viên'),
        ('LIBRARIAN', 'Thủ thư'),
        ('READER', 'Sinh viên/Giảng viên'),
    )

    avatar = models.ImageField(upload_to='users/%Y/%m', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='READER')
    is_verified_librarian = models.BooleanField(default=False)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Document(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255)
    published_year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    cover_image = models.ImageField(upload_to='documents/covers/%Y/%m', null=True, blank=True)
    file = models.FileField(upload_to='documents/files/%Y/%m', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    popularity = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class DocumentAccess(BaseModel):
    ACCESS_CHOICES = (
        ('VIEW', 'Truy cập'),
        ('BORROW', 'Mượn'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='VIEW')

    def __str__(self):
        return f'{self.user.username} - {self.document.title}'


class Payment(BaseModel):
    METHOD_CHOICES = (
        ('CASH', 'Tiền mặt'),
        ('PAYPAL', 'PayPal'),
        ('STRIPE', 'Stripe'),
        ('MOMO', 'MoMo'),
        ('ZALOPAY', 'ZaloPay'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Đang chờ'),
        ('SUCCESS', 'Thành công'),
        ('FAILED', 'Thất bại'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCCESS')

    def __str__(self):
        return f'{self.user.username} - {self.document.title} - {self.amount}'