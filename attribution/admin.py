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


class TextAssertionsInline (admin.TabularInline):

    model = PropertyAssertion.texts.through


class TitleInline (admin.TabularInline):

    extra = 1
    model = Title


class PropertyAssertionAdmin (admin.ModelAdmin):

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


class SourceAdmin (NamableAdmin, admin.ModelAdmin):

    pass


class TextAdmin (admin.ModelAdmin):

    inlines = [TextAssertionsInline]


admin.site.register(Date)
admin.site.register(Person)
admin.site.register(PropertyAssertion, PropertyAssertionAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Title)
