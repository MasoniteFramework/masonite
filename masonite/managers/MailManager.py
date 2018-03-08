from masonite.managers.Manager import Manager


class MailManager(Manager):

    config = 'MailConfig'
    driver_prefix = 'Mail'
