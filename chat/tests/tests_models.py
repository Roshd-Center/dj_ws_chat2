from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from chat.models import Topic, Message


class TopicTest(TestCase):

    def setUp(self) -> None:
        self.users = [User.objects.create(username='test0'),
                      User.objects.create(username='test1'),
                      User.objects.create(username='test2'),
                      User.objects.create(username='test3')]
        self.topic = Topic.objects.create(owner=self.users[0], title='Test1')
        self.topic.participants.add(self.users[1])
        self.topic.participants.add(self.users[2])
        self.topic.participants.add(self.users[3])

    def test_add_owner_to_participants(self):
        print(Topic.objects.get(id=self.topic.id).participants.all())
        self.assertIn(self.users[0],Topic.objects.get(id=self.topic.id).participants.all())


class MessageTest(TopicTest):

    def setUp(self) -> None:
        super().setUp()
        self.new_topic = Topic.objects.create(owner=self.users[0], title='Test2')
        self.topic.participants.add(self.users[1])
        self.topic.participants.add(self.users[2])
        self.topic.participants.add(self.users[3])

    def test_send_simple_msg(self):
        msg1 = Message.objects.create(sender=self.users[0], content='Test1', topic=self.topic)
        msg2 = Message.objects.create(sender=self.users[1], content='Test2', topic=self.topic)
        self.assertIn(msg1, self.topic.messages.all())
        self.assertIn(msg2, self.topic.messages.all())


    def test_send_reply_msg(self):
        msg1 = Message.objects.create(sender=self.users[0], content='Test1', topic=self.topic)
        msg2 = Message.objects.create(sender=self.users[1], content='Test2', topic=self.topic, reply=msg1)
        self.assertIn(msg2, msg1.replies.all())

    def test_send_foreign_reply_msg_failed(self):
        msg1 = Message.objects.create(sender=self.users[0], content='Test1', topic=self.topic)
        self.assertRaises(Message.ForeignTopicReply, Message.objects.create,
                          sender=self.users[1], content='Test2', topic=self.new_topic, reply=msg1)

    def test_forward_msg(self):
        msg1 = Message.objects.create(sender=self.users[0], content='Test1', topic=self.topic)
        msg2 = msg1.forward(self.users[1], self.new_topic)
        self.assertEqual(msg1.content, msg2.content)


    def test_seen_msg(self):
        msg1 = Message.objects.create(sender=self.users[0], content='Test1', topic=self.topic)
        msg1.seen(self.users[3])
        self.assertIn(self.users[3], msg1.seeners.all())

