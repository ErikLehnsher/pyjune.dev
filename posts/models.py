from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# =========================
# Category
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================
# Tag
# =========================
class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================
# Post (FULL – match Admin)
# =========================
class Post(models.Model):
    # ---- Basic ----
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    excerpt = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )

    # ---- Meta (custom domain fields) ----
    odoo_version = models.CharField(max_length=20, blank=True)
    module = models.CharField(max_length=100, blank=True)
    error_keyword = models.CharField(max_length=255, blank=True)

    # ---- Tiptap Content ----
    content_json = models.JSONField(
        null=True,
        blank=True,
        help_text="Raw Tiptap JSON"
    )

    html_content = models.TextField(
        blank=True,
        help_text="Rendered HTML from Tiptap"
    )

    # ---- Publish ----
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
        ],
        default='draft'
    )

    is_published = models.BooleanField(default=True)

    # ---- Time ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']   # ✅ FIX lỗi trước đó

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
