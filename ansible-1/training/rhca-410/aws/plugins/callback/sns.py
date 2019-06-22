# from plugins/callback/slack.py

from ansible.constants import mk_boolean
from ansible.module_utils.urls import open_url
from ansible.plugins.callback import CallbackBase

try:
    import prettytable
    HAS_PRETTYTABLE = True
except ImportError:
    HAS_PRETTYTABLE = False

class CallbackModule(CallbackBase):
    """This is an ansible callback plugin that sends status
    updates to a Slack channel during playbook execution.

    This plugin makes use of the following environment variables:
        SLACK_WEBHOOK_URL (required): Slack Webhook URL
        SLACK_CHANNEL     (optional): Slack room to post in. Default: #ansible
        SLACK_USERNAME    (optional): Username to post as. Default: ansible
        SLACK_INVOCATION  (optional): Show command line invocation
                                      details. Default: False

    Requires:
        prettytable

    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'sns'
    CALLBACK_NEEDS_WHITELIST = True

...

    def send_msg(self, attachments):
        payload = {
            'channel': self.channel,
            'username': self.username,
            'attachments': attachments,
            'parse': 'none',
            #'icon_url': ('http://www.ansible.com/hs-fs/hub/330046/file-449187601-png/ansible_badge.png'),
             
            'icon_url': (''),
        }

        data = json.dumps(payload)
        self._display.debug(data)
        self._display.debug(self.webhook_url)
        try:
            response = open_url(self.webhook_url, data=data)
            return response.read()
        except Exception as e:
            self._display.warning('Could not submit message to Slack: %s' %
                                  str(e))

    def v2_playbook_on_play_start(self, play):
        """Display Play start messages"""

        name = play.name or 'Play name not specified (%s)' % play._uuid
        msg = '*Starting play* (_%s_)\n\n*%s*' % (self.guid, name)
        attachments = [
            {
                'fallback': msg,
                'text': msg,
                'color': 'warning',
                'mrkdwn_in': ['text', 'fallback', 'fields'],
            }
        ]
        self.send_msg(attachments=attachments)
