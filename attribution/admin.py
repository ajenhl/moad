from django.contrib import admin

from .models import Identifier, Person, PropertyAssertion, Source, Text, Title


class IdentifierInline (admin.TabularInline):

    model = Identifier


class TextAssertionsInline (admin.TabularInline):

    model = PropertyAssertion.texts.through


class PropertyAssertionAdmin (admin.ModelAdmin):

    inlines = [IdentifierInline]


class TextAdmin (admin.ModelAdmin):

    inlines = [TextAssertionsInline]


admin.site.register(Person)
admin.site.register(PropertyAssertion, PropertyAssertionAdmin)
admin.site.register(Source)
admin.site.register(Text, TextAdmin)
admin.site.register(Title)
