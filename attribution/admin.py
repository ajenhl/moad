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


class PropertyAssertionAdmin (admin.ModelAdmin):

    list_display = ('source', 'argument', 'is_preferred')
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
admin.site.register(Person)
admin.site.register(PropertyAssertion, PropertyAssertionAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Title)
