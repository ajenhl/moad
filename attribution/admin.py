from django.contrib import admin

from haystack.admin import SearchModelAdmin

from .models import Date, Identifier, Person, PersonRole, PropertyAssertion, Source, Text, Title


class DateInline (admin.TabularInline):

    extra = 1
    model = Date


class IdentifierInline (admin.TabularInline):

    extra = 1
    model = Identifier


class PersonInvolvementInline (admin.TabularInline):

    model = PropertyAssertion.people.through
    raw_id_fields = ('person',)
    autocomplete_lookup_fields = {
        'fk': ['person'],
    }


class TitleInline (admin.TabularInline):

    extra = 1
    model = Title


class DateAdmin (admin.ModelAdmin):

    list_display = ('name', 'sort_date', 'notes')


class PersonAdmin (SearchModelAdmin):

    list_display = ('name', 'date', 'sort_date')
    search_fields = ('name', 'date', 'sort_date')
    fieldsets = (
        (None, {'fields': ('name', 'date', 'sort_date', 'notes')}),
    )


class PropertyAssertionAdmin (SearchModelAdmin):

    list_display = ('source_abbreviation', 'argument', 'is_preferred')
    list_display_links = ('source_abbreviation', 'argument')
    list_filter = ('is_preferred',)
    search_fields = ('argument',)
    fieldsets = (
        (None, {'fields': ('texts',)}),
        (None, {'classes': ('placeholder person_involvements-group',), 'fields': ()}),
        (None, {'classes': ('placeholder titles-group',), 'fields': ()}),
        (None, {'classes': ('placeholder dates-group',), 'fields': ()}),
        (None, {'classes': ('placeholder identifiers-group',), 'fields': ()}),
        ('Source and argument',
         {'fields': ('source', 'source_detail', 'argument', 'is_preferred')}),
    )
    filter_horizontal = ['texts']
    inlines = [DateInline, IdentifierInline, TitleInline,
               PersonInvolvementInline]
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


class SourceAdmin (SearchModelAdmin):

    fields = ('name', 'date', 'abbreviation', 'notes')
    list_display = ('abbreviation', 'name', 'date')
    search_fields = ['name']


class TextAdmin (SearchModelAdmin):

    actions = ['regenerate_identifier']
    search_fields = ('cached_identifier__identifier',)

    def regenerate_identifier (self, request, queryset):
        for text in queryset:
            text.save()
    regenerate_identifier.short_description = 'Update the generated identifier for the selected texts'


admin.site.register(Date, DateAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonRole)
admin.site.register(PropertyAssertion, PropertyAssertionAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Title)
