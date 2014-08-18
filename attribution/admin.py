from django.contrib import admin

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


class DateAdmin (admin.ModelAdmin):

    list_display = ('name', 'sort_date', 'notes')


class PersonAdmin (admin.ModelAdmin):

    list_display = ('name', 'date', 'sort_date')


class PropertyAssertionAdmin (admin.ModelAdmin):

    list_display = ('source_abbreviation', 'argument', 'is_preferred')
    list_display_links = ('source_abbreviation', 'argument')
    list_filter = ('is_preferred',)
    search_fields = ('source__name', 'argument')
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

    def source_abbreviation (self, obj):
        return obj.source.abbreviation

class SourceAdmin (NamableAdmin, admin.ModelAdmin):

    fields = ('name', 'date', 'abbreviation', 'notes')
    list_display = ('abbreviation', 'name', 'date')
    search_fields = ['name']


class TextAdmin (admin.ModelAdmin):

    actions = ['regenerate_identifier']
    search_fields = ('cached_identifier__identifier',)

    def regenerate_identifier (self, request, queryset):
        for text in queryset:
            text.save()
    regenerate_identifier.short_description = 'Update the generated identifier for the selected texts'


admin.site.register(Date, DateAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PropertyAssertion, PropertyAssertionAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Title)
