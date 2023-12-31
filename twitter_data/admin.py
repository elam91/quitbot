from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from .models import Feature, Topic, Keyword, TwitterUser, Tweet, Webhook


class TopicsAdmin(admin.ModelAdmin):
    filter_horizontal = ("keywords",)


class TweetsAdmin(ImportExportModelAdmin):
    list_display = ("tweet_id", "user", "retweeted", "liked", "replied", "go_to_tweet")
    list_filter = (
        "retweeted",
        "liked",
        "replied",
    )
    search_fields = ["user__user_profile", "text"]
    actions = ["export_as_csv_response"]

    def go_to_tweet(self, obj):
        link = f"https://twitter.com/{obj.user.user_profile}/status/{obj.tweet_id}"
        return mark_safe(f'<a href="{link}" target="blank">link</a>')


class TwitterUsersAdmin(ImportExportModelAdmin):
    list_display = (
        "user_profile",
        "followed",
        "ignore",
        "must_follow",
        "must_like",
        "must_rt",
        "priority",
        "go_to_profile",
    )
    list_editable = (
        "ignore",
        "must_follow",
        "must_like",
        "must_rt",
        "priority",
    )
    list_filter = (
        "ignore",
        "must_follow",
        "must_like",
        "must_rt",
        "priority",
    )
    search_fields = ["user_profile"]

    def go_to_profile(self, obj):
        link = f"https://twitter.com/{obj.user_profile}"
        return mark_safe(f'<a href="{link}" target="blank">link</a>')


admin.site.register(Topic, TopicsAdmin)
admin.site.register(Keyword)
admin.site.register(TwitterUser, TwitterUsersAdmin)
admin.site.register(Tweet, TweetsAdmin)
admin.site.register(Feature)
admin.site.register(Webhook)
