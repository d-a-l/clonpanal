from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def followers_url(obj):
    ct_id = ContentType.objects.get_for_model(obj).pk
    return reverse('social-followers', None, (ct_id, obj.pk))


@register.simple_tag
def following_url(user):
    return reverse('social-following', None, (user.pk,))


@register.simple_tag
def unfollow_url(actor):
    content_type = ContentType.objects.get_for_model(actor)
    return reverse('actstream_unfollow', kwargs={'content_type_id': content_type.pk,
                                                 'object_id': actor.pk})


@register.simple_tag
def actual_follow_all_url(actor):
    content_type = ContentType.objects.get_for_model(actor)
    return reverse('actstream_follow_all', kwargs={'content_type_id': content_type.pk,
                                                   'object_id': actor.pk})


@register.simple_tag(takes_context=True)
def message_form_for(context, obj):
    from social.forms import MessageWithContentForm
    content_type = ContentType.objects.get_for_model(obj)

    form = MessageWithContentForm({'content_type': content_type,
                                   'object_id': obj.pk})

    return render_to_string("social/message_with_content_form.html",
                            context={'form': form},
                            request=context.get('request'))


@register.simple_tag(takes_context=True)
def show_messages_for(context, obj):
    from social.models import Message
    content_type = ContentType.objects.get_for_model(obj)

    messages = Message.objects.filter(object_id=obj.pk,
                                      content_type=content_type)
    return render_to_string("social/messages_for_object.html",
                            {"messages": messages},
                            request=context.get('request'))

@register.filter
def render_collaborators(project):
    return " ".join(["@%s" % user.username for user in project.collaborators()])

