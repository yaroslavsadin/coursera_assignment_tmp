from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    # Создать пользователя first_name = u1, last_name = u1.
    # FIXME use `create` method instead
    u1 = User(first_name='u1', last_name='u1')
    u1.save()
    # Создать пользователя first_name = u2, last_name = u2.
    u2 = User(first_name='u2', last_name='u2')
    u2.save()
    # Создать пользователя first_name = u3, last_name = u3.
    u3 = User(first_name='u3', last_name='u3')
    u3.save()
    # Создать блог title = blog1, author = u1.
    blog1 = Blog(title='blog1', author=u1)
    blog1.save()
    # Создать блог title = blog2, author = u1.
    blog2 = Blog(title='blog2', author=u1)
    blog2.save()
    # Подписать пользователей u1 u2 на blog1, u2 на blog2.
    blog1.subscribers.add(u1)
    blog1.subscribers.add(u2)
    blog1.save()
    blog2.subscribers.add(u2)
    blog2.save()
    # Создать топик title = topic1, blog = blog1, author = u1.
    topic1 = Topic(title='topic1', blog=blog1, author=u1)
    topic1.save()
    # Создать топик title = topic2_content, blog = blog1, author = u3, created = 2017-01-01.
    topic2 = Topic(
        title='topic2_content', blog=blog1,
        author=u3, created=datetime(2017, 1, 1)  # FIXME use tzinfo
    )
    topic2.save()
    # Лайкнуть topic1 пользователями u1, u2, u3.
    topic1.likes.add(u1)
    topic1.likes.add(u2)
    topic1.likes.add(u3)
    topic1.save()


def edit_all():
    # FIXME use `update` method right after `all()`
    users = User.objects.all()
    for user in users:
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    # FIXME cna use filter + `update`
    users = User.objects.filter(first_name__in=['u1', 'u2']).all()
    for user in users:
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    User.objects.get(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    # FIXME `through` table
    blogs = Blog.objects.all()
    user = User.objects.get(first_name='u2')
    for blog in blogs:
        blog.subscribers.remove(user)

def get_topic_created_grated():
    return Topic.objects.filter(created__gt='2018-01-01')


def get_topic_title_ended():
    q = Topic.objects.filter(title__endswith='content')
    print(q.query)
    return q


def get_user_with_limit():
    q = User.objects.order_by('-id')
    print(q.query)
    return q[:2]


def get_topic_count():
    q = (
        Blog.objects
        .annotate(topic_count=Count('topic__id'))
        .order_by('topic_count')
    )
    print(q.query)
    return q


def get_avg_topic_count():
    q = (
        Blog.objects
        .annotate(topic_count=Count('topic__id'))
    )
    print(q.query)
    return q.aggregate(avg=Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    q = (
        Blog.objects.filter(topic__id__isnull=False).distinct()
    )
    print(q.query)
    return q


def get_topic_by_u1():
    q = (
        Topic.objects.filter(author__first_name='u1')
    )
    print(q.query)
    return q


def get_user_that_dont_have_blog():
    q = (
        User.objects.filter(blog__id__isnull=True)
    )
    print(q.query)
    return q


def get_topic_that_like_all_users():
    q = Topic.objects.all()

    for u in User.objects.all():
        q = q.filter(likes=u)

    print(q.query)
    return q


def get_topic_that_dont_have_like():
    q = Topic.objects.filter(~Q(likes__in=User.objects.all()))
    print(q.query)
    return q
