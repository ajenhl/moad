from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.html import escape

from .models import Date, Identifier, Person, PropertyAssertion, Source, Text, Title


class NamableAdmin ():

    search_fields = ['name']


class DateInline (admin.TabularInline):

    extra = 1
    model = Date


class IdentifierInline (admin.TabularInline):

    extra = 1
    model = Identifier


class TitleInline (admin.TabularInline):

    extra = 1
    model = Title


class LogEntryAdmin (admin.ModelAdmin):

    # Code from https://djangosnippets.org/snippets/3009/

    date_hierarchy = 'action_time'
    readonly_fields = admin.models.LogEntry._meta.get_all_field_names()
    list_filter = ['user', 'content_type', 'action_flag']
    search_fields = ['object_repr', 'change_message']
    list_display = ['action_time', 'user', 'content_type', 'object_link',
                    'action_flag', 'change_message']

    def has_add_permission (self, request):
        return False

    def has_delete_permission (self, request, obj=None):
        return False

    def object_link (self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                        args=[obj.object_id])
            link = u'<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return link if obj.action_flag != admin.models.DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset (self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')



class PropertyAssertionAdmin (admin.ModelAdmin):

    list_display = ('source', 'argument', 'is_preferred')
    list_filter = ('is_preferred',)
    search_fields = ('source', 'argument')
    fieldsets = (
        (None, {'fields': ('texts',)}),
        ('People', {'fields': ('authors', 'translators')}),
        (None, {'classes': ('placeholder titles-group',), 'fields': ()}),
        (None, {'classes': ('placeholder dates-group',), 'fields': ()}),
        (None, {'classes': ('placeholder identifiers-group',), 'fields': ()}),
        ('Source and argument',
         {'fields': ('source', 'source_detail', 'argument', 'is_preferred')}),
    )
    filter_horizontal = ['authors', 'texts', 'translators']
    inlines = [DateInline, IdentifierInline, TitleInline]
    raw_id_fields = ('source',)
    autocomplete_lookup_fields = {
        'fk': ['source'],
    }

    def save_related (self, request, form, formsets, change):
        super(PropertyAssertionAdmin, self).save_related(request, form,
                                                         formsets, change)
        for text in form.instance.texts.all():
            text.save()

class SourceAdmin (NamableAdmin, admin.ModelAdmin):

    list_display = ('name', 'date', 'abbreviation')
    search_fields = ['name']


class TextAdmin (admin.ModelAdmin):

    actions = ['regenerate_identifier']
    search_fields = ('cached_identifier__identifier',)

    def regenerate_identifier (self, request, queryset):
        for text in queryset:
            text.save()
    regenerate_identifier.short_description = 'Update the generated identifier for the selected texts'


admin.site.register(Date)
admin.site.register(admin.models.LogEntry, LogEntryAdmin)
admin.site.register(Person)
admin.site.register(PropertyAssertion, PropertyAssertionAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Title)
