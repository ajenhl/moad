from django.contrib import admin

from haystack.admin import SearchModelAdmin

from .behaviours import DRAFT_STATUS, PUBLISHED_STATUS
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


class PublishableModelAdmin (SearchModelAdmin):

    def get_queryset(self, request):
        qs = super(PublishableModelAdmin, self).get_queryset(request)
        user = request.user
        if not user.has_perm('attribution.change_published_items'):
            qs = qs.filter(status=DRAFT_STATUS).filter(author=user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        fields = []
        user = request.user
        if not user.has_perm('attribution.change_assertion_author'):
            fields.append('author')
        if not user.has_perm('attribution.change_assertion_status'):
            fields.append('status')
        return fields

    def has_change_permission(self, request, obj=None):
        permission = super(PublishableModelAdmin, self).has_change_permission(
            request, obj)
        if obj is not None:
            if request.user == obj.author and obj.status == DRAFT_STATUS:
                permission = True
        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(PublishableModelAdmin, self).has_delete_permission(
            request, obj)
        if obj is not None:
            if request.user == obj.author and obj.status == DRAFT_STATUS:
                permission = True
        return permission

    def save_model(self, request, obj, form, change):
        # Set the author when creating the object.
        if not change:
            obj.author = request.user
        obj.save()


class RelatedModelAdmin (admin.ModelAdmin):

    """ModelAdmin subclass that handles permissions for models that are
    dependent on a PublishableModelAdmin model.

    These dependent models (ie, that has a ForeignKey to
    PropertyAssertion, Person, Source, etc.) do not require their own
    owner and status fields.

    """

    def get_queryset(self, request):
        qs = super(RelatedModelAdmin, self).get_queryset(request)
        user = request.user
        if not user.has_perm('attribution.change_published_items'):
            qs = qs.filter(assertion__status=DRAFT_STATUS).filter(
                assertion__author=user)
        return qs

    def has_change_permission(self, request, obj=None):
        permission = super(RelatedModelAdmin, self).has_change_permission(
            request, obj)
        if obj is not None:
            assertion = obj.assertion
            if request.user == assertion.author and \
               assertion.status == DRAFT_STATUS:
                permission = True
        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(RelatedModelAdmin, self).has_delete_permission(
            request, obj)
        if obj is not None:
            assertion = obj.assertion
            if request.user == assertion.author and \
               assertion.status == DRAFT_STATUS:
                permission = True
        return permission


class DateAdmin (RelatedModelAdmin):

    list_display = ('name', 'sort_date', 'notes')


class PersonAdmin (PublishableModelAdmin):

    list_display = ('name', 'date', 'sort_date')
    search_fields = ('name', 'date', 'sort_date')
    fieldsets = (
        (None, {'fields': ('name', 'date', 'sort_date', 'notes')}),
    )


class PropertyAssertionAdmin (PublishableModelAdmin):

    list_display = ('source_abbreviation', 'argument', 'is_preferred',
                    'status', 'author')
    list_display_links = ('source_abbreviation', 'argument')
    list_filter = ('is_preferred', 'status', 'author')
    search_fields = ('argument',)
    fieldsets = (
        (None, {'fields': ('texts',)}),
        (None, {'classes': ('placeholder person_involvements-group',),
                'fields': ()}),
        (None, {'classes': ('placeholder titles-group',), 'fields': ()}),
        (None, {'classes': ('placeholder dates-group',), 'fields': ()}),
        (None, {'classes': ('placeholder identifiers-group',), 'fields': ()}),
        ('Source and argument',
         {'fields': ('source', 'source_detail', 'argument', 'is_preferred')}),
        ('Metadata',
         {'fields': ('author', 'contributors', 'status')}),
    )
    filter_horizontal = ['texts', 'contributors']
    inlines = [DateInline, IdentifierInline, TitleInline,
               PersonInvolvementInline]
    raw_id_fields = ('source',)
    autocomplete_lookup_fields = {
        'fk': ['source'],
    }

    def get_readonly_fields(self, request, obj=None):
        fields = super(PropertyAssertionAdmin, self).get_readonly_fields(
            request)
        if not request.user.has_perm(
                'attribution.change_assertion_contributor'):
            fields.append('contributors')
        return fields

    def save_model(self, request, obj, form, change):
        super(PropertyAssertionAdmin, self).save_model(request, obj, form,
                                                       change)
        # If the status is changed to Published, make all of the
        # associated objects Published as well.
        if obj.status == PUBLISHED_STATUS:
            for person in Person.objects.filter(status=DRAFT_STATUS):
                person.status = PUBLISHED_STATUS
                person.save()
            for source in Source.objects.filter(status=DRAFT_STATUS):
                source.status = PUBLISHED_STATUS
                source.save()
            for text in Text.objects.filter(status=DRAFT_STATUS):
                text.status = PUBLISHED_STATUS
                text.save()

    def save_related(self, request, form, formsets, change):
        super(PropertyAssertionAdmin, self).save_related(request, form,
                                                         formsets, change)
        for text in form.instance.texts.all():
            text.save()

    def source_abbreviation(self, obj):
        return obj.source.abbreviation


class SourceAdmin (PublishableModelAdmin):

    fields = ('name', 'date', 'abbreviation', 'notes')
    list_display = ('abbreviation', 'name', 'date')
    search_fields = ['name']


class TextAdmin (PublishableModelAdmin):

    actions = ['regenerate_identifier']
    search_fields = ('identifier',)

    def get_readonly_fields(self, request, obj=None):
        fields = super(TextAdmin, self).get_readonly_fields(request)
        fields.append('identifier')
        return fields

    def regenerate_identifier(self, request, queryset):
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
