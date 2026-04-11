from django.contrib import admin
from .models import Resume, ResumeStat, ResumeSocial, ResumeFloatingCard, ResumeSkill, ResumeJourney, SkillCategory, Skill, Profession, Certification, Journey, Excellence, ServiceSection, Service, PortfolioSection, PortfolioCategory, PortfolioItem, TestimonialSection, Testimonial, ReviewPlatform, FAQSection, FAQ, ContactSection, ContactMessage

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

class ExcellenceInline(admin.TabularInline):
    model= Excellence
    extra = 1

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

class ResumeJourneyInline(admin.TabularInline):
    model = ResumeJourney
    extra = 1
    fields = ('year', 'description', 'order', 'is_active')

class ResumeSkillInline(admin.TabularInline):
    model = ResumeSkill
    extra = 1
    fields = (
        'title',
        'icon_class',
        'description',
        'aos_animation',
        'aos_delay',
        'order',
        'is_active'
    )

class ResumeFloatingCardInline(admin.TabularInline):
    model = ResumeFloatingCard
    extra = 1
    fields = (
        'title',
        'icon_class',
        'card_class',
        'aos_animation',
        'aos_delay',
        'order',
        'is_active'
    )

class ResumeSocialInline(admin.TabularInline):
    model = ResumeSocial
    extra = 1
    fields = ('platform', 'url', 'icon_class', 'order', 'is_active')
    ordering = ('order',)

class ResumeStatInline(admin.TabularInline):
    model = ResumeStat
    extra = 1
    fields = ('icon_class', 'value', 'label', 'aos_delay', 'order')
    ordering = ('order',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'theme', 'is_active', 'updated_at')
    list_filter = ('theme', 'is_active')
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'title', 'email', 'phone', 'tags', 'tag_line', 'short_desc')}),
        ('Images', {'fields': ('profile_image', 'banner_image')}),
        ('Resume Details', {'fields': ('summary', 'skills', 'experience', 'education')}),
        ('Theme', {'fields': ('theme',)}),
        ('Status', {'fields': ('is_active',)}),
    )
    
    inlines = [ResumeStatInline, ResumeSocialInline, ResumeFloatingCardInline, ResumeSkillInline, ResumeJourneyInline]
    
@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'order')
    inlines = [SkillInline]

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    inlines = [CertificationInline]
    filter_horizontal = ('resume_stats',)

@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    inlines = [ExcellenceInline]

@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    inlines = [ServiceInline]

class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem
    extra = 1
    fields = (
        'title',
        'image',
        'order',
        'is_active'
    )
    ordering = ('order',)
    show_change_link = True


class PortfolioCategoryInline(admin.TabularInline):
    model = PortfolioCategory
    extra = 1
    fields = ('title', 'slug', 'order')
    ordering = ('order',)


@admin.register(PortfolioSection)
class PortfolioSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'is_active')
    inlines = [PortfolioCategoryInline, PortfolioItemInline]


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'is_active')
    list_filter = ('section', 'is_active', 'categories')
    filter_horizontal = ('categories',)
    ordering = ('section', 'order')


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    fields = (
        'author_name',
        'author_role',
        'source',
        'rating',
        'order',
        'is_active'
    )
    ordering = ('order',)
    show_change_link = True


class ReviewPlatformInline(admin.TabularInline):
    model = ReviewPlatform
    extra = 1


@admin.register(TestimonialSection)
class TestimonialSectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'average_rating',
        'total_reviews',
        'is_active'
    )
    inlines = [TestimonialInline, ReviewPlatformInline]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'author_name',
        'source',
        'rating',
        'section',
        'order',
        'is_active'
    )
    list_filter = ('section', 'rating', 'is_active')
    ordering = ('section', 'order')

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = (
        'question',
        'order',
        'is_active'
    )
    ordering = ('order',)
    show_change_link = True


@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'resume',
        'order',
        'is_active'
    )
    list_filter = ('is_active', 'resume')
    ordering = ('order',)
    inlines = [FAQInline]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'section',
        'order',
        'is_active'
    )
    list_filter = ('section', 'is_active')
    ordering = ('section', 'order')

@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'receive_email_at', 'is_active')
    list_filter = ('is_active', 'resume')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')